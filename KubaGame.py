# Author      : Ethan Rietz
# Date        : 2021-05-24
# Description : Contains a class called KubaGame for playing a game of Kuba

# TODO: write unittests for each method 
# TODO: check all requirements in README
# TODO: add all docstrings

class KubaPlayer:
    def __init__(self, player_info):
        self._name = player_info[0]
        self._color = player_info[1]
        self._captured_count = 0

    def get_name(self):
        return self._name

    def get_color(self):
        return self._color

    def get_captured_count(self):
        return self._captured_count

    def increment_captured_count(self):
        self._captured_count += 1


class KubaBoard:
    def __init__(self, clone=None):
        self._BLACKBG  = '\33[40m'
        self._WHITEBG  = '\33[47m'
        self._REDBG    = '\33[41m'
        self._ENDC     = '\033[0m'
        if clone is None:
            self.board = [
                ['W', 'W', ' ', ' ', ' ', 'B', 'B'],
                ['W', 'W', ' ', 'R', ' ', 'B', 'B'],
                [' ', ' ', 'R', 'R', 'R', ' ', ' '],
                [' ', 'R', 'R', 'R', 'R', 'R', ' '],
                [' ', ' ', 'R', 'R', 'R', ' ', ' '],
                ['B', 'B', ' ', 'R', ' ', 'W', 'W'],
                ['B', 'B', ' ', ' ', ' ', 'W', 'W'],
            ]
        else:
            self.clone_board(clone)

    def clone_board(self, board):
        new_board = []
        for row in board:
            new_row = []
            for marble in row:
                new_row.append(marble)
            new_board.append(new_row)
        self.board = new_board

    def get_marble(self, coordinates):
        marble = self.board[coordinates[0]][coordinates[1]]
        if marble == ' ':
            return 'X'
        else:
            return marble

    def get_marble_count(self):
        """
        Returns tuple (W, B, R) of marble counts on the board
        """
        W, B, R = 0, 0, 0
        for row in self.board:
            W += row.count('W')
            B += row.count('B')
            R += row.count('R')
        return W, B, R

    def display(self, colored=False):
        """
        Prints out the 7x7 board with the rows and column numbers displayed on
        the left and top respectfully. If colored is set to True, the board is
        displayed in color. Note: this requires a terminal that excepts the
        escape codes profided by the Colors class.
        """
        if not colored:
            i = 0
            print(' ', *list(range(7)), sep=' ')
            for row in self.board:
                print(i, end=' ')
                for column in row:
                    print(column, end=' ')
                i +=1
                print()
            return

        new_board = []
        for row in self.board:
            new_row = []
            for column in row:
                if column == 'W':
                    new_row.append(self._WHITEBG + 'W' + self._ENDC)
                elif column == 'B':
                    new_row.append(self._BLACKBG + 'B' + self._ENDC)
                elif column == 'R':
                    new_row.append(self._REDBG + 'R' + self._ENDC)
                else:
                    new_row.append(' ')
            new_board.append(new_row)

        print('  ', '-'*16)
        print(' ', '|', *list(range(7)), '|', sep=' ')
        print('  ', '-'*16)
        i = 0
        for row in new_board:
            print(i, '|', end=' ')
            for column in row:
                print(column, end=' ')
            i += 1
            print('|', end=' ')
            print()
        print('  ', '-'*16)


