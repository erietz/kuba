# Author      : Ethan Rietz
# Date        : 2021-06-09
# Description : 
#   Contains a class named KubaGame for playing a slightly modified version of
#   the game of Kuba. For instructions on how to play, see
#   https://sites.google.com/site/boardandpieces/list-of-games/kuba or watch
#   this video: https://www.youtube.com/watch?v=XglqkfzsXYc to learn how to
#   play the game.  KubaGame is composed of the KubaPlayer and KubaBoard
#   classes and differs from the original board game by not allowing players to
#   continue making moves after pushing off a marble.

class KubaPlayer:
    """
    Represents one of the two players in a game of Kuba. Has data members to
    hold the players name, color, and red marble captured count. This class
    also contains a method to increase the captured count by one marble.
    """
    def __init__(self, player_info):
        """
        Creates a player using player_info and initializes their captured count
        to zero.

        :param player_info: A tuple (name, color) used to identify the player.
                            Name and color are both strings and the color can
                            either be white (W) or black (B).
        """
        self._name = player_info[0]
        self._color = player_info[1]
        self._captured_count = 0

    def get_name(self):
        """Returns the name of the player"""
        return self._name

    def get_color(self):
        """Returns the color of the player"""
        return self._color

    def get_captured_count(self):
        """Returns the number of red marbles captured by the player"""
        return self._captured_count

    def increment_captured_count(self):
        """Increases the number of red marbles captured by the player by 1"""
        self._captured_count += 1


class KubaBoard:
    """
    Represents a 7x7 board that a game of Kuba is played on. This class has
    methods to initialize its board from clone operation, get the marble at a
    specifed coordinate, get a count of all the marbles on the board, and to
    display the board with or without color.
    """
    def __init__(self, clone=None):
        """
        Creates a new KubaBoard.

        If the clone argument is left out, the board will be initialized like a
        traditional game of Kuba with 8 white and black marbles and 13 red
        marbles. If clone is provided, it should be a 7x7 grid (list of lists)
        of marbles ('W', 'B', 'R', and ' ' for empty positions).
        """
        # for printing the board in color
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
        """
        Sets the board data member to board by copying the list of lists.

        :param board: 7x7 grid (list of lists) of marbles ('W', 'B', 'R', and
                      ' ' for empty positions).
        """
        new_board = []
        for row in board:
            new_row = []
            for marble in row:
                new_row.append(marble)
            new_board.append(new_row)
        self.board = new_board

    def get_marble(self, coordinates):
        """
        Returns the marble at coordinates

        :param coordinates: A tuple (row, col) of indicis on the board
        """
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
        self._old_board = KubaBoard()

        self._debug = False     # Will print board after each move if True
        self._debug_color = False   # Will print board in color if True

    def get_current_turn(self):
        """Returns the players name whose turn it is"""
        return self._turn

    def _validate_move(self, player, row, col, direction):
        """
        Used internally to check if the move is valid.

        :return Boolean: False if move cannot be made, otherwise True
        """
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
        """
        Used internally to push a row of marbles to the right starting at
        coordinates row and col for a player. If a marble is at row 6, the
        marble will be pushed off of the board. Returns a copy of a board.
        """
        board = KubaBoard(board).board
        try:
            # last = index of last marble being pushed
            last = board[row].index(' ', col + 1) - 1
        except ValueError:
            # If there are no spaces between first marble and end of board, set
            # the last marble to be 5, or the last possible marble that could
            # be pushed.
            last = 5

        board[row][col+1:last+2] = board[row][col:last+1]
        board[row][col] = ' '
        return board

    def _move_backward(self, board, row, col, player):
        """
        Used internally to push a column of marbles backwards. Note: moving
        backwards is exactly the same as moving right but with a transposed
        board and reversing the row and column indices. Returns a copy of a
        board.
        """
        tmp_board = self._transpose_matrix(board)
        tmp_board = self._move_right(tmp_board, col, row, player)
        tmp_board = self._transpose_matrix(tmp_board)
        return tmp_board

    def _move_left(self, board, row, col, player):
        """
        Used internally to push a row of marbles to the left starting at
        coordinates row and col for a player. If a marble is at row 0, the
        marble will be pushed off of the board. Returns a copy of a board.
        """
        board = KubaBoard(board).board
        # Here we are reversing a list and rev_col represents the index of the
        # column after reversing the row. See _move_right if confused.
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
        """
        Used internally to push a column of marbles forwards. Note: moving
        forwards is exactly the same as moving left but with a transposed board
        and reversing the row and column indices. Returns a copy of a board.
        """
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

        if new_board == self._old_board.board:
            return False
        else:
            self._old_board = KubaBoard(self._board.board)
            self._board = KubaBoard(new_board)

        if red_count > self._board.get_marble_count()[2]:
            player.increment_captured_count()

        self._update_winner_state()

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
        """Returns the name of the player who is not player_name"""
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
