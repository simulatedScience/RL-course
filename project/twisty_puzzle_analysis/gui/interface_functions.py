"""
interface methods
"""
import time
import vpython as vpy
from interaction_modules.colored_text import colored_text
# from interaction_modules.methods import *


def interface_import(filepath, history_dict, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    """
    import puzzle from geogebra file and save information in 'history_dict'
    """
    try:
        puzzle.import_puzzle(filepath)
        print(f"successfully imported {colored(filepath, arg_color)}")
    except ValueError:
        print(f"{colored('Error:', error_color)} The path must lead to a .ggb file including the file ending.")
    except FileNotFoundError:
        print(f"{colored('Error:', error_color)} Invalid file path, try again.")


def interface_snap(shape, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    if not shape in ['r', 'c', 's', 'reset', 'cube', 'sphere']:
        print(f"{colored('Error:', error_color)} Invalid shape specified. Try {colored('cube', command_color)}, {colored('sphere', command_color)} or {colored('reset', command_color)}")
    if not puzzle.vpy_objects == []:
        puzzle.snap(shape)
    else:
        print(f"{colored('Error:', error_color)} use {colored('import', command_color)} before snapping")


def interface_newmove(movename, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    if len(movename) == 0 or ' ' in movename:
        print(
            f"{colored('Error:', error_color)} Movename cannot be empty or include a space.")
        return
    puzzle.newmove(movename)


def interface_endmove(puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    puzzle.end_movecreation(arg_color=arg_color)


def interface_move(movename, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    try:
        puzzle.perform_move(movename)
    except KeyError:
        print(f"{colored('Error:', error_color)} move '{colored(movename, arg_color)}' does not exist yet.\
 Create a move using {colored('newmove', command_color)}.")


def interface_printmove(movename, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    try:
        puzzle.print_move(movename, arg_color=arg_color)
    except KeyError:
        print(f"{colored('Error:', error_color)} move '{colored(movename, arg_color)}' does not exist yet. Create a move using {colored('newmove', command_color)}.")


def interface_savepuzzle(puzzlename, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    try:
        if not ' ' in puzzlename:
            puzzle.save_puzzle(puzzlename)
            print(f"saved puzzle as {colored(puzzlename, arg_color)}")
        else:
            raise ValueError("invalid puzzle name")
    except:
        print(f"{colored('Error:', error_color)} invalid puzzle name. Name must not include spaces or other invalid characters for filenames.")


def interface_loadpuzzle(puzzlename, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    """
    load a puzzle 'puzzlename' from 'puzzles/[puzzlename]/puzzle_definition.xml' and
        save information in history_dict
    """
    try:
        puzzle.load_puzzle(puzzlename)
    except FileNotFoundError:
        print(f"{colored('Errod:', error_color)} Puzzle file does not exist yet. Create necessary files with {colored('savepuzzle', command_color)}.")


def interface_listmoves(puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    puzzle.listmoves(arg_color=arg_color)


def interface_rename(user_input, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    """
    renames the move given in user_input

    inputs:
    -------
        user_input - (str) - two movenames, old and new seperated by a space
    """
    old_name, new_name = user_input.split(" ")
    try:
        puzzle.rename(old_name, new_name)
    except KeyError:
        print(f"{colored('Error:', error_color)} Move {colored(old_name, arg_color)} does not exist.")


def interface_delmove(move_name, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    """
    deletes the given move from the given puzzle object
    """
    try:
        puzzle.del_move(move_name)
        print(f"delted the move {colored(movename, arg_color)}.")
    except KeyError:
        print(f"{colored('Error:', error_color)} Move {colored(move_name, arg_color)} does not exist.")


def interface_sleeptime(sleep_time, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    """
    updates the sleep time in the active puzzle
    """
    try:
        puzzle.sleep_time = float(sleep_time)
    except:
        print(f"{colored('Error:', error_color)} Given time is not a float.")


def interface_scramble(max_moves, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    """
    scrambles the given puzzle
    """
    try:
        puzzle.scramble(max_moves=int(max_moves), arg_color=arg_color)
    except:
        puzzle.scramble(arg_color=arg_color)


def interface_reset(puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    """
    reset puzzle to a solved state
    """
    puzzle.reset_to_solved()