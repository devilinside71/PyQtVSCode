# -*- coding: utf-8 -*-
"""This module does blah blah."""
___copyright___ = 'Copyright (c) 2024 Laszlo Tamas'
___author___ = 'Laszlo Tamas'

# import locale
import logging
import sys
import os
from pathlib import Path
from PyQt5 import QtCore, QtWidgets

from ui.mainwindow import MainWindow

LOGGER = logging.getLogger('program')
# set level for file handling (NOTSET>DEBUG>INFO>WARNING>ERROR>CRITICAL)

LOGGER.setLevel(logging.DEBUG)

# create file handler which logs even debug messages

LOGGER_FH = logging.FileHandler('program.log')

# create console handler with a higher log level

LOGGER_CH = logging.StreamHandler()
LOGGER_CH.setLevel(logging.INFO)

# create formatter and add it to the handlers

LOG_FORMATTER = \
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                      )
LOGGER_FH.setFormatter(LOG_FORMATTER)
LOGGER_CH.setFormatter(LOG_FORMATTER)

# add the handlers to the logger

LOGGER.addHandler(LOGGER_FH)
LOGGER.addHandler(LOGGER_CH)


if __name__ == '__main__':
    LOGGER.debug('Start program')
    # Read LOC_LANG from settings file
    SETTINGS = QtCore.QSettings('settings.ini', QtCore.QSettings.IniFormat)
    SETTINGS.beginGroup('UserSettings')
    LOC_LANG = SETTINGS.value('Language')
    SETTINGS.endGroup()
    APP = QtWidgets.QApplication(sys.argv)
    PARENT_PATH = os.path.join(__file__, os.path.pardir)
    DIR_PATH = os.path.abspath(PARENT_PATH)
    FILE_PATH = os.path.join(DIR_PATH, 'i18n', LOC_LANG + '.qm')
    if Path(FILE_PATH).exists():
        TRANSLATOR = QtCore.QTranslator()
        TRANSLATOR.load(FILE_PATH)
        APP.installTranslator(TRANSLATOR)
    UI = MainWindow()
    UI.show()
    sys.exit(APP.exec_())
    LOGGER.debug('Exit program')
