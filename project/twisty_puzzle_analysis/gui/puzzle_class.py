"""
a class for storing information about twisty puzzles
"""
import time
from copy import deepcopy
import vpython as vpy

import ggb_import.ggb_to_vpy as ggb_vpy

from interaction_modules.colored_text import colored_text as colored
from interaction_modules.save_to_xml import save_to_xml
from interaction_modules.load_from_xml import load_puzzle

from vpython_modules.create_canvas import create_canvas
from vpython_modules.vpy_rotation import get_com, make_move
from vpython_modules.cycle_input import bind_click

from shape_snapping import snap_to_cube, snap_to_sphere

from ai_modules.twisty_puzzle_model import scramble, perform_action


class Twisty_Puzzle():
    def __init__(self):
        self.PUZZLE_NAME = None

        self.POINT_POSITIONS = [] # list of vpython vectors - correct position of 3d points
        self.SOLVED_STATE = [] # list of vpython vectors - correct colors of 3d points
        self.POINT_INFO_DICTS = []
        self.COM = None # vpython vector - center of mass of 3d points
        self.vpy_objects = [] # list of vpython objects - current state of the puzzle in animation
        self.sleep_time = 5e-3
        self.canvas = None
        self.moves = dict() # dcitionary containing all moves for the puzzle
        self.movecreator_mode = False


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
            self.snap_obj = None
        except NameError: # define self.snap_obj
            self.snap_obj = None
        if shape == "r" or shape == "reset":
            self.reset_point_positions()
        elif shape == "c" or shape =="cube":
            if not isinstance(self.snap_obj, vpy.box):
                self.snap_obj = snap_to_cube(self.vpy_objects, show_cube=True)
        elif shape == "s" or shape =="sphere":
            if not isinstance(self.snap_obj, vpy.sphere):
                self.snap_obj = snap_to_sphere(self.vpy_objects, show_sphere=True)
        self.POINT_POSITIONS = [vpy.vec(obj.pos) for obj in self.vpy_objects]


    def reset_point_positions(self):
        """
        resets the point positions to their initial position
        """
        for point_dict, obj in zip(self.POINT_INFO_DICTS, self.vpy_objects):
            obj.pos = point_dict["coords"]
        try:
            self.snap_obj.visible = False
            self.snap_obj = None
        except:
            self.snap_obj = None


    def scramble(self, max_moves=30):
        """
        scramble the puzzle by applying [max_moves] random moves

        inputs:
        -------
            max_moves - (int) - the number of random moves
        """
        scramble_hist = scramble(self.current_state, max_moves=max_moves, arg_color="#0066ff")
        print("scrambled with the following moves:\n{colored(scramble_hist, arg_color)}")
        self.perform_move(scramble_hist)


    def reset_to_solved(self):
        """
        resets the puzzle colors to a solved state
        """
        for color, obj in zip(self.SOLVED_STATE, self.vpy_objects):
            obj.color = color


    def perform_move(self, moves):
        """
        perform the given move on the puzzle self
        if multiple moves are given, they are all executed

        inputs:
        -------
            moves - (str) - a single move or several seperated by spaces
        """
        if ' ' in moves:
            for move in moves.split(' '):
                self.perform_move(move)
                time.sleep(50*self.sleep_time)
        else:
            # make_move also permutes the vpy_objects
            make_move(self.vpy_objects,
                      self.moves[moves],
                      self.POINT_POSITIONS,
                      self.COM,
                      sleep_time=self.sleep_time,
                      anim_steps=45)


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
                                            self.active_move_cycles,
                                            self.vpy_objects,
                                            self.active_arrows)


    def end_movecreation(self, arg_color="#0066ff", add_inverse=True):
        """
        exit movecreator mode and save the last move
        """
        self.movecreator_mode = False
        try:
            for arrow in self.active_arrows: #hide all arrows showing the move
                arrow.visible = False
            del(self.active_arrows)
        except AttributeError:
            pass
        self.moves[self.active_move_name] = deepcopy(self.active_move_cycles)

        print(f"saved move {colored(self.active_move_name, arg_color)}.")
        if add_inverse:
            # prepare for adding inverse move:
            self.inverse_cycles(self.active_move_cycles)
            self.active_move_name = self.active_move_name[:-1] \
                if "'" == self.active_move_name[-1] else self.active_move_name + "'"
            self.end_movecreation(arg_color=arg_color, add_inverse=False) # add inverse move


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
        self.PUZZLE_NAME = puzzle_name
        save_to_xml(self)


    def load_puzzle(self, puzzle_name):
        """
        load the given puzzle from a .xml file
        set all important class variables accordingly

        inputs:
        -------
            puzzle_name - (str) - name of the puzzle
                must not include spaces or other invalid characters for filenames
        """
        self.POINT_INFO_DICTS, self.moves = load_puzzle(puzzle_name)
        self.canvas = create_canvas()
        self.vpy_objects = ggb_vpy.draw_points(self.POINT_INFO_DICTS)

        self.POINT_POSITIONS = [point["coords"] for point in self.POINT_INFO_DICTS]
        self.SOLVED_STATE = [point["vpy_color"] for point in self.POINT_INFO_DICTS]
        self.COM = get_com(self.vpy_objects)
        self.PUZZLE_NAME = puzzle_name

    
    def import_puzzle(self, filepath):
        """
        imports a puzzle from a given .ggb (Geogebra) file
        The puzzle will automatically be centered around the origin.

        inputs:
        -------
            filepath - (str) - path to a .ggb file represeting a puzzle
        """
        try:
            self.POINT_INFO_DICTS = ggb_vpy.get_point_dicts(filepath)
        except FileNotFoundError:
            self.POINT_INFO_DICTS = ggb_vpy.get_point_dicts(filepath+".ggb")
        self.COM = get_com(self.vpy_objects)
        self.canvas = create_canvas()
        # draw_points also converts coords in dictionaries to vpython vectors
        self.vpy_objects = ggb_vpy.draw_points(self.POINT_INFO_DICTS)

        if not self.COM.abs < 1e-10:
            for point_dict, obj in zip(self.POINT_INFO_DICTS, self.vpy_objects):
                obj.pos -= self.COM
                point_dict["coords"] -= self.COM

        self.POINT_POSITIONS = [point["coords"] for point in self.POINT_INFO_DICTS]
        self.SOLVED_STATE = [point["color"] for point in self.POINT_INFO_DICTS]


    def listmoves(self, arg_color="#0066ff"):
        """
        print all availiable moves for this puzzle
        if every move has an inverse: don't print the inverse moves
        """
        print(f"the puzzle {colored(self.PUZZLE_NAME, arg_color)} is defined with the following moves:")
        for movename in self.moves.keys():
            self.print_move(movename,
                           arg_color=arg_color)


    def print_move(self, move_name, arg_color="#0066ff"):
        """
        print the given move
        """
        print(f"{colored(move_name, arg_color)} is defined by the cycles", self.moves[move_name])


