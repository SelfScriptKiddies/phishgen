import argparse

from pathlib import Path

from phishgen.logger import get_logger
from phishgen.config import MACRO_DOTM_PATH
from phishgen.macros.macro_modifier import replace_source_code

log = get_logger(__name__)


def macro(args: argparse.Namespace):
    """
    Function for mode 'macro'.
    Modifies source code in .dotm file.

    :param args: arguments from command line
    """
    source = args.source
    source_code = None
    if not source:
        log.fatal("No source code provided!")
        exit(1)

    if Path(source).is_file():
        try:
            with open(source, 'r', encoding='utf-8') as f:
                source_code = f.read()
            log.debug(f"Loaded code for macro from '{source}'.")
        except Exception as e:
            log.fatal(f"Error when reading file '{source}': {e}")
            exit(1)

    if type(source) == str:
        source_code = source
        log.debug(f"Using provided string with code: {source}")

    if source_code is None:
        log.error(f"Something wrong with your code...")
        exit(1)

    replace_source_code(MACRO_DOTM_PATH, source_code, args.output_file)

    log.debug(f"Mode macro")


def add_subparser(subparsers):
    """
    Argument subparser for mode macro

    :param subparsers: parent parser for adding child
    :return:
    """
    parser_macro = subparsers.add_parser(
        'macro',
        help="modify macro in .dotm file"
    )
    parser_macro.add_argument(
        '-o',
        '--output',
        help="Filepath to new file. Otherwise it will be original file + suffix '_patched'",
        type=Path,
        default=None,
        dest="output_file"
    )
    group = parser_macro.add_mutually_exclusive_group()
    group.add_argument(
        '-s',
        '--string',
        type=str,
        help="macro code in string",
        dest="source"
    )
    group.add_argument(
        '-f',
        '--file',
        type=Path,
        help="file with macro code inside",
        dest="source"
    )
    parser_macro.set_defaults(
        func=macro)
