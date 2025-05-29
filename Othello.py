# Author: Niko Bransfield
# GitHub Username: NikoB15
# Date: 2023-05-27
# Description: An implementation of the board game "Othello".
#              Othello class: controls logic for making moves and winning the game
#              Player class: represents a player in an Othello game with a name and piece color

class Player:
    """
    Represents a player in an Othello game.
    Used by the player list in the Othello class.
    """

    def __init__(self, name: str, color: str):
        """
        Initializes a new Player object.
        :param name: The name of the player.
        :param color: The player's tile color.
        """
        self._name = name
        self._color = color

    def get_name(self) -> str:
        """
        :return: This player's name
        """
        return self._name

    def get_color(self) -> str:
        """
        :return: This player's tile color
        """
        return self._color


class Othello:
    """
    Represents a game of Othello.
    Contains a list of players and controls the logic for making moves and winning.
    """

    def __init__(self):
        """
        Initializes a new Othello game.
        Sets up a starting board and creates an empty player list.
        """

        # Create the starting board
        self._board = [['*'] * 10] \
                      + [['*'] + ['.'] * 8 + ['*'] for _ in range(8)] \
                      + [['*'] * 10]
        self._board[4][5] = self._board[5][4] = 'X'
        self._board[4][4] = self._board[5][5] = 'O'

        self._players: list[Player] = []

    def get_piece_of_color(self, color: str) -> str:
        """
        :param color: The color to retrieve ("white" or "black")
        :return: The string representing a piece of that color
        """
        return 'X' if color.lower() == "black" else 'O' if color.lower() == "white" else ''

    # We assume this method will only be called when the game ends.
    def get_piece_of_opposite_color(self, color: str) -> str:
        """
        :param color: The color to use ("white" or "black")
        :return: The string representing a piece of the opposite color
        """
        return 'O' if color.lower() == "black" else 'X' if color.lower() == "white" else ''

    def is_valid_color(self, string: str) -> bool:
        """
        Checks whether the given string is a valid color
        :param string: The string to check
        :return: True if the given string is "black" or "white" (case-insensitive), otherwise False
        """
        return string.lower() in ["black", "white"]

    def create_player(self, player_name: str, color: str):
        """
        Adds a new player to this Othello game.
        :param player_name: The name of the player to add
        :param color: The color this player will take ("white" or "black")
        """
        if not self.is_valid_color(color):
            print(f"Invalid color: {color}")
            return

        self._players.append(Player(player_name, color))

    def count_pieces(self, color: str) -> int:
        """
        Counts the number of pieces of the given color that are currently on the board
        :param color: The color to count ("white" or "black")
        :return: The number of pieces of the given color on the board
        """
        if not self.is_valid_color(color):
            print(f"Invalid color: {color}")
            return 0

        own_color = self.get_piece_of_color(color)

        pieces = 0
        for row in self._board:
            pieces += row.count(own_color)
        return pieces

    def return_winner(self) -> str:
        """
        Determines the winner of the game based on the number of pieces each player currently has on the board.
        :return: a message declaring who won and whether the game tied.
        """
        player1_pieces = self.count_pieces(self._players[0].get_color())
        player2_pieces = self.count_pieces(self._players[1].get_color())

        if player1_pieces == player2_pieces:
            return "It's a tie"

        winner = self._players[0] if player1_pieces > player2_pieces else self._players[1]
        return f"Winner is {winner.get_color()} player: {winner.get_name()}"

    def return_available_positions(self, color: str) -> list:
        """
        Calculates every position the current color can make, assuming it's that color's turn.
        :param color: The color to find moves for ("white" or "black")
        :return: A list of valid positions for the current color
        """
        if not self.is_valid_color(color):
            print(f"Invalid color: {color}")
            return []

        valid_positions = []
        for row in range(1, 9):
            for col in range(1, 9):
                if self.is_valid_move(color, (row, col)):
                    valid_positions.append((row, col))
        return valid_positions

    def is_valid_move(self, color: str, position: tuple) -> bool:
        """
        Checks whether putting a piece of the given color at the specified position would be a valid move,
        assuming it's that color's turn.
        :param color: The color of the piece to place ("white" or "black")
        :param position: The position to place the piece
        :return: True if the move is valid, otherwise False
        """
        if not self.is_valid_color(color):
            print(f"Invalid color: {color}")
            return False

        if self._board[position[0]][position[1]] != '.':
            return False

        for direction in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            capturable_positions = self.get_capturable_tiles(color, position, direction)
            if len(capturable_positions) > 0:
                return True
        return False

    def get_capturable_tiles(self, color: str, position: tuple, direction: tuple) -> list:
        """
        Determines which tiles a piece would capture in the given direction if placed at the given position.
        :param color: The color of the piece to place ("white" or "black")
        :param position: The position to place the piece
        :param direction: A tuple representing one step forward in a particular direction.
                          For example, (1, 1) represents "down and to the right".
        :return: True if the move is valid, otherwise False
        """
        if not self.is_valid_color(color):
            print(f"Invalid color: {color}")
            return []

        own_color = self.get_piece_of_color(color)
        opponent_color = self.get_piece_of_opposite_color(color)

        position = (position[0] + direction[0], position[1] + direction[1])
        opponent_tiles = []

        while self._board[position[0]][position[1]] == opponent_color:
            opponent_tiles.append(position)
            position = (position[0] + direction[0], position[1] + direction[1])

        if self._board[position[0]][position[1]] == own_color:
            return opponent_tiles
        else:
            return []

    # We assume only valid moves will be passed to this method.
    def make_move(self, color: str, position: tuple) -> list:
        """
        Puts a piece of the given color at the specified position and captures enemy pieces appropriately.
        :param color: The color of the piece to place ("white" or "black")
        :param position: The position to place the piece
        :return: The board after placing the piece
        """
        if not self.is_valid_color(color):
            print(f"Invalid color: {color}")
            return self._board

        own_piece = self.get_piece_of_color(color)
        self._board[position[0]][position[1]] = own_piece

        captured_tiles = []
        for direction in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
            captured_tiles += self.get_capturable_tiles(color, position, direction)
        for tile in captured_tiles:
            self._board[tile[0]][tile[1]] = own_piece

        return self._board

    def play_game(self, color: str, position: tuple):
        """
        Attempts to place a piece of the given color at the specified position.
        If the position is valid, places the piece and captures enemy pieces appropriately;
        then prints a "game ended" message if no more moves can be made by either player.
        If the position is invalid, prints an error message and a list of valid moves.
        :param color: The color of the piece to place ("white" or "black")
        :param position: The position to place the piece
        :return: "Invalid move" if the move was invalid; "Game over" if the move caused the game to end; otherwise,
                 returns nothing.
        """
        if not self.is_valid_color(color):
            print(f"Invalid color: {color}")
            return

        opponent_color = 'white' if color == 'black' else 'black'

        valid_moves = self.return_available_positions(color)

        if position not in valid_moves:
            print(f"Invalid move. Here are your valid moves:"
                  f"\n {valid_moves}")
            return "Invalid move"

        else:
            self.make_move(color, position)
            # Check whether the game is over
            opponent_valid_moves = self.return_available_positions(opponent_color)
            own_valid_moves = self.return_available_positions(color)
            if len(opponent_valid_moves) == 0 and len(own_valid_moves) == 0:
                # Game is over
                print(f"\nGAME OVER!"
                      f"\n  * White pieces: {self.count_pieces('white')}"
                      f"\n  * Black pieces: {self.count_pieces('black')}")
                print(f"\n{self.return_winner()}")
                return "Game over"

    def print_board(self):
        """
        Prints out the current game board.
        """
        for row in self._board:
            print(' '.join(row))
