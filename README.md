## Software Engineering Final Project - Online Rummikub Game
_____
### Run with:
`python main.py`

### Testing:
Included are various key binds that are very helpful for testing:
- E: This acts as end turn and saves the tiles where they are on the board.
- S: This acts as a step back or rebase, and sends the tiles back to where they were 1 "turn" before.
- Q: This acts as the checker and checks if you made a valid move.
  - Note: A turn is only valid (saves the board) if every tile on the board is in a valid collection (set or run)
  - This acts on a "turn by turn" basis.
- D: This adds one tile to your dock acting as a draw. 
  - Note: you cannot draw more tiles than you already have even if some of them are on the board.
  - To draw more place them on the board in a valid way and press Q or place them on the board in any assortment and press E.
- W: This takes you to the win view (WIP)
- L: This takes you to the loss view (WIP)

### Necessary packages:
- pyarcade