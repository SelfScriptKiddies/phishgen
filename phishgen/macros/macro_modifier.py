import os

import jinja2

if os.name == 'nt':
    import win32com.client, pythoncom

    pythoncom.CoInitialize()

from pathlib import Path
from phishgen.logger import get_logger
from phishgen.macros import data_scrub
from phishgen.config import MACRO_SOURCE_PATH

log = get_logger(__name__)


def compile_code(payload: list[str]) -> str:
    """
    Compile payload into macro's code from jinja pattern

    :param payload: list of strings with VBA-payload
    :return: code, ready for execute
    """
    with open(MACRO_SOURCE_PATH) as file:
        code_skeleton = file.read()
    template = jinja2.Template(code_skeleton).render(source_code=payload)
    log.debug(f"Compiled new code:\n{template}")
    return template


def open_document(filepath: Path) -> tuple[win32com.client.CDispatch, win32com.client.CDispatch]:
    """
    Opens file in new instance of Word client

    :param filepath: path of needed file to open
    :return: word client and document object
    """
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(filepath.__str__(), ReadOnly=False)
    log.info(f"Opened new document: {filepath}")
    return word, doc


def close_handlers(word: win32com.client.Dispatch, doc: win32com.client.Dispatch):
    """
    Closing handlers for stable work

    :param word: word client
    :param doc: document object
    """
    doc.Close()
    word.Quit()
    log.debug(f"Closed word and document")


def modify_macro(doc: win32com.client.Dispatch, payload: str):
    """
    Modifying macro code in VBA-project

    :param doc: document object
    :param payload: rendered code
    :return: old code, which was in file before replacing
    """
    vba_project = doc.VBProject
    module = vba_project.VBComponents("NewMacros")
    old_code = module.CodeModule.Lines(1, module.CodeModule.CountOfLines)
    log.debug(f"Old module code: \n{old_code}")

    # Replace old code with payload
    module.CodeModule.DeleteLines(1, module.CodeModule.CountOfLines)
    module.CodeModule.AddFromString(payload)

    log.debug(f"New module code: \n{module.CodeModule.Lines(1, module.CodeModule.CountOfLines)}")
    return old_code


def save_file(doc: win32com.client.Dispatch, filepath: Path) -> Path:
    """
    Deletes personal data and saves file

    :param doc: document object
    :param filepath: filepath for saving file
    :return: filepath of new file
    """
    data_scrub.remove_document_properties(doc)
    data_scrub.remove_comments_and_tracked_changes(doc)
    log.debug(f"Successfully deleted all metadata")
    doc.SaveAs2(filepath.__str__(), FileFormat=15)
    log.info(f"Saved new file: {filepath}")
    return filepath


def replace_source_code(filepath: Path, source_code: str, output_path: Path = None):
    """
    Replacing source code of provided .dotm macro file

    :param filepath: path to macro file
    :param source_code: source code represented as string
    :param output_path: optional arg with path to output file
    :return:
    """
    if output_path is None:
        output_path = Path(os.getcwd()) / f"macro.dotm"
    word, doc = open_document(filepath)
    compiled_code = compile_code(source_code.split('\n'))
    modify_macro(doc, compiled_code)
    save_file(doc, output_path)
    close_handlers(word, doc)
