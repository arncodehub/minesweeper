# Hides the pygame support prompt
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"

# Imports required libraries
import pygame
import random

from collections import deque

# Initializes `pygame` library and pygame's `font` module
pygame.init()
pygame.font.init()

# Initializes window and set's window title to `Minesweeper`
window = pygame.display.set_mode([480, 480])
pygame.display.set_caption("Minesweeper")
pygame.display.update()

# Sets up the pygame clock to maintain a stable 60FPS, and the `impact regular` font
clock = pygame.time.Clock()
font = pygame.font.SysFont('Impact Regular', 50)

# Sets the dimensions of the game grid
WIDTH = 10
HEIGHT = 10

# Function to generate a 2D mine grid of 1s (mines) and 0s (not mines)
def generate_mine_grid(mines):
  new_mine_grid = []
  mine_locations = []
  for i in range(mines):
    new_location = random.randint(1, WIDTH*HEIGHT)
    while new_location in mine_locations:
      new_location = random.randint(1, WIDTH*HEIGHT)
    mine_locations.append(new_location)
  for x in range(WIDTH):
    new_mine_subgrid = []
    for y in range(HEIGHT):
      spot_idx = x * HEIGHT + y + 1
      is_mine = 0
      if spot_idx in mine_locations:
        is_mine = 1
      new_mine_subgrid.append(is_mine)
    new_mine_grid.append(new_mine_subgrid)
  return new_mine_grid, mine_locations


# Takes in a 2D mine grid of 0s and 1s, and set's -1s in place of mines.
# For non-mine cells, number of surrounding mines is a value from 0-8.
def generate_number_grid(mine_grid):
  new_number_grid = []
  for x in range(WIDTH):
    new_number_subgrid = []
    for y in range(HEIGHT):
      this_cell = mine_grid[x][y]
      if this_cell:  # if it is a mine
        new_number_subgrid.append(-1)
        continue  # add `-1` and move on!
      neighbor_cells = []
      for i in range(-1, 2, 1):  # i represents X offset
        for j in range(-1, 2, 1):  # j represents Y offset
          if [i, j] == [0, 0]:  # this would be the same cell!
            continue  # just move on!
          if x + i < 0 or x + i > WIDTH-1 or y + j < 0 or y + j > HEIGHT-1:  # this would be out of bounds!
            continue  # just move on!
          neighbor_cells.append(mine_grid[x + i][
              y + j])  # finally add if it is in bounds and not the same cell!
      neighbors = neighbor_cells.count(1)
      new_number_subgrid.append(neighbors)
    new_number_grid.append(new_number_subgrid)
  return new_number_grid

# Takes in a cell value from the `number grid` from -1 to 8, returns corresponding image path
def get_image(cell_data):
  if cell_data == -1: return "assets/mine.png"
  return f"assets/{cell_data}.png"

# Displays the minesweeper grid, based on the `uncovered`, `flagged`, and `number_grid`
def display_grid(number_grid, uncovered, flagged):
  for x in range(WIDTH):
    for y in range(HEIGHT):
      display_X = x * (480 / WIDTH)
      display_Y = y * (480 / HEIGHT)
      SIZE_X, SIZE_Y = (480 / WIDTH), (480 / HEIGHT)
      if x * HEIGHT + y + 1 in flagged:
        blit_image = pygame.image.load("assets/marked.png")
        blit_transform = pygame.transform.scale(blit_image, (SIZE_X, SIZE_Y))
        window.blit(blit_transform, (display_X, display_Y))
        continue  # move on! don't do the rest!
      if x * HEIGHT + y + 1 not in uncovered:
        blit_image = pygame.image.load("assets/covered.png")
        blit_transform = pygame.transform.scale(blit_image, (SIZE_X, SIZE_Y))
        window.blit(blit_transform, (display_X, display_Y))
        continue  # move on! don't do the rest!
      cell_data = number_grid[x][y]
      blit_path = get_image(cell_data)
      blit_img = pygame.image.load(blit_path)
      blit_transform = pygame.transform.scale(blit_img, (SIZE_X, SIZE_Y))
      window.blit(blit_transform, (display_X, display_Y))

# Gets the cell location of a click, translates mouseX, mouseY to cellX, cellY
# For instance, (cellX: 0, cellY: 0) would be the top left, (cellX: 9, cellY: 9) is bottom right
def get_cell_click():
  mouse_position = pygame.mouse.get_pos()
  mouse_X, mouse_Y = mouse_position[0], mouse_position[1]
  cell_X, cell_Y = mouse_X // (480 / WIDTH), mouse_Y // (480 / HEIGHT)
  cell_data = cell_X * HEIGHT + cell_Y + 1
  if cell_X != round(cell_X) or cell_Y != round(cell_Y):
    print("Wow, get_cell_click() seems to have an issue, it has a decimal cell x or cell y value!")
    exit()
  cell_X, cell_Y = round(cell_X), round(cell_Y)
  return cell_X, cell_Y

"""
  If the user clicks a ZERO tile, with no mines around it, "floodfill" occurs.
  All cells around the ZERO (including the tile itself) are cleared.
  If a tile around the ZERO is also a ZERO, it repeats the "floodfill" again.
  This results in a recursive floodfill until all cells surrounding the zero are cleared,
  as well as zeros surrounding the zero, zeroes surrounding those, etc.
"""

