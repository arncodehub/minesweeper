# minesweeper
This is the Minesweeper game, written in Python.

Run "main.py" to play the game.

For convenience reasons, some aspects of the original game have been modified.


**1. The First Click is now always a Zero, Blank Tile**

In regular Minesweeper, the first click is never a mine, but it can be a number tile, forcing you to guess again.

The second guess can easily land you in a mine, defeated after 2 clicks, with no way to stop it coming.


In this version, the first click is not only safe from a mine but guaranteed to be a zero, blank tile.

Zero, blank tiles have no mines around them, and they automatically open up surrounding tiles in a floodfill pattern.

If the floodfill runs into more zero tiles, those zero tiles will also floodfill.

This can make a chain reaction where one zero tile click at the start, can uncover 50 tiles at once.


**2. Flags are Automatically Placed for You once you have uncovered 88 non-mine Tiles**

In this version, the game is a 10x10 grid of tiles, and 12 of them are randomly selected to be mine tiles.

So, once you have uncovered 88 non-mine tiles, all the remaining tiles are just mines.

Some of them you have not flagged yet, so it wastes time having to flag all of them.


Not anymore! In this version, once you have uncovered 88 non-mine tiles, the remaining tiles are automatically flagged for you.

This means you do not have to waste time on that.


**3. The grid is always 10x10 with 12 mines**

There are no difficulty settings for this project, that are attainable without modifying the code.

The grid is always 10x10 with 100 tiles and with 12 mine-tiles in them.


**More Information**

Sometimes, you can get extra lucky towards the end of the game.

You can hit a zero tile, which auto uncovers many surrounding tiles until you then have 88 total uncovered non-mine tiles.

Then, all the remaining tiles are auto-flagged and you win instantly.

This saves a lot of time!


Have fun!
