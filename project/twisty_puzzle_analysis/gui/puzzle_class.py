"""
a class for storing information about twisty puzzles
"""
import vpython as vpy


class twisty_puzzle():
    def __init__(self):
        self.moves = []
        self.COM = COM                         # vpython vector - center of mass of 3d points
        self.POINT_POSITIONS = POINT_POSITIONS # list of vpython vectors - correct position of 3d points
        self.DEFAULT_POSITIONS = [vpy.vec(vec) for vec in POINT_POSITIONS]
        self.current_state = [] # list of vpython objects - current state of the puzzle in animation
        self.movecreator_mode = False


    def perform_move(self, move):
        """
        perform the given move on the puzzle self
        """


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


    def scramble(self, max_moves=30):
        """
        scramble the puzzle by applying [max_moves] random moves

        inputs:
        -------
            max_moves - (int) - the number of random moves
        """


    def newmove(self, movename):
        """
        start defining a new move with the given name, enable movecreator mode

        inputs:
        -------
            movename - (str) - the name of the new move
                must not include spaces
        """


    def end_movecreation(self):
        """
        exit movecreator mode and save the last move
        """


    def listmoves(self):
        """
        print all availiable moves for this puzzle
        if every move has an inverse: don't print the inverse moves
        """


    def rename_move(self, old_name, new_name):
        """
        rename the move [old_name] to [new_name]
        if the move [new_name] already exists, a warning could be useful

        inputs:
        -------
            old_name - (str) - name of the move to be renamed
            new_name - (str) - new name for that move
        """


    def del_move(self, move_name):
        """
        delete the move [move_name]

        inputs:
        -------
            move_name - (str) - name of the move to be deleted
        """

    def save_puzzle(self, puzzle_name=None):
        """
        save the puzzle under the given name.
        if puzzle_name is None, try to save it as self.puzzle_name

        inputs:
        -------
            puzzle_name - (str) - name of the puzzle
        """