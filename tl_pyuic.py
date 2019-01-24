# -*- coding: utf-8 -*-
"""Pyuic replacement"""


import os
import sys
import xml.etree.ElementTree as ET
import logging
import platform

__author__ = 'Laszlo Tamas'
__copyright__ = 'Copyright 2027, Laszlo Tamas'
__license__ = 'GPL'
__version__ = '0.0.1'
__maintainer__ = 'Laszlo Tamas'
__status__ = 'Initial'

LOGGER = logging.getLogger('tlpyuic')
# set level for file handling (NOTSET>DEBUG>INFO>WARNING>ERROR>CRITICAL)
LOGGER.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
LOGGER_FH = logging.FileHandler('tlpyuic.log')

# create console handler with a higher log level
LOGGER_CH = logging.StreamHandler()
LOGGER_CH.setLevel(logging.INFO)

# create FORMATTER and add it to the handlers
FORMATTER = \
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                      )
LOGGER_FH.setFormatter(FORMATTER)
LOGGER_CH.setFormatter(FORMATTER)

# add the handlers to the LOGGER
LOGGER.addHandler(LOGGER_FH)
LOGGER.addHandler(LOGGER_CH)


class TLPyUIC():
    """Main class.

    """

    def __init__(self):
        self.par_input = ''
        self.output = ''
        self.pyuic_cmd = ''
        self.base_name = ''
        self.class_name = ''
        self.super_class = ''
        self.form_class = ''
        self.form_file = ''
        self.control_output = ''
        self.parent_path = ''
        self.preview_mode = False
        self.pyuic_cmd_win = 'c:\\Python36\\Scripts\\pyuic5.exe'
        self.pyuic_cmd_mac = '/Library/Frameworks/Python.framework/Versions/3.6/bin/pyuic5'
        self.pyuic_cmd_linux = '/usr/bin/pyuic5'
        self.control_file_exists = False

    def compile_form(self):
        """Execute the program by arguments.
        """
        if str(sys.argv[1]) == '-p':
            self.preview_mode = True
            self.par_input = str(sys.argv[2])
        else:
            self.par_input = str(sys.argv[1])
        LOGGER.debug('Preview mode: %s', self.preview_mode)
        self.base_name = os.path.basename(self.par_input)
        self.form_file = os.path.splitext(self.base_name)[0].lower()
        self.parent_path = os.path.abspath(
            os.path.join(self.par_input, os.pardir))
        self.class_name = os.path.splitext(self.base_name)[0]
        self.output = self.parent_path+'/Ui_'+self.form_file+'.py'
        self.control_output = self.parent_path+'/'+self.form_file+'.py.txt'
        self.control_file_exists = os.path.isfile(self.control_output)
        if platform.system() == 'Windows':
            if self.preview_mode:
                self.pyuic_cmd = self.pyuic_cmd_win + ' -p ' + self.par_input
            else:
                self.pyuic_cmd = self.pyuic_cmd_win + ' -o ' + \
                    self.output + ' ' + self.par_input
        if platform.system() == 'Darwin':
            if self.preview_mode:
                self.pyuic_cmd = self.pyuic_cmd_mac + ' -p ' + self.par_input
            else:
                self.pyuic_cmd = self.pyuic_cmd_mac + ' -o ' + self.output + ' ' + self.par_input
        if platform.system() == 'Linux':
            if self.preview_mode:
                self.pyuic_cmd = self.pyuic_cmd_linux + ' -p ' + self.par_input
            else:
                self.pyuic_cmd = self.pyuic_cmd_linux + \
                    ' -o ' + self.output + ' ' + self.par_input
        LOGGER.debug('Command: %s', platform.system() + '>>' + self.pyuic_cmd)
        os.system(self.pyuic_cmd)
        LOGGER.debug('Input: %s', self.par_input)
        LOGGER.debug('Output: %s', self.output)
        LOGGER.debug('Control output: %s', self.control_output)

    def add_executable_part(self):
        """Add executable __mai__ part to compiled file.
        """
        tree = ET.parse(self.par_input)
        root = tree.getroot()
        self.form_class = ''
        for child in root:
            if child.tag == 'class':
                self.form_class = child.text
        self.super_class = 'Q'+self.form_class
        # append execution code to Ui_*.py
        gen_code = '\n'
        gen_code += 'if __name__ == \'__main__\':\n'
        gen_code += '    import sys\n'
        gen_code += '    import os\n'
        gen_code += '    APP = QtWidgets.QApplication(sys.argv)\n'
        gen_code += '    PARENT_PATH = os.path.join(os.path.join(\n'
        gen_code += '        __file__, os.path.pardir), os.path.pardir)\n'
        gen_code += '    DIR_PATH = os.path.abspath(PARENT_PATH)\n'
        gen_code += '    FILE_PATH = os.path.join(DIR_PATH, \'i18n\',  \'hu.qm\')\n'
        gen_code += '    TRANSLATOR = QtCore.QTranslator()\n'
        gen_code += '    TRANSLATOR.load(FILE_PATH)\n'
        gen_code += '    APP.installTranslator(TRANSLATOR)\n'
        gen_code += '    THISWINDOW = QtWidgets.'+self.super_class+'()\n'
        gen_code += '    UI = Ui_'+self.form_class+'()\n'
        gen_code += '    UI.setupUi(THISWINDOW)\n'
        gen_code += '    THISWINDOW.show()\n'
        gen_code += '    sys.exit(APP.exec_())\n'
        with open(self.output, "a") as myfile:
            myfile.write(gen_code)

    def generate_control_head(self):
        """Generate the head part of the control .py file.
        """
        if not self.control_file_exists:
            gen_code = ''
            gen_code += '# -*- coding: utf-8 -*-\n'
            gen_code += '\n'
            gen_code += '"""Module implementing '+self.class_name+'."""\n'
            gen_code += '\n'
            gen_code += 'import logging\n'
            gen_code += 'from PyQt5.QtCore import pyqtSlot, QCoreApplication\n'
            gen_code += 'from PyQt5.QtWidgets import '+self.super_class+', QMessageBox\n'
            gen_code += '\n'
            gen_code += 'from .Ui_'+self.form_file+' import Ui_'+self.form_class+'\n'
            gen_code += '\n'
            gen_code += '\n'
            gen_code += 'class '+self.class_name + \
                '('+self.super_class+', Ui_'+self.form_class+'):\n'
            gen_code += '    """\n'
            gen_code += '    Class documentation goes here.\n'
            gen_code += '    """\n'
            gen_code += '    def __init__(self, arguments, parent=None):\n'
            gen_code += '        """\n'
            gen_code += '        Constructor\n'
            gen_code += '        \n'
            gen_code += '        @param parent reference to the parent widget\n'
            gen_code += '        @type QWidget\n'
            gen_code += '        """\n'
            gen_code += '        super('+self.class_name + \
                ', self).__init__(parent)\n'
            gen_code += '        self.class_name = self.__class__.__name__\n'
            gen_code += '        log_name = \'program.\' + self.class_name\n'
            gen_code += '        self.module_logger = logging.getLogger(log_name)\n'
            gen_code += '        self.module_logger.setLevel(logging.DEBUG)\n'
            gen_code += '        logger_fh = logging.FileHandler(\'program.log\')\n'
            gen_code += '        logger_ch = logging.StreamHandler()\n'
            gen_code += '        logger_ch.setLevel(logging.INFO)\n'
            gen_code += '        self.args = arguments\n'
            gen_code += '\n'
            gen_code += '        # create formatter and add it to the handlers\n'
            gen_code += '\n'
            gen_code += '        formatter = \\\n'
            gen_code += '            logging.Formatter(\n'
            gen_code += '                    '
            gen_code += '\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\'\n'
            gen_code += '                              )\n'
            gen_code += '        logger_fh.setFormatter(formatter)\n'
            gen_code += '        logger_ch.setFormatter(formatter)\n'
            gen_code += '\n'
            gen_code += '        # add the handlers to the logger\n'
            gen_code += '\n'
            gen_code += '        self.module_logger.addHandler(logger_fh)\n'
            gen_code += '        self.module_logger.addHandler(logger_ch)\n'
            gen_code += '        self.setupUi(self)\n'
            with open(self.control_output, 'wb') as myfile:
                myfile.write(gen_code.encode('utf-8'))

    def generate_general_slots(self):
        """Generate generally used slot codes.
        """
        if not self.control_file_exists:
            gen_code = '\n'
            gen_code += '    @pyqtSlot()\n'
            gen_code += '    def closeEvent(self, event):\n'
            gen_code += '        """\n'
            gen_code += '        Override original event.\n'
            gen_code += '\n'
            gen_code += '        @param event original close event\n'
            gen_code += '\n'
            gen_code += '        """\n'
            gen_code += '        _translate = QCoreApplication.translate\n'
            gen_code += '        quit_title = _translate(\'' + \
                self.class_name+'\', \'Confirmation\')\n'
            gen_code += '        quit_msg = _translate(\'' + \
                self.class_name+'\',\n'
            gen_code += '         '
            gen_code += '                     \'Are you sure you want to exit the program?\')\n'
            gen_code += '        reply = QMessageBox.question(self, quit_title, quit_msg,\n'
            gen_code += '                                     QMessageBox.Yes, QMessageBox.No)\n'
            gen_code += '        if reply == QMessageBox.Yes:\n'
            gen_code += '            self.module_logger.debug(\'Confirmed to exit program\')\n'
            gen_code += '            event.accept()\n'
            gen_code += '        else:\n'
            gen_code += '            event.ignore()\n'
            with open(self.control_output, 'ab') as myfile:
                myfile.write(gen_code.encode('utf-8'))

    def generate_slots(self):
        """Generate slot codes.
        """
        gen_code = ''
        action_code = ''
        tree = ET.parse(self.par_input)
        root = tree.getroot()
        for level1 in root:
            for level2 in level1:
                # print('2', level2.tag, level2.attrib)
                # menu items
                if level2.tag == 'action':
                    action_name = level2.get('name')
                    action_code = 'def on_' + \
                        action_name + '_triggered(self):'
                    if not self.control_file_exists or \
                            not action_code in open(self.control_output).read():
                        gen_code += '    \n'
                        gen_code += '    @pyqtSlot()\n'
                        gen_code += '    def on_' + \
                            action_name + '_triggered(self):\n'
                        gen_code += '        """\n'
                        gen_code += '        Slot documentation goes here.\n'
                        gen_code += '        """\n'
                        if action_name == 'actionQuit':
                            gen_code += '        self.close()\n'
                        else:
                            gen_code += '        # TODO: not implemented yet\n'
                            gen_code += '        raise NotImplementedError\n'
                # controls
                for level3 in level2:
                    level_class = level3.get('class')
                    level_name = level3.get('name')
                    if level_class == 'QPushButton':
                        actions = ('clicked', 'pressed', 'released')
                        act_count = 0
                        pre = ''
                        for act in actions:
                            act_count += 1
                            action_code = 'def on_' + \
                                level_name + '_' + act + '(self):\n'
                            if not self.control_file_exists or \
                                    not action_code in open(self.control_output).read():
                                if act_count > 1:
                                    pre = '# '
                                gen_code += '\n'
                                gen_code += pre + '    @pyqtSlot()\n'
                                gen_code += pre + '    def on_' + \
                                    level_name + '_' + act + '(self):\n'
                                gen_code += pre + '        """\n'
                                gen_code += pre + '        Slot documentation goes here.\n'
                                gen_code += pre + '        """\n'
                                gen_code += pre + '        # TODO: not implemented yet\n'
                                gen_code += pre + '        raise NotImplementedError\n'
                    if level_class == 'QCheckBox':
                        action_code = 'def on_' + \
                            level_name + '_toggled(self, checked):\n'
                        if not self.control_file_exists or \
                                not action_code in open(self.control_output).read():
                            gen_code += '\n'
                            gen_code += '    @pyqtSlot(bool)\n'
                            gen_code += '    def on_' + \
                                level_name + '_toggled(self, checked):\n'
                            gen_code += '        """\n'
                            gen_code += '        Slot documentation goes here.\n'
                            gen_code += '        """\n'
                            gen_code += '        \n'
                            gen_code += '        @param checked DESCRIPTION\n'
                            gen_code += '        @type bool\n'
                            gen_code += '        """\n'
                            gen_code += '        # TODO: not implemented yet\n'
                            gen_code += '        raise NotImplementedError\n'
                    if level_class == 'QLineEdit':
                        action_code = 'def on_' + \
                            level_name + '_textChanged(self, p0):\n'
                        if not self.control_file_exists or \
                                not action_code in open(self.control_output).read():
                            gen_code += '\n'
                            gen_code += '    @pyqtSlot(str)\n'
                            gen_code += '    def on_' + \
                                level_name + '_textChanged(self, p0):\n'
                            gen_code += '        """\n'
                            gen_code += '        Slot documentation goes here.\n'
                            gen_code += '        \n'
                            gen_code += '        @param p0 DESCRIPTION\n'
                            gen_code += '        @type str\n'
                            gen_code += '        """\n'
                            gen_code += '        # TODO: not implemented yet\n'
                            gen_code += '        raise NotImplementedError\n'
                            gen_code += '    \n'
                        action_code = 'def on_' + \
                            level_name + '_returnPressed(self):\n'
                        if not self.control_file_exists or \
                                not action_code in open(self.control_output).read():
                            gen_code += '\n'
                            gen_code += '    @pyqtSlot()\n'
                            gen_code += '    def on_' + \
                                level_name + '_returnPressed(self):\n'
                            gen_code += '        """\n'
                            gen_code += '        Slot documentation goes here.\n'
                            gen_code += '        """\n'
                            gen_code += '        # TODO: not implemented yet\n'
                            gen_code += '        raise NotImplementedError\n'
                            gen_code += '    \n'

        with open(self.control_output, 'ab') as myfile:
            myfile.write(gen_code.encode('utf-8'))


if __name__ == '__main__':
    LOGGER.debug('Start program')
    PROG = TLPyUIC()
    PROG.compile_form()
    if not PROG.preview_mode:
        PROG.add_executable_part()
        PROG.generate_control_head()
        PROG.generate_general_slots()
        PROG.generate_slots()
    LOGGER.debug('Exit program')
    sys.exit()
