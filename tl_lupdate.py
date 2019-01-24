# -*- coding: utf-8 -*-
"""Pylupdate replacement"""


import os
import platform


def main():
    pyuic_cmd_win = 'pylupdate5 '
    pyuic_cmd_mac = 'pylupdate5 '
    pyuic_cmd_linux = 'pylupdate5 '
    parent_path = os.path.join(__file__, os.path.pardir)
    dir_name = os.path.abspath(parent_path)
    # print(dir_name)
    # Get the list of all files in directory tree at given path
    list_of_files = list()
    for (dirpath, dirnames, filenames) in os.walk(dir_name):
        for filename in filenames:
            if filename.endswith('.py'):
                # list_of_files += [os.path.join(dirpath, filename)]
                list_of_files += [os.path.join(dirpath,
                                               filename).replace(dir_name+'/', '')]

    # Print the files
    # for elem in list_of_files:
    #     print(elem)
    parent_path = os.path.join(__file__, os.path.pardir)
    dir_path = os.path.abspath(parent_path)
    print(dir_path)
    # Create command line
    cmd_line = ''
    if platform.system() == 'Windows':
        cmd_line = pyuic_cmd_win
    if platform.system() == 'Darwin':
        cmd_line = pyuic_cmd_mac
    if platform.system() == 'Linux':
        cmd_line = pyuic_cmd_linux
    for elem in list_of_files:
        if platform.system() == 'Windows':
            cmd_line += '"'+elem.replace(dir_path+'\\', '')+'" '
        else:
            cmd_line += elem+' '
    cmd_line += '-ts i18n/hu.ts'
    print(cmd_line)
    os.system(cmd_line)


if __name__ == '__main__':
    main()
