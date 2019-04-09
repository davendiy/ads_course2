#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Пакет з модулями, необхідними для роботи програми.
"""

from .constants import *
from .storage import *
from .html_redactors import *
from .merge import *
from .report import *

__all__ = ['HOME_PAGE',
           'HOME_PAGE_PATTERN',
           'DEFAULT_DATABASE',
           'DEFAULT_N',
           'change_html',
           'ADD_PARAMS',
           'id_dict',
           'name_dict',
           'fill_cr_page',
           'HTML_PIECE',
           'STYLE_SHEET',
           'data_curs',
           'data_connector',
           'FILE_MODE',
           'STRING_MODE',
           'showerror',
           'ERROR_PAGE',
           'StorageCollection',
           'StorageDB',
           'HOME_PARAMS',
           'DEFAULT_REPORT',
           'START_RELEASE',
           'CANCEL_RELEASE',
           'END_RELEASE',
           'ERROR_PAGE',
           'RELEASE_PAGE',
           'RELEASE_PAGE_PATTERN',
           "RELEASE_PARAMS",
           "REPORT_TEMPLATE",
           "ADD_PAGE_PATTERN",
           'create_report',
           'create_xlsx',
           'FINAL_PAGE',
           'showhref',
           'AUTHOR',
           'TMP_FILE_NAME',
           ]
