"""
functions for the catching of command line arguments
"""

import toml


def save_args(args):
    """Saves command line arguments to CmdArgs.toml"""
    with open("CmdArgs.toml", "w") as toml_file:
        toml.dump(args, toml_file)


def load_args():
    """Loads command line arguments from CmdArgs.toml"""
    with open("CmdArgs.toml") as toml_file:
        args = toml.load(toml_file)
    for key,value in args.items():
        print(key, "=>", value)
    return args