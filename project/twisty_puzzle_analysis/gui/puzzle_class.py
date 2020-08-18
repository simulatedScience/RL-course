"""
a class for storing information about twisty puzzles
"""
import time
import vpython as vpy
from twisty_puzzle_model import scramble, perform_action

class twisty_puzzle():
    def __init__(self, point_dicts, name="twisty_puzzle"):
        self.POINT_POSITIONS = [point["coords"] for point in point_dicts] # list of vpython vectors - correct position of 3d points
        self.SOLVED_STATE = [point["color"] for point in point_dicts] # list of vpython vectors - correct colors of 3d points
        self.COM = vpy.vec(0,0,0) # vpython vector - center of mass of 3d points
        self.vpy_objects = [] # list of vpython objects - current state of the puzzle in animation
        self.canvas = None
        self.moves = dict() # dcitionary containing all moves for the puzzle
        self.movecreator_mode = False


    def perform_move(self, moves, sleep_time=0.1):
        """
        perform the given move on the puzzle self
        if multiple moves are given, they are all executed
        """
        if ' ' in moves:
            for move in moves.split(' '):
                self.perform_move(move, sleep_time=sleep_time)
        else:
            # TODO


    def snap(self, shape):
        """
        snap points to a given shape

        inputs:
        -------
            shape - (str) - the shape
                should be:
                    'cube' or 'c' for a cube
                    'sphere' or 's' for a sphere
                    #TODO:
                    'reset' or 'r' to reset to default positions
        """
        try:
            self.snap_obj.visible = False
            del self.snao_obj
        except NameError:
            pass
        if shape == "r" or shape == "reset":
            self.reset_to_solved()
        else:
            self.snap_obj, self.COM = run_snap(shape, self.vpy_objects, prev_shape=self.snap_obj)




    def scramble(self, max_moves=30):
        """
        scramble the puzzle by applying [max_moves] random moves

        inputs:
        -------
            max_moves - (int) - the number of random moves
        """
        scramble_hist = scramble(self.current_state, max_moves=max_moves)
        return scramble_hist


    def reset_to_solved(self):
        """
        resets the puzzle to a solved state
        """
        for color, obj in zip(self.SOLVED_STATE, self.vpy_objects):
            obj.color = color


    def newmove(self, movename):
        """
        start defining a new move with the given name, enable movecreator mode

        inputs:
        -------
            movename - (str) - the name of the new move
                must not include spaces
        """
        if self.movecreator_mode:
            self.end_movecreation(self)
        self.movecreator_mode = True
        # TODO


    def end_movecreation(self):
        """
        exit movecreator mode and save the last move
        """
        self.movecreator_mode = False
        # TODO


    def rename_move(self, old_name, new_name):
        """
        rename the move [old_name] to [new_name]
        if the move [new_name] already exists, a warning could be useful

        inputs:
        -------
            old_name - (str) - name of the move to be renamed
            new_name - (str) - new name for that move
        """
        self.moves[new_name] = self.moves[old_name]
        del(self.moves[old_name])


    def del_move(self, move_name):
        """
        delete the move [move_name]

        inputs:
        -------
            move_name - (str) - name of the move to be deleted
        """
        del(self.moves[move_name])


    def save_puzzle(self, puzzle_name=None):
        """
        save the puzzle under the given name.
        if puzzle_name is None, try to save it as self.puzzle_name

        inputs:
        -------
            puzzle_name - (str) - name of the puzzle
        """
        # TODO


    def listmoves(self, arg_color="#0066ff"):
        """
        print all availiable moves for this puzzle
        if every move has an inverse: don't print the inverse moves
        """
        print(f"the puzzle {colored(self.name, arg_color)} is defined with the following moves:")
        for movename in self.moves.keys():
            self.printmove(movename,
                           history_dict=history_dict,
                           arg_color=arg_color)


    def print_move(self, move_name, arg_color="#0066ff"):
        """
        print the given move
        """
        print(f"{colored(movename, arg_color)} is defined by the cycles", cycle_list)


