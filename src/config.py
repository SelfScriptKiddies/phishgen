import logging
from pathlib import Path

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = None
LOG_DATE = False

DOTM_SETTINGS_PATH = "resources/templates/dotm_setting.j2"
MACRO_SOURCE_PATH = "resources/templates/macro_source.j2"

DOCX_TEMP_FILENAME = "document"
ACCEPT_NON_EXIST_MACRO = False

MACRO_DOTM_PATH = Path("resources/examples/macro.dotm").absolute()
