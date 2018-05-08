"""
An implementation of Subtract Square.
"""
from game import Game
from subtract_square_state import SubtractSquareState


class SubtractSquareGame(Game):
    """
    Abstract class for a game to be played with two players.
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """
        count = int(input("Enter the number to subtract from: "))
        self.current_state = SubtractSquareState(p1_starts, count)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        instructions = "Players take turns subtracting square numbers from" + \
            " the starting number. The winner is the person who subtracts to 0."
        return instructions

    def is_over(self, state: SubtractSquareState) -> bool:
        """
        Return whether or not this game is over.

        :return: True if the game is over, False otherwise.
        :rtype: bool
        """
        return state.current_total == 0

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, string: str) -> int:
        """
        Return the move that string represents. If string is not a move,
        return an invalid move.
        """
        if not string.strip().isdigit():
            return -1

        return int(string.strip())