class KubaGame:
    """
    Represents a game of Kuba. This class has data members to represent the
    board and players for a Kuba game. This class also contains all of the
    methods required to make moves, keep track of the current state, and play
    the game from start to finish.
    """
    def __init__(self, player1_info, player2_info):
        """
        Creates a new game of Kuba with a 7x7 board set up with marbles in the
        correct locations. Two players are created using the information
        provided by the arguments player1_info and player2_info.

        :param player1_info: tuple (color, name) of the players color which can
                             be either 'W' of 'B' and their name. Both are strings.

        :param player2_info: tuple (color, name) same info but for player 2.
        """
        self._player_info = {
            player1_info[0]: KubaPlayer(player1_info),
            player2_info[0]: KubaPlayer(player2_info)
        }
        self._turn = None       # Name of player whose turn it is
        self._winner = None     # Name of player who wins the game
        self._board = KubaBoard()
        self._old_board_states = [KubaBoard().board]

        # TODO: delete me
        self._debug = False     # Will print board after each move if True
        self._debug_color = False   # Will print board in color if True

    def get_current_turn(self):
        """Returns the players name whose turn it is"""
        return self._turn

    def _validate_move(self, player, row, col, direction):
        if self._turn != player.get_name(): # Trying to make_move out of turn
            return False
        if self._winner != None:            # A player has already won
            return False
        for coordinate in (row, col):      # The coordinates are out of range
            if coordinate not in range(7):
                return False
        # Can only push using players balls
        if self._board.board[row][col] != player.get_color():
            return False

        # There is a ball in front of the ball trying to be pushed
        if direction == 'R':
            # Trying to push off ones own ball
            if self._board.board[row][6] == player.get_color():
                return False
            # Ball is blocked by another ball
            if col in range(1, 7) and self._board.board[row][col- 1] != ' ':
                return False
        elif direction == 'L':
            # Trying to push off ones own ball
            if self._board.board[row][0] == player.get_color():
                return False
            # Ball is blocked by another ball
            if col in range(6) and self._board.board[row][col + 1] != ' ':
                return False
        elif direction == 'B':
            # Trying to push off ones own ball
            if self._board.board[6][col] == player.get_color():
                return False
            # Ball is blocked by another ball
            if row in range(1, 7) and self._board.board[row - 1][col] != ' ':
                return False
        elif direction == 'F':
            # Trying to push off ones own ball
            if self._board.board[0][col] == player.get_color():
                return False
            # Ball is blocked by another ball
            if row in range(6) and self._board.board[row + 1][col] != ' ':
                return False

        return True

    def _move_right(self, board, row, col, player):
        board = KubaBoard(board).board
        try:
            last_marble = board[row].index(' ', col + 1) - 1
        except ValueError:
            last_marble = 5
            #last_marble = 6
            # leads to crazy result if pushing off index 6 using index 5

        board[row][col+1:last_marble+2] = board[row][col:last_marble+1]
        board[row][col] = ' '
        return board

    def _move_backward(self, board, row, col, player):
        tmp_board = self._transpose_matrix(board)
        tmp_board = self._move_right(tmp_board, col, row, player)
        tmp_board = self._transpose_matrix(tmp_board)
        return tmp_board

    def _move_left(self, board, row, col, player):
        board = KubaBoard(board).board
        rev_col = 7 - col - 1
        try:
            last = board[row][::-1].index(' ', rev_col + 1) - 1
            last = 7 - last - 1     # want index of list not reversed list
        except ValueError:
            last = 1

        board[row][last-1:col] = board[row][last:col+1]
        board[row][col] = ' '
        return board

    def _move_forward(self, board, row, col, player):
        tmp_board = self._transpose_matrix(board)
        tmp_board = self._move_left(tmp_board, col, row, player)
        tmp_board = self._transpose_matrix(tmp_board)
        return tmp_board

    def make_move(self, player_name, coordinates, direction):
        """
        :param player_name: Name of the player used to initially create the
                            object

        :param coordinates: Tuple of coordinates of the board (row, col) of the
                            marble to push. Indices row and col range from 0 to
                            7.

        :param direction:   Direction to push the balls. Valid options are 'L'
                            (left), 'R' (right), 'F' (forward), and 'B' (back).

        :return Boolean:    True if the move is made and False if the move is
                            invalid (i.e. make_move did not do anything).
        """
        if self._turn is None:                      # First move of the game
            self._turn = player_name
        row, col = coordinates[0], coordinates[1]   # To reduce typing and brain power
        player = self._player_info[player_name]
        #opponent = self._player_info[self._get_opponent_name(player_name)]

        move_is_valid = self._validate_move(player, row, col, direction)
        if not move_is_valid:
            return False

        red_count = self._board.get_marble_count()[2]

        if direction == 'R':
            new_board = self._move_right(self._board.board, row, col, player)
        elif direction == 'L':
            new_board = self._move_left(self._board.board, row, col, player)
        elif direction == 'B':
            new_board = self._move_backward(self._board.board, row, col, player)
        elif direction == 'F':
            new_board = self._move_forward(self._board.board, row, col, player)

        if new_board == self._old_board_states[-1]:
            return False
        else:
            self._old_board_states.append(self._board.board)
            self._board = KubaBoard(new_board)

        if red_count > self._board.get_marble_count()[2]:
            player.increment_captured_count()

        self._update_winner_state()

        #self._turn = opponent.get_name()
        self._turn = self._get_opponent_name(player_name)

        if self._debug:
            print('Player:', player_name)
            print('Coordinates:', row, col)
            print('Direction:', direction)
            self._board.display(colored=self._debug_color)

        return True

    def _transpose_matrix(self, matrix):
        """
        Takes an iterable of iterables and returns a new iterable of iterables
        where the rows are now the columns. This is like the transpose of a
        matrix.
        """
        new_matrix = []
        for j in range(len(matrix[0])):
            new_row = []
            for i in range(len(matrix)):
                new_row.append(matrix[i][j])
            new_matrix.append(new_row)
        return new_matrix

    def _get_opponent_name(self, player_name):
        """Returns the name of the player whose turn it is NOT"""
        players = list(self._player_info.keys())
        index = players.index(player_name)
        if index == 0:
            return players[1]
        else:
            return players[0]

    def _update_winner_state(self):
        """
        Updates the winner data member if the player makes a move which results
        in capturing 7 balls or knocking all of their opponents balls off of
        the board.
        """
        marble_count = self.get_marble_count()
        if self._player_info[self._turn].get_captured_count() == 7:
            self._winner = self._turn
        elif marble_count[0] == 0 or marble_count[1] == 0:
            self._winner = self._turn

    def get_winner(self):
        """Returns the name of the winner of the game"""
        return self._winner

    def get_captured(self, player_name):
        """Returns the count of the red marbles captured by player_name"""
        return self._player_info[player_name].get_captured_count()

    def get_marble(self, coordinates):
        """
        Returns the color of the marble located at coordinates
        :param coordinates: tuple (row, col) where row and column are indices 
                            between 0 and 6
        """
        return self._board.get_marble(coordinates)

    def get_marble_count(self):
        """
        Returns tuple (W, B, R) of marble counts on the board
        """
        return self._board.get_marble_count()
