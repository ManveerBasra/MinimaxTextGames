"""
Module for StonehengeGame and StonehengeState
"""
import copy
from typing import Dict, List, Any
from game import Game
from game_state import GameState

# For board initialization
ALPHABET = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

# For doctests
IDEAL_BOARD_SIZE_1 = ('      @   @\n' +
                      '     /   /\n' +
                      '@ - A - B\n' +
                      '     \\ / \\\n' +
                      '  @ - C   @\n' +
                      '       \\  \n        @')
IDEAL_REPR_SIZE_1 = "P1's Turn: True - Board: \n{}".format(IDEAL_BOARD_SIZE_1)


class StonehengeGame(Game):
    """
    Class for 2 player Stonehenge Game

    Attributes:
        p1_starts: whether it's player 1's turn
    """
    p1_starts: bool

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.

        :param p1_starts: A boolean representing whether Player 1 is the first
                          to make a move.
        """
        board_size = int(input("Enter the size of the board: "))

        # Add rows of stonehenge board to board
        board = []
        char_count = 0
        for i in range(2, board_size + 2):
            board.append([ALPHABET[ch]
                          for ch in range(char_count, char_count + i)])
            char_count += i

            # Add last row
            if i == board_size + 1:
                board.append([ALPHABET[ch]
                              for ch in range(char_count, char_count + i - 1)])

        # Keep track of ley line markers
        ley_markers = {
            'h': ['@'] * (board_size + 1),
            'du': ['@'] * (board_size + 1),
            'dd': ['@'] * (board_size + 1)
        }

        board_data = {
            'board': board,
            'ley_markers': ley_markers
        }
        self.current_state = StonehengeState(p1_starts, board_data)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        instructions = "Players take turns claiming cells. When a player " + \
            "captures at least half of the cells in a ley-line, then the " + \
            "player captures that ley-line. The first player to capture at" + \
            "least half of the ley-lines is the winner. A ley-line, once " + \
            "claimed, cannot be taken by the other player."
        return instructions

    def is_over(self, state: 'StonehengeState') -> bool:
        """
        Return whether or not this game is over.
        """
        over = False

        # For each token, check whether their count in ley-line markers is at
        # least half
        for token in ['1', '2']:
            occurr = 0
            total_leys = 0
            for key in state.board_data['ley_markers'].keys():
                ley = state.board_data['ley_markers'][key]
                occurr += ley.count(token)
                total_leys += len(ley)

            if not over and (occurr / total_leys) >= 0.5:
                over = True

        return over

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        token = '1' if player == 'p1' else '2'

        occurr = 0
        total_leys = 0

        # If player's token count in ley-line markers is at least half they've
        # won
        for key in self.current_state.board_data['ley_markers'].keys():
            ley = self.current_state.board_data['ley_markers'][key]
            occurr += ley.count(token)
            total_leys += len(ley)

        return ((occurr / total_leys) >= 0.5
                and self.is_over(self.current_state))

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return an invalid move.
        """
        if (not string.isalpha()) or len(string) != 1:
            return '-1'
        return string.upper()


