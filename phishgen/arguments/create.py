import os
import argparse

from phishgen.config import ROOT_PATH
from phishgen.logger import get_logger
from phishgen.patcher.docx_patch import copy_template

log = get_logger(__name__)


def create(args: argparse.Namespace):
    """
    Function for mode 'macro'.
    Modifies source code in .dotm file.

    :param args: arguments from command line
    """
    mode = args.create_mode

    if mode not in ['fulldoc', 'empty', 'full', 'malware']:
        log.fatal(f"Mode not available: {mode}")
        exit(1)

    if mode == 'fulldoc':
        copy_template(ROOT_PATH / r"resources/examples/resume_document.docx", args.working_directory)
        log.info(f"Copied full document to '{args.working_directory}'. You can inject your code!")
        return

    if mode == 'empty':
        copy_template(ROOT_PATH / r"resources/examples/harmless_pattern.dotx", args.working_directory)
        log.info(f"Copied empty pattern to '{args.working_directory}'. Create docx document with it and inject")
        return

    if mode == 'full':
        copy_template(ROOT_PATH / r"resources/examples/full_resume_pattern.dotx", args.working_directory)
        log.info(f"Copied pattern with full resume to '{args.working_directory}'. Create docx document with it and "
                 f"inject")
        return

    if mode == 'macro':
        copy_template(ROOT_PATH / r"resources/examples/macro.dotm", args.working_directory)
        log.info(f"Copied macro file macro.dotm from examples to {args.working_directory}")
        return


def add_subparser(subparsers):
    """
    Argument subparser for mode create

    :param subparsers: parent parser for adding child
    :return:
    """
    parser_create = subparsers.add_parser(
        'create',
        help="Create document with specific format (.docx, .dotx)"
    )
    parser_create.add_argument(
        '-d',
        '--directory',
        help="working directory",
        default=os.getcwd(),
        dest="working_directory",
    )
    parser_create.add_argument(
        'create_mode',
        type=str,
        choices=['fulldoc', 'empty', 'full'],
        help="Mode: 'fulldoc', 'empty' or 'full'."
    )
    parser_create.set_defaults(func=create)
