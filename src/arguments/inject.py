import os
import argparse

from pathlib import Path
from src.patcher.docx_patch import patch_macro_path
from src.logger import get_logger

log = get_logger(__name__)


def inject(args: argparse.Namespace):
    """
    Function for mode 'inject'.
    Adds specified macro to document

    :param args: arguments to program from command line
    """
    log.info("Mode inject")
    patch_macro_path(args.document, args.macro, args.output_file)
    log.debug(f"Successfully injected macro {args.macro} to {args.document}")


def add_subparser(subparsers):
    """
    Argument subparser for mode inject

    :param subparsers: parent parser for adding child
    :return:
    """
    parser_inject = subparsers.add_parser(
        'inject',
        help="inject macro in document"
    )
    parser_inject.add_argument(
        'document',
        type=Path,
        help="document path to inject"
    )
    parser_inject.add_argument(
        'macro',
        type=Path,
        help="injecting macro URL/filepath"
    )
    parser_inject.add_argument(
        '-d',
        '--directory',
        help="working directory",
        default=os.getcwd(),
        dest="working_directory",
    )
    parser_inject.add_argument(
        '-o',
        '--output',
        help="Filepath to new file. Otherwise it will be original file + suffix '_patched'",
        type=Path,
        default=None,
        dest="output_file"
    )
    parser_inject.set_defaults(func=inject)  # inject(arguments.document, arguments.macro)