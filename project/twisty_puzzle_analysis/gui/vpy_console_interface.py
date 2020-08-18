"""
This module provides an interface to control the vpython animation via the terminal

it should be able to...
    - import a .ggb file                # done (running import twice is still broken)
    - show the points defined there     # done (except cone option)
    - allow visual input of cycles      # done
    - allow visual input of moves       # done
    - provide output option for moves   # done
    - perform animated moves            # done
"""
from os import _exit as exit
from interaction_modules.colored_text import colored_text
from interface_functions import *
from puzzle_class import Twisty_Puzzle


def main_interaction():
    """
    user interaction via the terminal
    allowing different commands and executing them accordingly

    inputs: (via terminal)
    -------
        - 'import' [filepath]          - load file from 'filepath' and show points in vpython
        - 'snap' [mode]                - snap points to shape, 'mode' = 'cube'='c' or 'sphere'='s'
        - 'newmove' [movename]         - create new move with name 'movename'
        - 'endmove'                    - exit move creator mode and save current move to some file
        - 'move' [movename]            - perform the mive with the given 'movename'
        - 'listmoves'                  - list all saved moves
        - 'printmove' [movename]       - print all cycles of the given move
        - 'help'                       - print this overview
        - 'exit'                       - close program
        - 'savepuzzle' [puzzlename]    - save the current puzzle into a file 'puzzledefinition.xml' or for now .txt
        - 'loadpuzzle' [puzzlename]       - load puzzle from a given file
        - 'rename' [oldname] [newname] - rename a move
        - 'delmove' [movename]         - delete the given move
        - 'closepuzzle'                - close the current puzzle animation
    """
    command_color = "#ff8800"
    argument_color = "#5588ff"
    user_input = ""

    puzzle = Twisty_Puzzle()
    n = 0

    while user_input.lower() != "exit":
        print()
        print(
            f"type in a command: ('{colored_text('help', command_color)}' to list all commands)")
        user_input = input(">>> ")
        if user_input.lower() == "exit":
            exit(0)
        command_dict = {"help": interface_help,
                        "import": interface_import,
                        "snap": interface_snap,
                        "newmove": interface_newmove,
                        "endmove": interface_endmove,
                        "move": interface_move,
                        "printmove": interface_printmove,
                        "listmoves": interface_listmoves,
                        "savepuzzle": interface_savepuzzle,
                        "loadpuzzle": interface_loadpuzzle,
                        "rename": interface_rename,
                        "delmove": interface_delmove,
                        "closepuzzle": interface_closepuzzle}

        if validate_command(command_dict, user_input):
            run_command(command_dict, user_input, puzzle,
                        command_color, argument_color)


def validate_command(command_dict, user_input):
    """
    check whether the given input is a valid command

    inputs:
    -------
        user_input - (str) - any string, only valid commands cause action

    returns:
    --------
        (bool) - whether or not the input is a valid command
    """
    input_list = user_input.split(" ")

    if not input_list[0].lower() in command_dict.keys():
        return False
    return True


def run_command(command_dict, user_input, puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    """
    execute a given command

    inputs:
    -------
        user_input - (str) - string representing a valid command

    returns:
    --------
        None
    """
    command = user_input.split(" ")[0]

    if command in ["import", "snap", "newmove", "move", "printmove", "savepuzzle", "loadpuzzle", "rename", "delmove"]:
        try:
            user_arguments = user_input[len(command)+1:]
            print(
                f"executing {colored(command, command_color)} {colored(user_arguments, arg_color)} ...")
        except IndexError:
            print(
                f"{colored('Error:', error_color)} {colored(command, command_color)} requires additional options.")
        command_dict[command](user_arguments,
                              puzzle,
                              command_color=command_color,
                              arg_color=arg_color,
                              error_color=error_color)
    else:
        command_dict[command](puzzle,
                              command_color=command_color,
                              arg_color=arg_color,
                              error_color=error_color)


def interface_closepuzzle(puzzle, command_color="#ff8800", arg_color="#5588ff", error_color="#ff0000"):
    """
    close the current puzzle and reset history_dict
    """
    save_answer = ""
    while not save_answer in ["y", "n"]:
        save_answer = input("save current puzzle before closing? (y/n) ")
        if save_answer.lower() == "y":
            if puzzle.PUZZLE_NAME == None:
                puzzlename = ' '
                while ' ' in puzzlename:
                    puzzlename = input("Enter a name without spaces to save the puzzle: ")
            puzzle.save_puzzle(puzzlename)
            print(f"saved puzzle as {colored(puzzlename, arg_color)}")
        try:
            puzzle.canvas.delete()
        except:
            pass
        main_interaction()


if __name__ == "__main__":
    main_interaction()
