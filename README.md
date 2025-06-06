# Othello
Niko Bransfield  
Oregon State University  
CS261 Portfolio Project  
Completed 2023-06-11

## Overview
A program that allows two players to play text-based [Othello](https://en.wikipedia.org/wiki/Reversi). In this game, two players take turns placing their colored pieces on an 8x8 board. The objective is to capture the opponent's pieces and have the majority of your own pieces on the board at the end of the game.

## Rules
- The game is played on an 8x8 board
- Players take turns placing their pieces on the board, starting with black.
- To capture pieces, a player must place their piece adjacent to an opponent's piece, forming a straight line of adjacent pieces (horizontal, vertical, or diagonal) with their piece at each end.
- Multiple chains/directions of pieces can be captured all at once in a single move, and the captured pieces are converted to the capturing player's color
- The game starts with four pieces placed in the middle of the board, forming a square with same-colored pieces on a diagonal
- Once a piece is placed, it cannot be moved to a new square.
- If a player cannot make a valid move(a capturing move), their turn passes to the other player.
- The game ends when neither player can move, and the player with the most pieces on the board wins. A tie occurs if both players have the same number of pieces.

## Game Board
The game board is represented by a 10x10 grid.
- Edges: `*`
- Black Pieces: `X`
- White Pieces: `O`
- Empty Squares: `.`

## Usage
For testing purposes, game methods are able to be called alone from `Othello.py` like in the examples below.
```
game = Othello()
game.create_player("Helen", "white")
game.create_player("Leo", "black")
game.make_move("black", (5,6))
game.print_board()
game.play_game("white", (7,6))
game.print_board()
```
```
game = Othello()
game.print_board()
game.create_player("Helen", "white")
game.create_player("Leo", "black")
game.play_game("black", (6,5))
game.print_board()
game.play_game("white", (6,6))
game.print_board()
```
A full game can be played more naturally using `OthelloPlayInTerminal.py`. This feature was not part of the assignment specification but felt appropriate to add.
