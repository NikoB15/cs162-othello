# Author: Niko Bransfield
# GitHub Username: NikoB15
# Date: 2023-05-27
# Description: A script that can run an Othello game in the terminal. (Added for fun.)

from Othello import Othello


def main():
    """
    Starts a game of Othello that can be played using the terminal.
    """
    black_player_name = input("Enter the name of the person who will play Black ('X'): ")
    white_player_name = input("Enter the name of the person who will play White ('O'): ")

    game = Othello()
    game.create_player(black_player_name, 'black')
    game.create_player(white_player_name, 'white')

    input("\nPress ENTER when you are ready to begin.\n")
    goto_next_turn(game, "white", (black_player_name, white_player_name))
    play_game_by_turn(game, (black_player_name, white_player_name))


def play_game_by_turn(game: Othello, players: tuple[str, str]):
    """
    The main loop of the game. Controls player input and starting and ending turns.
    """
    turn_color = "black"
    # Turn loop
    while True:
        # Check whether current player has any valid moves. If not, skip their turn.
        # We don't need to check for two skips in a row here. game.play_game does that already.
        if should_skip_turn(game, turn_color):
            opponent = players[0] if turn_color == "white" else players[1]
            print(f"{opponent} has no available moves!")
            turn_color = goto_next_turn(game, turn_color, players, print_board=False)
            continue  # Move to next turn

        # Player move validation loop
        while True:
            valid_moves = game.return_available_positions(turn_color)
            position = get_player_move(valid_moves)  # Ask player to input a move
            result = game.play_game(turn_color, position)
            if result == "Invalid move":  # If the player isn't allowed to make that move
                continue  # Give player input prompt again
            if result == "Game over":  # If the game is over
                game_over(game)
                return  # Exit script
            break  # If the player successfully made the move, exit loop

        # End of turn
        turn_color = goto_next_turn(game, turn_color, players)


def should_skip_turn(game: Othello, turn_color: str) -> bool:
    """
    Returns True if the current color has no valid moves, otherwise False.
    """
    valid_moves = game.return_available_positions(turn_color)
    return len(valid_moves) == 0


def goto_next_turn(game: Othello, turn_color: str, players: tuple[str, str], print_board=True) -> str:
    """
    Prepares the next turn of the game. Returns the next turn color.
    """
    turn_color = "white" if turn_color == "black" else "black"
    turn_symbol = 'X' if turn_color == "black" else 'O'
    current_player_name = players[0] if turn_color == "black" else players[1]
    if print_board:
        game.print_board()
    print(f"It's your turn, {current_player_name}! ({turn_symbol})")
    return turn_color


def get_player_move(valid_moves: list[tuple[int, int]]) -> tuple[int, int]:
    """
    A validation loop for player turn input. Prompts the player to input coordinates to make their next move.
    If the player gives invalid input, it will ask again until they give valid input.
    """
    # Input validation loop
    while True:
        print(f"\nHere are your valid moves: {valid_moves}.")
        move = input(f"Enter the move you'd like to make (Example: \"3,4\" means row 3, column 4): ")

        try:
            position = [int(x) for x in move.split(",")]  # Turn input into a list of ints
        except ValueError:  # If the player didn't input integers
            print(f"\nInvalid input: \"{move}\". Expected two integers separated by a comma.")
            continue

        if len(position) != 2:  # If the player input more than 2 integers
            print(f"\nInvalid input: \"{move}\". Expected two integers separated by a comma.")
            continue

        print("\n")  # Text spacer
        return position[0], position[1]


def game_over(game: Othello):
    """
    Ends the game.
    """
    game.print_board()
    input("\nPress ENTER to exit the script.")


if __name__ == '__main__':
    main()
