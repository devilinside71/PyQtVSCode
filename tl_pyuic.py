# -*- coding: utf-8 -*-

import os
import sys
from subprocess import call
import xml.etree.ElementTree as ET
cmd_arg = sys.argv[1]
base_name = os.path.basename(cmd_arg)
form_file = os.path.splitext(base_name)[0].lower()
parent_path = os.path.abspath(os.path.join(cmd_arg, os.pardir))
out_file = parent_path+"/Ui_"+form_file+".py"
pyuic_cmd = "c:\\Python36\\Scripts\\pyuic5.exe -o " + \
    out_file + " " + str(cmd_arg)
print(pyuic_cmd)
os.system(pyuic_cmd)


tree = ET.parse(cmd_arg)
root = tree.getroot()
form_class = ''
for child in root:
    if child.tag == 'class':
        form_class = child.text
super_class = 'Q'+form_class
class_name = os.path.splitext(base_name)[0]


# append execution code to Ui_*
gen_code = '\n'
gen_code += 'if __name__ == \'__main__\':\n'
gen_code += '    import sys\n'
gen_code += '    import os\n'
gen_code += '    app = QtWidgets.QApplication(sys.argv)\n'
gen_code += '    parent_path = os.path.join(os.path.join(\n'
gen_code += '        __file__, os.path.pardir), os.path.pardir)\n'
gen_code += '    dir_path = os.path.abspath(parent_path)\n'
gen_code += '    file_path = os.path.join(dir_path, \'i18n\',  \'hu.qm\')\n'
gen_code += '    translator = QtCore.QTranslator()\n'
gen_code += '    translator.load(file_path)\n'
gen_code += '    app.installTranslator(translator)\n'
gen_code += '    '+class_name+' = QtWidgets.'+super_class+'()\n'
gen_code += '    ui = Ui_'+form_class+'()\n'
gen_code += '    ui.setupUi('+class_name+')\n'
gen_code += '    '+class_name+'.show()\n'
gen_code += '    sys.exit(app.exec_())\n'

with open(out_file, "a") as myfile:
    myfile.write(gen_code)

# generate main .py file
gen_code = ''
gen_code += '# -*- coding: utf-8 -*-\n'
gen_code += '\n'
gen_code += '"""Module implementing '+class_name+'."""\n'
gen_code += '\n'
gen_code += 'import logging\n'
gen_code += 'from PyQt5.QtCore import pyqtSlot\n'
gen_code += 'from PyQt5.QtWidgets import '+super_class+', QMessageBox\n'
gen_code += '\n'
gen_code += 'from .Ui_'+form_file+' import Ui_'+form_class+'\n'
gen_code += '\n'
gen_code += '\n'
gen_code += 'class '+class_name+'('+super_class+', Ui_'+form_class+'):\n'
gen_code += '    """\n'
gen_code += '    Class documentation goes here.\n'
gen_code += '    """\n'
gen_code += '    def __init__(self, parent=None):\n'
gen_code += '        """\n'
gen_code += '        Constructor\n'
gen_code += '        \n'
gen_code += '        @param parent reference to the parent widget\n'
gen_code += '        @type QWidget\n'
gen_code += '        """\n'
gen_code += '        super('+class_name+', self).__init__(parent)\n'
gen_code += '        self.class_name = self.__class__.__name__\n'
gen_code += '        log_name = \'program.\' + self.class_name\n'
gen_code += '        self.module_logger = logging.getLogger(log_name)\n'
gen_code += '        self.module_logger.setLevel(logging.DEBUG)\n'
gen_code += '        logger_fh = logging.FileHandler(\'program.log\')\n'
gen_code += '        logger_ch = logging.StreamHandler()\n'
gen_code += '        logger_ch.setLevel(logging.INFO)\n'
gen_code += '\n'
gen_code += '        # create formatter and add it to the handlers\n'
gen_code += '\n'
gen_code += '        formatter = \\\n'
gen_code += '            logging.Formatter(\n'
gen_code += '                    \'%(asctime)s - %(name)s - %(levelname)s - %(message)s\'\n'
gen_code += '                              )\n'
gen_code += '        logger_fh.setFormatter(formatter)\n'
gen_code += '        logger_ch.setFormatter(formatter)\n'
gen_code += '\n'
gen_code += '        # add the handlers to the logger\n'
gen_code += '\n'
gen_code += '        self.module_logger.addHandler(logger_fh)\n'
gen_code += '        self.module_logger.addHandler(logger_ch)\n'
gen_code += '        self.setupUi(self)\n'


# PyQt slots
gen_code += '\n'
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
    class_name+'\', \'Confirmation\')\n'
gen_code += '        quit_msg = _translate(\''+class_name+'\',\n'
gen_code += '                              \'Are you sure you want to exit the program?\')\n'
gen_code += '        reply = QMessageBox.question(self, quit_title, quit_msg,\n'
gen_code += '                                     QMessageBox.Yes, QMessageBox.No)\n'
gen_code += '        if reply == QMessageBox.Yes:\n'
gen_code += '            self.module_logger.debug(\'Confirmed to exit program\')\n'
gen_code += '            event.accept()\n'
gen_code += '        else:\n'
gen_code += '            event.ignore()\n'

for level1 in root:
    for level2 in level1:
        for level3 in level2:
            level_class = level3.get('class')
            level_name = level3.get('name')
            if level_class == 'QPushButton':
                gen_code += '\n'
                gen_code += '    @pyqtSlot()\n'
                gen_code += '    def on_' + level_name + '_clicked(self):\n'
                gen_code += '        """\n'
                gen_code += '        Slot documentation goes here.\n'
                gen_code += '        """\n'
                gen_code += '        # TODO: not implemented yet\n'
                gen_code += '        raise NotImplementedError\n'
            if level_class == 'QCheckBox':
                gen_code += '\n'
                gen_code += '    @pyqtSlot(int)\n'
                gen_code += '    def on_' + level_name + \
                    '_stateChanged(self, p0):\n'
                gen_code += '        """\n'
                gen_code += '        Slot documentation goes here.\n'
                gen_code += '        \n'
                gen_code += '        @param p0 DESCRIPTION\n'
                gen_code += '        @type int\n'
                gen_code += '        """\n'
                gen_code += '        # TODO: not implemented yet\n'
                gen_code += '        raise NotImplementedError\n'
            if level_class == 'QRadioButton':
                gen_code += '\n'
                gen_code += '    @pyqtSlot(bool)\n'
                gen_code += '    def on_' + level_name + \
                    '_toggled(self, checked):\n'
                gen_code += '        """\n'
                gen_code += '        Slot documentation goes here.\n'
                gen_code += '        \n'
                gen_code += '        @param checked DESCRIPTION\n'
                gen_code += '        @type bool\n'
                gen_code += '        """\n'
                gen_code += '        # TODO: not implemented yet\n'
                gen_code += '        raise NotImplementedError\n'

f = open(parent_path+"/"+form_file+".py.txt", 'wb')
f.write(gen_code.encode('utf-8'))
