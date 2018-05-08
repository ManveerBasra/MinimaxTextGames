"""
Module for Node Object
"""
from typing import List, Any
from game_state import GameState


class Node:
    """
    Represent a Current_State object with more attributes for use in iterative
    minimax strategy in strategy.py

    Attributes:
        current_state - GameState object
        children - Node children
        score - current score
        move - move applied to reach current_state
    """
    current_state: GameState
    children: List['Node']
    score: int
    move: str

    def __init__(self, current_state: GameState, move: str) -> None:
        """ Initialize a new Node

        >>> cs = Node(GameState(True), 'A')
        >>> cs.children
        []
        >>> cs.score is None
        True
        """
        self.current_state, self.move = current_state, move
        self.children = []
        self.score = None

    def __str__(self) -> str:
        """
        Return a string representation of self

        >>> print(Node(GameState(True), 'A'))
        (P1's Turn: True, Children: [], Score: None, Move: A)
        """
        return "(P1's Turn: {}, Children: {}, Score: {}, Move: {})".format(
            self.current_state.p1_turn,
            self.children,
            self.score,
            self.move
        )

    def __eq__(self, other: Any) -> bool:
        """ Return whether self is equivalent to other

        >>> cs1 = Node(GameState(True), 'A')
        >>> cs2 = Node(GameState(True), 'B')
        >>> cs1 == cs1
        True
        >>> cs1 == cs2
        False
        >>> cs1 == 'A'
        False
        """
        return (type(self) == type(other)
                and self.current_state == other.current_state
                and self.children == other.children
                and self.move == other.move
                and self.score == other.score)
