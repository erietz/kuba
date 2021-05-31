# Author      : Ethan Rietz
# Date        : 2021-05-24
# Description : Contains a class called KubaGame for playing a game of Kuba

class Colors:
    BLACKBG  = '\33[40m'
    WHITEBG  = '\33[47m'
    REDBG    = '\33[41m'
    ENDC     = '\033[0m'

class KubaGame:
    def __init__(self, player1_info, player2_info):
        self._player_info = {
            player1_info[0]: {
                'color': player1_info[1],
                'captured_count': 0
            },
            player2_info[0]: {
                'color': player2_info[1],
                'captured_count': 0
            }
        }
        self._turn = None
        self._winner = None
        self._board = [
            ['W', 'W', ' ', ' ', ' ', 'B', 'B'],
            ['W', 'W', ' ', 'R', ' ', 'B', 'B'],
            [' ', ' ', 'R', 'R', 'R', ' ', ' '],
            [' ', 'R', 'R', 'R', 'R', 'R', ' '],
            [' ', ' ', 'R', 'R', 'R', ' ', ' '],
            ['B', 'B', ' ', 'R', ' ', 'W', 'W'],
            ['B', 'B', ' ', ' ', ' ', 'W', 'W'],
        ]

    def _display_board(self, colored=False):
        if not colored:
            for row in self._board:
                for column in row:
                    print(column, end=' ')
                print()
            return

        new_board = []
        for row in self._board:
            new_row = []
            for column in row:
                if column == 'W':
                    new_row.append(Colors.WHITEBG + 'W' + Colors.ENDC)
                elif column == 'B':
                    new_row.append(Colors.BLACKBG + 'B' + Colors.ENDC)
                elif column == 'R':
                    new_row.append(Colors.REDBG + 'R' + Colors.ENDC)
                else:
                    new_row.append(' ')
            new_board.append(new_row)
        for row in new_board:
            for column in row:
                print(column, end=' ')
            print()

    def get_current_turn(self):
        return self._turn

    def make_move(self, player_name, coordinates, direction):
        """
        :param player_name: Name of the player used to initially create the
                            object

        :param coordinates: Tuple of coordinates of the board (x, y) of the
                            marble to push. Indices x and y range from 0 to 7.

        :param direction:   Direction to push the balls. Valid options are 'L'
                            (left), 'R' (right), 'F' (forward), and 'B' (back).

        :return Boolean:    True if the move is made and False if the move is
                            invalid (i.e. make_move did not do anything).
        """
        players_turn = self._turn
        if players_turn is None:    # First move of the game
            players_turn = player_name
        bonus_turn = False          # set to True if a ball is knocked off
        ball_color = self._board[coordinates[0]][coordinates[1]]
        player = self._player_info[player_name]

        # Check to see if the move is valid
        if players_turn != player_name:     # Trying to make_move out of turn
            return False
        if self._winner != None:            # A player has already won
            return False
        for coordinate in coordinates:      # The coordinates are out of range
            if coordinate not in range(7):
                return False
        if ball_color != player['color']:   # Can only push using players balls
            return False

        if direction == 'R':
            pass
        elif direction == 'L':
            pass
        elif direction == 'B':
            pass
        elif direction == 'F':
            pass

        return True

    def get_opponent_name(self, player_name):
        players = list(self._player_info.keys())
        index = players.index(player_name)
        if index == 0:
            return players[1]
        else:
            return players[0]

    def get_winner(self):
        return self._winner

    def get_captured(self, player_name):
        return self._player_info[player_name].get('captured_count')

    def get_marble(self, coordinates):
        marble = self._board[coordinates[0]][coordinates[1]]
        if marble == ' ':
            return 'X'
        else:
            return marble

    def get_marble_count(self):
        W, B, R = 0, 0, 0
        for row in self._board:
            W += row.count('W')
            B += row.count('B')
            R += row.count('R')
        return W, B, R

if __name__ == '__main__':
    game = KubaGame(('ann', 'W'), ('bob', 'B'))
    game._display_board(colored=True)
    print('marble count', game.get_marble_count())
    print(game.make_move('ann', (3, 4), 'R'))
