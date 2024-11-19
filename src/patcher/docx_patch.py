import os
import shutil
import zipfile
import tempfile
import jinja2

from pathlib import Path
from src import logger
from src.config import DOCX_TEMP_FILENAME, ACCEPT_NON_EXIST_MACRO, DOTM_SETTINGS_PATH
from urllib.parse import urlparse

log = logger.get_logger(__name__)


def create_temp_dir() -> Path:
    """
    Creates temporary directory and returns it. Made for logs

    :return: Path object, pointing to the temporary directory
    """
    temp_directory = tempfile.mkdtemp()
    log.debug(f"Created temp directory: {temp_directory}")
    return Path(temp_directory)


def delete_temp_dir(dir_path: Path):
    """
    Checks if path is directory and deletes it, if it exists

    :param dir_path: Path to directory
    """
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        log.debug(f"Deleted temp directory: {dir_path}")
        return

    log.error(f"Directory {dir_path} does not exist")


def validate_url(url: str):
    """
    Validates url

    :param url: URL to validate
    :return: True if url is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def refactor_macro_link(link: str) -> str:
    """
    Macro can be local and remote. This function recognize URL or filepath

    :param link:
    :return: True/False
    """
    if os.path.isfile(link):
        return f"file:///" + link
    if validate_url(link):
        return link
    if ACCEPT_NON_EXIST_MACRO:
        return link
    log.fatal(f"Link to macro {link} not an URL or filepath (to override change config)")


def patch_macro_path(filepath: Path, new_macro_path: str):
    """
    Edits template, that will be executed after opening the file

    :param filepath: filepath to DOCX file, created by template
    :param new_macro_path: filepath or URL of new macro
    :return:
    """
    if type(filepath) is str:
        filepath = Path(filepath)

    temp_directory = create_temp_dir()

    shutil.copyfile(filepath, temp_directory / f"{DOCX_TEMP_FILENAME}.zip")
    document = zipfile.ZipFile(temp_directory / f"{DOCX_TEMP_FILENAME}.zip", 'r')
    document.extractall(temp_directory / f"{DOCX_TEMP_FILENAME}")
    log.debug(f"Extracted {DOCX_TEMP_FILENAME}.zip in {temp_directory}")

    settings_filepath = None
    if os.path.isfile(variant1 := temp_directory / f"{DOCX_TEMP_FILENAME}/word/_rels/settings.xml.rels"):
        settings_filepath = variant1
    elif os.path.isfile(variant2 := temp_directory / f"{DOCX_TEMP_FILENAME}/word_rels/settings.xml.rels"):
        settings_filepath = variant2

    if settings_filepath is None:
        log.fatal(f"Not found settings.xml.rels! Maybe document was created without word template?")
        return

    if settings_filepath is not None:
        log.debug(f"Found settings: {settings_filepath}")

        with open(DOTM_SETTINGS_PATH, "r") as file:
            pattern = jinja2.Template(file.read())

        with open(settings_filepath, "w") as file:
            file.write(pattern.render(filepath=new_macro_path))
        log.info(f"Patched document's macro path to {new_macro_path}")

        temp_folder = temp_directory / f"{DOCX_TEMP_FILENAME}"

        with zipfile.ZipFile(temp_directory / f"{DOCX_TEMP_FILENAME}_patched.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in temp_folder.rglob('*'):
                if item.is_file():
                    zipf.write(item, arcname=item.relative_to(temp_folder))
                elif item.is_dir():
                    zip_info = zipfile.ZipInfo(str(item.relative_to(temp_folder)) + '/')
                    zipf.writestr(zip_info, '')

        new_filepath = filepath.parent / f"{filepath.stem}_patched.docx"
        shutil.move(
            temp_directory / f"{DOCX_TEMP_FILENAME}_patched.zip",
            new_filepath
        )
        log.info(f"Moved patched document to {new_filepath}")

    document.close()
    delete_temp_dir(temp_directory)


def copy_template(filepath: str, new_filepath: str):
    """
    Just copying function for better logging

    :param filepath: filepath for original file
    :param new_filepath: filepath for new file
    :return:
    """
    shutil.copy(filepath, new_filepath)
    log.debug(f"Copied {filepath} to {new_filepath}")
