import jinja2
import win32com.client, pythoncom
from src import logger

log = logger.get_logger(__name__)
pythoncom.CoInitialize()


def compile_code(payload: list[str]) -> str:
    """
    Compile payload into macro's code from jinja pattern

    :param payload: list of strings with VBA-payload
    :return: code, ready for execute
    """
    with open("resources/templates/macro_source.j2") as file:
        code_skeleton = file.read()
    template = jinja2.Template(code_skeleton).render(source_code=payload)
    log.debug(f"Compiled new code:\n{template}")
    return template


def open_document(filepath: str) -> tuple[win32com.client.CDispatch, win32com.client.CDispatch]:
    """
    Opens file in new instance of Word client

    :param filepath: path of needed file to open
    :return: word client and document object
    """
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(filepath, ReadOnly=False)
    return word, doc


def modify_macro(doc):
    ...
