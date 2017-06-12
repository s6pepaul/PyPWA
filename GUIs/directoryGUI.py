#!/usr/bin/python3
# -*- coding: utf-8 -*-

# PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Directory Widget
----------------
This is a widget to view a directory and display changes to that directory
based on a button press.

- _TreeInitialization - Creates a tree of the directory specified by main
window.

-_DirectoryWatcher - Checks current directory for created, deleted or modified
files. Returns any changes to a text box.

-_UpdateUserOnNewFileEntry - Initializes _DirectoryWater to create a initial
object containing directory data. Once the directory changes, a trigger is
activated and the updates are displayed in a directory

-_Splitter - Creates a widget that vertically splits a display of a
directory tree(_TreeInitialization) and a text box with file changes
(_UpdateUserOnNewFileEntry).

-_DirectoryView - Places splitter widget in a layout. Main object to create
this widget

"""

import sys
import watchdog
import copy

from typing import List
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from watchdog import utils
from watchdog.utils import dirsnapshot


class _TreeInitialization(QtWidgets.QTreeView):
    def __init__(self, initial_path):
        super(_TreeInitialization, self).__init__()
        self.__model = None
        self.__creating_model(initial_path)
        self.__defining_tree(initial_path)

    def __creating_model(self, initial_path):
        self.__model = QtWidgets.QFileSystemModel()
        self.__model.setRootPath(initial_path)

    def __defining_tree(self, initial_path):
        self.setModel(self.__model)
        self.setRootIndex(self.__model.index(initial_path))
        self.setAnimated(True)
        self.setIndentation(20)
        self.setSortingEnabled(True)
        self.setWindowTitle("Dir View")


class _DirectoryWatcher(object):
    def __init__(self, initial_path):
        super(_DirectoryWatcher, self).__init__()
        self.__initial_path = initial_path
        self.__current_directory = None
        self.__updated_directory = None
        self.__compare_directories = None
        self.__number_of_files_before = None
        self.__number_of_files_after = None
        self.__added_files_log = []
        self.__deleted_files_log = []
        self.__modified_files_log = []
        self.__take_snapshot_of_current_directory()

    def __take_snapshot_of_current_directory(self):
        self.__current_directory = watchdog.utils.dirsnapshot. \
            DirectorySnapshot(self.__initial_path, recursive=False)

        self.__number_of_files_before = len(self.__current_directory.paths)

    def __compare_changes_in_directories(self):
        self.__updated_directory = watchdog.utils.dirsnapshot. \
            DirectorySnapshot(self.__initial_path, recursive=False)

        self.__number_of_files_after = len(self.__updated_directory.paths)

        self.__compare_directories = watchdog.utils.dirsnapshot. \
            DirectorySnapshotDiff(self.__current_directory,
                                  self.__updated_directory)

    def __get_files_from_added_log(self, list_of_added_files):
        self.__take_snapshot_of_current_directory()
        for file in self.__added_files_log:
            if file not in list_of_added_files:
                list_of_added_files.append(file)
        list_of_added_files.insert(0, 'File(s) added: \n')
        return list_of_added_files

    def __get_files_from_deleted_log(self, list_of_deleted_files):
        self.__take_snapshot_of_current_directory()
        for file in self.__deleted_files_log:
            if file not in list_of_deleted_files:
                list_of_deleted_files.append(file)
        list_of_deleted_files.insert(0, 'File(s) removed: \n')
        return list_of_deleted_files

    def __get_files_from_modified_log(self, list_of_modified_files):
        self.__take_snapshot_of_current_directory()
        for file in self.__modified_files_log:
            if file not in list_of_modified_files:
                list_of_modified_files.append(file)
        list_of_modified_files.insert(0, 'File(s) Modified: \n')
        return list_of_modified_files

    def get_changed(self):
        # type: () -> str
        self.__compare_changes_in_directories()

        list_of_added_files = self.__compare_directories.files_created
        list_of_deleted_files = self.__compare_directories.files_deleted
        list_of_modified_files = self.__compare_directories.files_modified

        for file in list_of_added_files:
            if file not in self.__added_files_log:
                self.__added_files_log.append(file)

        for file in list_of_deleted_files:
            if file not in self.__deleted_files_log:
                self.__deleted_files_log.append(file)

        for file in list_of_modified_files:
            if file not in self.__modified_files_log:
                self.__modified_files_log.append(file)

        if self.__number_of_files_after > self.__number_of_files_before:
            updated_added_files_list \
                = self.__get_files_from_added_log(list_of_added_files)
            return updated_added_files_list

        elif self.__number_of_files_after < self.__number_of_files_before:
            updated_deleted_files_list \
                = self.__get_files_from_deleted_log(list_of_deleted_files)
            return updated_deleted_files_list

        elif len(list_of_modified_files) > 0:
            updated_modified_files_list\
                = self.__get_files_from_modified_log(list_of_modified_files)
            return updated_modified_files_list

        else:
            self.__take_snapshot_of_current_directory()
            listeria = 'No New Files \n'
            return listeria


class _UpdateUserOnNewFileEntry(QtWidgets.QTextEdit):
    def __init__(self, initial_path):
        super(_UpdateUserOnNewFileEntry, self).__init__()
        self.setReadOnly(True)
        self.__directory_updater = _DirectoryWatcher(initial_path)
        self.__initial_path = initial_path
        self.__trigger(initial_path)

    def __trigger(self, initial_path):
        self.__new_file_trigger = QtCore.QFileSystemWatcher(self)
        self.__new_file_trigger.addPath(initial_path)
        self.__new_file_trigger.directoryChanged.connect(
            self.__update_file_display)

    def __update_file_display(self):
        self.clear()
        changed__list = self.__directory_updater.get_changed()
        print('something happened')
        for file in changed__list:
            self.textCursor().insertText(file + '\n')


class _Splitter(QtWidgets.QSplitter):
    def __init__(self, initial_path):
        super(_Splitter, self).__init__()
        self.addWidget(_TreeInitialization(initial_path))
        self.addWidget(_UpdateUserOnNewFileEntry(initial_path))


class _DirectoryView(QtWidgets.QWidget):
    def __init__(self, initial_path):
        super(_DirectoryView, self).__init__()
        self.__initialize_ui(initial_path)

    def __initialize_ui(self, initial_path):
        vertical_box = QtWidgets.QVBoxLayout()
        vertical_box.addWidget(_Splitter(initial_path))
        self.setLayout(vertical_box)


class _MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(_MainWindow, self).__init__()
        self.setGeometry(300, 300, 600, 580)
        self.setWindowTitle('Home Directory View')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        self.setCentralWidget(_DirectoryView(QtCore.QDir.homePath()))
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    directory_view = _MainWindow()
    sys.exit(app.exec_())
