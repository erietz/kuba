# Author      : Ethan Rietz
# Date        : 2021-05-24
# Description : Contains a class called KubaGame for playing a game of Kuba

class bcolors:
    CBLACKBG  = '\33[40m'
    CWHITEBG  = '\33[47m'
    CREDBG    = '\33[41m'
    ENDC = '\033[0m'

class KubaGame:
    def __init__(self, player1_info, player2_info):
        self._p1 = {
            'name': player1_info[0],
            'color': player1_info[1],
            'captured_count': 0
        }
        self._p2 = {
            'name': player2_info[0],
            'color': player2_info[1],
            'captured_count': 0
        }
        self._turn = None
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
                    new_row.append(bcolors.CWHITEBG + 'W' + bcolors.ENDC)
                elif column == 'B':
                    new_row.append(bcolors.CBLACKBG + 'B' + bcolors.ENDC)
                elif column == 'R':
                    new_row.append(bcolors.CREDBG + 'R' + bcolors.ENDC)
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
        players_turn = self.get_current_turn()
        if players_turn is None:
            players_turn = player_name
        elif players_turn != player_name:
            return False

        if player_name == self._p1['name']:
            self._turn = self._p2['name']
        elif player_name == self._p2['name']:
            self._turn = self._p1['name']

        return True

    def get_winner(self):
        pass

    def get_captured(self, player_name):
        if player_name == self._p1.get('name'):
            return self._p1.get('captured_count')
        elif player_name == self._p2.get('name'):
            return self._p2.get('captured_count')

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
    game = KubaGame(('Jim', 'W'), ('Bob', 'B'))
    game._display_board(colored=True)
    print('marble count', game.get_marble_count())
