# Funktionen um ein Tik Tac Toe Feld auszugeben
def print_field(field):
    """
    print the given field
    inputs:
        field - (list) or (tuple) - list of 9 ints in (0,1,2)
            0 is an empty field
    """
    print_list = convert_field(field)
    for i in range(3):
        print("-"*13)
        print("| {} | {} | {} |".format( *print_list[3*i:3*i+3] ))
    print("-"*13)


def convert_field(field):
    """
    prepare field for printing by replacing characters
    inputs:
        field - (list) - list of 9 ints in (0,1,2)
            0 is an empty field
    returns:
        (list) - list of "o", "x" and " " representing the field
    """
    print_list = []
    for elem in field:
        if elem == 1:
            print_list.append("o")
        elif elem == 2:
            print_list.append("x")
        else:
            print_list.append(" ")
    return print_list


# Funktionen um mögliche Aktionen sowie das Spielende zu bestimmen.
from math import sqrt
def game_ended(field, get_winner=False):
    """
    checks whether or not a ttt-game has ended
    inputs:
        field - (list) - list (must not be a tuple) with integer entries 0, 1 and 2
    ouputs:
        if get_winner is False:
            (bool) - whether or not a ttt-game has ended
        else:
            (int) - sign of the winner. 0 if it is a draw
    """
    n = int(sqrt(len(field)))
    rows = [field[n*i:n*i+n] for i in range(n)] #get all rows of the field
    columns = [field[i::n] for i in range(n)]   #get all columns of the field
    diagonals = [field[::n+1], field[n-1:n**2-2:n-1]] #get both diagonals of the field

    win_lists = rows + columns + diagonals
    
    if not get_winner:
        if [1]*n in win_lists or [2]*n in win_lists:
            return True
        if not 0 in field:
            return True
        return False
    else:
        if [1]*n in win_lists:
            return 1
        if [2]*n in win_lists:
            return 2
        if not 0 in field:
            return 0


def get_actions(field):
    """
    calculate all possible actions for the given field
    inputs:
        field - (list) - list of 9 ints in (0,1,2)
            0 is an empty field
    returns:
        (list) - list of possible actions as list indices
    """
    actions = []
    if 0 in field and not game_ended(field):
        for i, elem in enumerate(field):
            if elem == 0:
                actions.append(i)
    return actions