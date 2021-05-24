# Author      : Ethan Rietz
# Date        : 2021-05-24
# Description : Contains a class called KubaGame for playing a game of Kuba

class KubaGame:
    def __init__(self, player1_info, player2_info):
        self._p1_name = player1_info[0]
        self._p1_color = player1_info[1]
        self._p2_name = player2_info[0]
        self._p2_color = player2_info[2]
        self._turn = None

    def get_current_turn(self):
        return self._turn

    def make_move(self, player_name, coordinates, direction):
        pass

    def get_winner(self):
        pass

    def get_captured(self, player_name):
        pass

    def get_marble(self, coordinates):
        pass

    def get_marble_count(self):
        pass
