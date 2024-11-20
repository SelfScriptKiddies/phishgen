import os
import argparse

from pathlib import Path
from src.logger import get_logger
from src.arguments import create, inject

if os.name == 'nt':
    from src.arguments import macro

log = get_logger(__name__)


def validate_directory(path):
    """
    validate directory function

    :param path: path to directory
    :return: path, if it exists.
    :raises argparse.ArgumentTypeError: if directory not valid.
    """
    p = Path(path)
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"'{path}' не является существующей директорией.")
    return p


def parse_args():
    parser = argparse.ArgumentParser(
        prog='phishgen',
        description='Generating phishing load with DOCX documents'
    )

    subparsers = parser.add_subparsers(
        title="Modes",
        description="Available modes",
        dest="mode",
        required=True
    )

    inject.add_subparser(subparsers)
    if os.name == 'nt':
        macro.add_subparser(subparsers)
    else:
        log.debug("Sorry, macro option is not available on non-Windows platforms")
    create.add_subparser(subparsers)

    args = parser.parse_args()
    args.func(args)