def floodfill(number_grid, cell_x, cell_y, ucc, flagged):
    new_ucc = ucc.copy()
    queue = deque([(cell_x, cell_y)])
    new_ucc.append(cell_x * HEIGHT + cell_y + 1)

    while queue:
        x, y = queue.popleft()

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_x, neighbor_y = x + i, y + j
                if (
                    0 <= neighbor_x < WIDTH
                    and 0 <= neighbor_y < HEIGHT
                    and (neighbor_x * HEIGHT + neighbor_y + 1) not in new_ucc
                    and (neighbor_x * HEIGHT + neighbor_y + 1) not in flagged  # Check if the cell is not flagged
                ):
                    new_ucc.append(neighbor_x * HEIGHT + neighbor_y + 1)
                    if number_grid[neighbor_x][neighbor_y] == 0:
                        queue.append((neighbor_x, neighbor_y))

    return new_ucc

# Uncovers a cell based on the `cell_x` and `cell_y` to uncover
# Triggers "floodfill" if a ZERO/BLANK cell is uncovered
def uncover_cell(number_grid, cell_x, cell_y, ucc, flagged):
  new_ucc = ucc.copy()
  cell_val = number_grid[cell_x][cell_y]
  cell_id = cell_x * HEIGHT + cell_y + 1
  if cell_val != 0:
    new_ucc.append(cell_id)
    return new_ucc  # case closed.
  # If it is equal to 0 indeed
  new_ucc = floodfill(number_grid, cell_x, cell_y, new_ucc, flagged)
  return new_ucc # finally! recursion complete.

# Resets the `mine_grid` and `number_grid` to ensure the first click is always a ZERO tile.
# It keeps resetting until the clicked tile IS a ZERO tile.
# First click always being a ZERO tile, gives the player a head start, making the game more fun.
def refresh_grids(X_Zero, Y_Zero, mines):
  location_to_be_zero_VALUE = None
  while location_to_be_zero_VALUE != 0:
    data = generate_mine_grid(mines)
    mine_grid, mine_locations = data[0], data[1]
    number_grid = generate_number_grid(mine_grid)
    location_to_be_zero_VALUE = number_grid[X_Zero][Y_Zero]
  return mine_grid, mine_locations, number_grid

# Displays the 'you lose' screen
def you_lose():
  text_surface = font.render('You Lose', False, (0, 0, 0))
  new_surface = font.render('[R] to Retry', False, (0, 0, 0))
  window.blit(text_surface, (100, 120))
  window.blit(new_surface, (10, 150))

# Displays the 'you win' screen
def you_win():
  text_surface = font.render('You Win', False, (0, 0, 0))
  new_surface = font.render('[R] to Replay', False, (0, 0, 0))
  window.blit(text_surface, (100, 120))
  window.blit(new_surface, (10, 150))

# Main Game Function and Main Loop
def main():
  MINES = int(WIDTH*HEIGHT // 8.33)
  data = generate_mine_grid(MINES)
  mine_grid, mine_locations = data[0], data[1]
  number_grid = generate_number_grid(mine_grid)
  locked = False
  is_first_click = True
  uncovered_cells = []
  flagged_cells = []
  has_won = False
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: # allows the 'X' to close the game
        exit()
      if event.type == pygame.MOUSEBUTTONDOWN and (not locked): # detect mouse clicks
        cell_x, cell_y = get_cell_click()
        if is_first_click == True and number_grid[cell_x][cell_y] != 0:
          refresh_data = refresh_grids(cell_x, cell_y, MINES)
          mine_grid = refresh_data[0]
          mine_locations = refresh_data[1]
          number_grid = refresh_data[2]
        if is_first_click == True:
          is_first_click = False
        cell_data = cell_x * HEIGHT + cell_y + 1
        if cell_data not in flagged_cells:
          uncovered_cells = uncover_cell(number_grid, cell_x, cell_y, uncovered_cells, flagged_cells)
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_f and (not locked):
          cell_x, cell_y = get_cell_click()
          cell_data = HEIGHT * cell_x + cell_y + 1
          if cell_data not in uncovered_cells:
            if cell_data in flagged_cells:
              del flagged_cells[flagged_cells.index(cell_data)]
            else:
              flagged_cells.append(cell_data)
        if event.key == pygame.K_r and locked: # allows the user to play again after loss or win
          data = generate_mine_grid(MINES)
          mine_grid, mine_locations = data[0], data[1]
          number_grid = generate_number_grid(mine_grid)
          locked = False
          is_first_click = True
          uncovered_cells = []
          flagged_cells = []
          has_won = False
    for cell in uncovered_cells:
      if cell in mine_locations:
        locked = True
    uncovered_cells = list(set(uncovered_cells)) # ensures no duplicates in list
    flagged_cells = list(set(flagged_cells)) # ensure no duplicates in list
    display_grid(number_grid, uncovered_cells, flagged_cells)
    if locked and (not has_won): # you win!
      you_lose()
    if ((not locked) or has_won) and (len(uncovered_cells) == WIDTH*HEIGHT - MINES): # you lose!
      for i in range(1, WIDTH*HEIGHT+1, 1):
        if i not in uncovered_cells:
          flagged_cells.append(i)
      you_win()
      locked = True
      has_won = True
    pygame.display.update()
    clock.tick(60)


if __name__ == "__main__":
  main() # calls main!
