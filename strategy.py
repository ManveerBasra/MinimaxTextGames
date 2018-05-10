"""
A module for strategies.
"""
from typing import Union, Dict
from game_state import GameState
from game import Game
from node import Node


def interactive_strategy(game: Game) -> Union[str, int]:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Game) -> Union[str, int]:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def recursive_minimax_strategy(game: Game) -> Union[str, int]:
    """
    Return a move by recursively looking at possible moves from the
    current_state and returning one that provides the best outcome.
    """
    current_state = game.current_state

    scores = []
    possible_moves = current_state.get_possible_moves()

    # Get scores for all current possible moves
    for move in possible_moves:
        new_state = current_state.make_move(move)
        scores.append(recursive_minimax_helper(game, new_state) * -1)

    # Reset game's current_state to state before move-checking
    game.current_state = current_state

    # Return the move that resulted in the highest score
    return possible_moves[scores.index(max(scores))]


def recursive_minimax_helper(game: Game, state: GameState) -> int:
    """
    Helper function for recursive_minimax_strategy. Recursively checks
    possible_moves for each state and returns the highest score for the current
    state.
    """
    game.current_state = state
    player = state.get_current_player_name()
    opponent = 'p1' if player == 'p2' else 'p2'

    # If game is over, return score based on who won
    if game.is_over(state):
        if game.is_winner(player):
            return 1
        elif game.is_winner(opponent):
            return -1
        return 0

    scores = []
    possible_moves = state.get_possible_moves()

    # Get scores for all current possible moves
    for move in possible_moves:
        new_state = state.make_move(move)
        scores.append(recursive_minimax_helper(game, new_state) * -1)

    # Return the highest resulting score
    return max(scores)


def iterative_minimax_strategy(game: Game) -> Union[str, int]:
    """
    Return a move by iteratively looking at possible moves from the
    current_state and returning one that provides the best outcome.
    """
    current_state = game.current_state

    # Create a stack to hold Nodes for iterative minimax
    stack = [Node(current_state, None)]

    best_move = None

    # Keep updating and getting scores while the stack isn't empty
    while len(stack) != 0:
        # Get item at top of stack and set some intermediate variables
        top = stack.pop()
        player = top.current_state.get_current_player_name()
        opponent = 'p1' if player == 'p2' else 'p2'
        game.current_state = top.current_state

        # Set score based on who won if game is over
        if game.is_over(top.current_state):
            if game.is_winner(player):
                top.score = 1
            elif game.is_winner(opponent):
                top.score = -1
            else:
                top.score = 0
        elif top.children == []:
            # Get children and add them to the stack
            new_nodes = []
            for move in top.current_state.get_possible_moves():
                new_nodes.append(Node(
                    top.current_state.make_move(move), move))

            top.children = new_nodes
            stack.append(top)
            for node in new_nodes:
                stack.append(node)
        else:
            # Get scores for all of top's children
            scores = []
            for child in top.children:
                scores.append(child.score * -1)

            # Set top's score to the max of it's children's scores * -1
            top.score = max(scores)

            # If the stack is empty then this is the last item and thus the
            # original current_state, so get the best_move
            if len(stack) == 0:
                best_move = top.children[scores.index(max(scores))].move

    # Reset game's current_state to state before move-checking
    game.current_state = current_state

    return best_move


def memoization_minimax_strategy(game: Game) -> Union[str, int]:
    """
    Return a move by recursively looking at possible moves from the
    current_state and returning one that provides the best outcome.

    Uses a dictionary to keep track of seen states and skips state if it's
    already in dictionary
    """
    current_state = game.current_state

    scores = []
    possible_moves = current_state.get_possible_moves()
    seen_states = {}

    # Get scores for all current possible moves
    for move in possible_moves:
        new_state = current_state.make_move(move)
        new_state_repr = new_state.__repr__

        # Check if new_state has already been seen, if so get its score, else
        # do a recursive call
        if new_state_repr in seen_states.keys():
            score = seen_states[new_state_repr]
        else:
            score = \
                memoization_minimax_helper(game, new_state, seen_states) * -1

        scores.append(score)
        seen_states[new_state_repr] = score

    # Reset game's current_state to state before move-checking
    game.current_state = current_state

    # Return the move that resulted in the highest score
    return possible_moves[scores.index(max(scores))]


def memoization_minimax_helper(game: Game, state: GameState,
                               seen_states: Dict[str, int]) -> int:
    """
    Helper function for recursive_minimax_strategy. Recursively checks
    possible_moves for each state and returns the highest score for the current
    state.

    Uses a dictionary to keep track of seen states and skips state if it's
    already in dictionary
    """
    game.current_state = state
    player = state.get_current_player_name()
    opponent = 'p1' if player == 'p2' else 'p2'

    # If game is over, return score based on who won
    if game.is_over(state):
        if game.is_winner(player):
            return 1
        elif game.is_winner(opponent):
            return -1
        return 0

    scores = []
    possible_moves = state.get_possible_moves()

    # Get scores for all current possible moves
    for move in possible_moves:
        new_state = state.make_move(move)
        new_state_repr = new_state.__repr__

        # Check if new_state has already been seen, if so get its score, else
        # do a recursive call
        if new_state_repr in seen_states.keys():
            score = seen_states[new_state_repr]
        else:
            score = \
                memoization_minimax_helper(game, new_state, seen_states) * -1

        scores.append(score)
        seen_states[new_state_repr] = score

    # Return the highest resulting score
    return max(scores)
