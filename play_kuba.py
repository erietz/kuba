from KubaGame import KubaGame

p1_name = input('Player 1 Name: ').strip()
p1_color = input('Player 1 color (W or B): ').upper()
p2_name = input('Player 2 Name: ').strip()
p2_color = input('Player 2 color (W or B): ').upper()

game = KubaGame((p1_name, p1_color), (p2_name, p2_color))
game._display_board(colored=True)

def get_name():
    name = input('name: ').strip()
    names = (p1_name, p2_name)
    if name not in names:
        print('name should be one of ', *names)
        return get_name()
    return name

def get_coordinates():
    try:
        coords = input('row col: ').strip().split()
        if len(coords) != 2:
            print('Coordinates should be: row col (separated by space)')
            return get_coordinates()
        else:
            coords = [int(i) for i in coords]
    except ValueError:
        print('Coordinates not integers')
        return get_coordinates()
    return coords

def get_direction():
    direction = input('direction: ').strip().upper()
    directions = ('R', 'L', 'F', 'B')
    if direction not in directions:
        print('Valid directions are', *directions)
        return get_direction()
    else:
        return direction


captured_sum = 0
while game.get_winner() == None:
        name = get_name()
        coord = get_coordinates()
        direction = get_direction()
        move = game.make_move(name, coord, direction)
        if not move:
            print('move not valid')
        else:
            game._display_board(colored=True)
            p1_score = game.get_captured(p1_name)
            p2_score = game.get_captured(p2_name)
            new_sum = p1_score + p2_score
            if  new_sum > captured_sum:
                print(p1_name, 'has captured', p1_score, 'balls')
                print(p2_name, 'has captured', p2_score, 'balls')
                captured_sum = new_sum

print(game.get_winner(), 'is victorious and won the game!!!!')
