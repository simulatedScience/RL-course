"""
a class for storing information about twisty puzzles
"""
import time
import vpython as vpy
from twisty_puzzle_model import scramble, perform_action

class twisty_puzzle():
    def __init__(self):
        self.puzzle_name = None

        self.POINT_POSITIONS = [] # list of vpython vectors - correct position of 3d points
        self.SOLVED_STATE = [] # list of vpython vectors - correct colors of 3d points
        self.POINT_INFO_DICTS = []
        self.COM = None # vpython vector - center of mass of 3d points
        self.vpy_objects = [] # list of vpython objects - current state of the puzzle in animation
        self.animation_speed = 5e-3
        self.canvas = None
        self.moves = dict() # dcitionary containing all moves for the puzzle
        self.movecreator_mode = False
        # self.POINT_POSITIONS = [point["coords"] for point in point_dicts]
        # self.SOLVED_STATE = [point["color"] for point in point_dicts]


    def snap(self, shape):
        """
        snap points to a given shape

        inputs:
        -------
            shape - (str) - the shape
                should be:
                    'cube' or 'c' for a cube
                    'sphere' or 's' for a sphere
                    'reset' or 'r' to reset to default positions
        """
        try:
            self.snap_obj.visible = False
        except AttributeError:
            pass
        except NameError: # define self.snap_obj
            self.snap_obj = None
        if shape == "r" or shape == "reset":
            self.reset_to_solved()
        elif shape == "c" or shape =="cube":
            if not isinstance(self.snap_obj, vpy.box):
                self.snap_obj = snap_to_cube(self.vpy_objects, show_cube=True)
        elif shape == "s" or shape =="sphere":
            if not isinstance(self.snap_obj, vpy.sphere):
                self.snap_obj = snap_to_sphere(self.vpy_objects, show_cube=True)


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


    def perform_move(self, moves):
        """
        perform the given move on the puzzle self
        if multiple moves are given, they are all executed

        inputs:
        -------
            moves - (str) - 

        """
        if ' ' in moves:
            for move in moves.split(' '):
                self.perform_move(move)
                time.sleep(100*self.sleep_time)
        else:
            # make_move also permutes the vpy_objects
            make_move(self.vpy_objects,
                      self.moves[moves],
                      self.POINT_POSITIONS,
                      self.COM,
                      sleep_time=self.sleep_time,
                      anim_steps=anim_steps)


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
        self.active_move_name = movename
        self.active_move_cycles = []
        self.active_arrows = []
        self.on_click_function = bind_click(self.canvas,
                                            self.active_cycle_list,
                                            self.vpy_objects,
                                            self.active_arrow)


    def end_movecreation(self):
        """
        exit movecreator mode and save the last move
        """
        self.movecreator_mode = False
        try:
            for arrow in self.active_arrows: #hide all arrows showing the move
                arrow.visible = False
            del(self.active_arrows)
        except NameError:
            pass
        self.moves[self.active_move_name] = deepcopy(self.active_move_cycles)
        # prepare for adding inverse move:
        self.inverse_cycles(self.active_move_cycles)
        self.active_move_name = self.active_move_name[:-1] \
            if "'" == self.active_move_name[-1] else self.active_move_name + "'"
        self.end_movecreation() # add inverse move


    def inverse_cycles(self, cycle_list):
        """
        inverts all cycles in [cycle_list]
        """
        for cycle in cycle_list:
            cycle.reverse()


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


    def save_puzzle(self, puzzle_name):
        """
        save the puzzle under the given name.
        if puzzle_name is None, try to save it as self.puzzle_name

        inputs:
        -------
            puzzle_name - (str) - name of the puzzle
                must not include spaces or other invalid characters for filenames
        """
        self.puzzle_name = puzzle_name
        save_to_xml(self)


    def load_puzzle(self, puzzle_name):
        """
        load the given puzzle from a .xml file

        inputs:
        -------
            puzzle_name - (str) - name of the puzzle
                must not include spaces or other invalid characters for filenames
        """
        # TODO

    
    def import_puzzle(self, filepath):
        """
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


