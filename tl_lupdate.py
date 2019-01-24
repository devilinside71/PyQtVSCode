# -*- coding: utf-8 -*-
"""Pylupdate replacement"""


import os


def main():
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

    # Create command line
    cmd_line = 'pylupdate5 '
    for elem in list_of_files:
        cmd_line += elem+' '
    cmd_line += '-ts i18n/hu.ts'
    print(cmd_line)
    os.system(cmd_line)


if __name__ == '__main__':
    main()
