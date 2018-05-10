"""
Module for SubtractSquareGame and SubtractSquareState
"""
from typing import Any
from game import Game
from game_state import GameState


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

    def is_over(self, state: 'SubtractSquareState') -> bool:
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


class SubtractSquareState(GameState):
    """
    The state of a game at a certain point in time.
    """

    def __init__(self, is_p1_turn: bool, current_total: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        """
        super().__init__(is_p1_turn)
        self.current_total = current_total

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        return "Current total: {}".format(self.current_total)

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        moves = []
        for i in range(1, self.current_total + 1):
            if i ** 2 <= self.current_total:
                moves.append(i ** 2)

        return moves

    def make_move(self, move: Any) -> "SubtractSquareState":
        """
        Return the GameState that results from applying move to this GameState.
        """
        if type(move) == str:
            move = int(move)

        new_state = SubtractSquareState(not self.p1_turn,
                                        self.current_total - move)
        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return "P1's Turn: {} - Total: {}".format(self.p1_turn,
                                                  self.current_total)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        if is_pos_square(self.current_total):
            return self.WIN
        elif all([is_pos_square(self.current_total - n ** 2)
                  for n in range(1, self.current_total + 1)
                  if n ** 2 < self.current_total]):
            return self.LOSE

        return self.DRAW


def is_pos_square(n: int) -> bool:
    """
    Return whether n is a positive perfect square

    >>> is_pos_square(5)
    False
    >>> is_pos_square(9)
    True
    """
    return 0 < n and (round(n ** 0.5) ** 2 == n)
