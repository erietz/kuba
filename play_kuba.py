from KubaGame import KubaGame

p1_name = input('Player 1 Name: ').strip()
p1_color = input('Player 1 color: ').upper()
p2_name = input('Player 2 Name: ').strip()
p2_color = input('Player 2 color: ').upper()

game = KubaGame((p1_name, p1_color), (p2_name, p2_color))
game._display_board(colored=True)

while game.get_winner() == None:
    try:
        name = input('name: ').strip()
        coord = input('coordinates: ')
        coord = [int(i) for i in coord.split()]
        direction = input('direction: ').upper()
        move = game.make_move(name, coord, direction)
        if not move:
            print('move not valid')
        else:
            game._display_board(colored=True)
    except IndexError or ValueError or KeyError:
        print('you are an idiot..... try again please.....')
        pass
print(game.get_winner(), 'is the shit and won the game!!!!')