class StonehengeState(GameState):
    """
    The state of stonehenge game at a certain point in time.

    Attributes:
        board_data: data about the current game board
    """
    board_data: Dict[str, Any]

    def __init__(self, is_p1_turn: bool, board_data: Dict[str, Any]) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        >>> ss = StonehengeState(True, {})
        >>> ss.p1_turn
        True
        >>> ss.board_data
        {}
        """
        super().__init__(is_p1_turn)
        self.board_data = board_data

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.

        >>> board_data = {
        ...     'board': [['A', 'B'], ['C']],
        ...     'ley_markers': {
        ...         'h': ['@', '@'], 'du': ['@', '@'], 'dd': ['@', '@']}}
        >>> str(StonehengeState(True, board_data)) == IDEAL_BOARD_SIZE_1
        True
        """
        board = self.board_data['board']
        ley_markers = self.board_data['ley_markers']
        board_size = len(board)
        output = ''

        # Add initial ley_line markers
        output += '  ' * (board_size + 1) \
                  + '%s   %s\n' % (ley_markers['du'][0], ley_markers['du'][1])
        output += '  ' * board_size + ' /   /\n'

        for i in range(board_size):
            # All but the last row have decreasing leading spaces
            if i == board_size - 1:
                output += '  '
            else:
                output += '  ' * (board_size - 2 - i)

            # Add row
            output += '%s - %s' % (ley_markers['h'][i], ' - '.join(board[i]))

            # Add ley line markers depending on row
            if i < board_size - 2:
                output += '   %s\n' % ley_markers['du'][i + 2]
            elif i == board_size - 1:
                output += '   %s\n' % ley_markers['dd'][board_size - 1]
            else:
                output += '\n'

            # Add connector lines depending on row
            if i < board_size - 2:
                output += '  ' * (board_size - 1 - i) \
                        + ' / \\' * len(board[i]) + ' /\n'
            elif i == board_size - 2:
                output += '  ' * 2 + ' \\ /' * (board_size - 1) + ' \\\n'
            else:
                output += '  ' * 3 + ' \\  ' * (board_size - 1) + '\n' \
                        + '  ' * 3 + '  %s' % '   '.join(ley_markers['dd'][:-1])

        return output

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves that can be applied to this state.

        >>> board_data = {
        ...     'board': [['A', 'B'], ['C']],
        ...     'ley_markers': {
        ...         'h': ['@', '@'], 'du': ['@', '@'], 'dd': ['@', '@']}}
        >>> StonehengeState(True, board_data).get_possible_moves()
        ['A', 'B', 'C']
        """
        moves = []

        if self.is_over():
            return moves

        # Add all cells that are characters
        for row in self.board_data['board']:
            for cell in row:
                if cell.isalpha():
                    moves.append(cell)

        return moves

    def make_move(self, move: str) -> "StonehengeState":
        """
        Return the GameState that results from applying move to this GameState.

        >>> board_data = {
        ...     'board': [['A', 'B'], ['C']],
        ...     'ley_markers': {
        ...         'h': ['@', '@'], 'du': ['@', '@'], 'dd': ['@', '@']}}
        >>> new_state = StonehengeState(True, board_data).make_move('A')
        >>> new_board_data = {
        ...     'board': [['1', 'B'], ['C']],
        ...     'ley_markers': {
        ...         'h': ['1', '@'], 'du': ['1', '@'], 'dd': ['1', '@']}}
        >>> new_state.board_data == new_board_data
        True
        """
        # Make a copy of current board_data
        board_data = copy.deepcopy(self.board_data)

        # Set intermediate variables
        board = board_data['board']
        ley_markers = board_data['ley_markers']
        board_size = len(board)

        token = '1' if self.p1_turn else '2'

        # Update board with move
        for i in range(board_size):
            for k in range(len(board[i])):
                if board[i][k] == move:
                    board[i][k] = token

        # Get leys from board
        leys = self.get_leys(board)

        # Check if current_player has claimed any new leys
        for ley_m in ['h', 'du', 'dd']:
            for i in range(board_size):
                ley = leys[ley_m][i]
                if (ley.count(token) / len(ley)) >= 0.5 \
                        and ley_markers[ley_m][i] == '@':
                    ley_markers[ley_m][i] = token

        board_data['board'] = board
        board_data['ley_markers'] = ley_markers
        new_state = StonehengeState(not self.p1_turn, board_data)

        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).

        >>> board_data = {
        ...     'board': [['A', 'B'], ['C']],
        ...     'ley_markers': {
        ...         'h': ['@', '@'], 'du': ['@', '@'], 'dd': ['@', '@']}}
        >>> StonehengeState(True, board_data).__repr__() == IDEAL_REPR_SIZE_1
        True
        """
        return "P1's Turn: {} - Board: \n{}".format(self.p1_turn,
                                                    self.__str__())

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        >>> board_data = {
        ...     'board': [['A', 'B'], ['C']],
        ...     'ley_markers': {
        ...         'h': ['@', '@'], 'du': ['@', '@'], 'dd': ['@', '@']}}
        >>> StonehengeState(True, board_data).rough_outcome()
        1
        """
        # Set some intermediate variables
        player = self.get_current_player_name()
        opponent = 'p2' if player == 'p1' else 'p1'
        loss_possible = True

        # Handle case where state is over
        if self.is_over():
            if self.is_winner(player):
                return 1
            elif self.is_winner(opponent):
                return -1
            return 0

        # Check for guaranteed win/loss case
        for move in self.get_possible_moves():
            new_state = self.make_move(move)
            # If player can win from any move from the current state, ro is WIN
            if new_state.is_winner(player):
                return self.WIN

            # If the opponent can win from any move player makes, ro is LOSE
            if not any(new_state.make_move(next_move).is_winner(opponent)
                       for next_move in new_state.get_possible_moves()):
                loss_possible = False

        if loss_possible:
            return self.LOSE

        # Get how many leys each player has captured
        player_leys = 0
        opponent_leys = 0
        total_leys = 0
        for key in self.board_data['ley_markers'].keys():
            ley = self.board_data['ley_markers'][key]
            player_leys += ley.count(player[1:])
            opponent_leys += ley.count(player[1:])
            total_leys += len(ley)

        return (player_leys - opponent_leys) / (total_leys / 2)

    def is_over(self) -> bool:
        """
        Return whether or not this game is over.

        >>> board_data = {
        ...     'board': [['A', 'B'], ['C']],
        ...     'ley_markers': {
        ...         'h': ['@', '@'], 'du': ['@', '@'], 'dd': ['@', '@']}}
        >>> StonehengeState(True, board_data).is_over()
        False
        """
        over = False
        for token in ['1', '2']:
            occurr = 0
            total_leys = 0
            for key in self.board_data['ley_markers'].keys():
                ley = self.board_data['ley_markers'][key]
                occurr += ley.count(token)
                total_leys += len(ley)

            if not over and (occurr / total_leys) >= 0.5:
                over = True

        return over

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.

        >>> board_data = {
        ...     'board': [['A', 'B'], ['C']],
        ...     'ley_markers': {
        ...         'h': ['@', '@'], 'du': ['@', '@'], 'dd': ['@', '@']}}
        >>> StonehengeState(True, board_data).is_winner('p1')
        False
        """
        token = '1' if player == 'p1' else '2'

        occurr = 0
        total_leys = 0
        for key in self.board_data['ley_markers'].keys():
            ley = self.board_data['ley_markers'][key]
            occurr += ley.count(token)
            total_leys += len(ley)

        return ((occurr / total_leys) >= 0.5
                and self.is_over())

    @staticmethod
    def get_leys(board: List[List[str]]) -> Dict[str, List]:
        """
        Return a dictionary of leys from board

        >>> return_leys = {'h': [['A', 'B'], ['C']], 'du': [['A'], ['B', 'C']],
        ...                'dd': [['A', 'C'], ['B']]}
        >>> StonehengeState.get_leys([['A', 'B'], ['C']]) == return_leys
        True
        """
        board_size = len(board)

        # Form a couple of empty lists to add to when getting leys from board
        leys = {
            'h': [[] for _ in range(board_size)],
            'du': [[] for _ in range(board_size)],
            'dd': [[] for _ in range(board_size)]
        }

        # Get leys from board
        for i in range(board_size):
            leys['h'][i].extend(board[i])
            for k in range(len(board[i])):
                if i != board_size - 1:
                    leys['du'][k].append(board[i][k])
                    leys['dd'][board_size - 2 - i + k].append(board[i][k])
                else:
                    leys['du'][k + 1].append(board[i][k])
                    leys['dd'][board_size - 1 - i + k].append(board[i][k])

        return leys
