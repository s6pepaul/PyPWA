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

-_CreateLogOfFiles - Creates a log that finds out whether files exist in it
or not. Makes an entire log of added, deleted, and modified files

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


class _CreateLogOfFiles(object):
    def __init__(self):
        super(_CreateLogOfFiles, self).__init__()
        self.__added_files_log = []
        self.__deleted_files_log = []
        self.__modified_files_log = []

    def add_file_to_added_log(self, file):
        if file not in self.__added_files_log:
            self.__added_files_log.append(file)

    def add_file_to_deleted_log(self, file):
        if file not in self.__deleted_files_log:
            self.__deleted_files_log.append(file)

    def add_file_to_modified_log(self, file):
        if file not in self.__modified_files_log:
            self.__modified_files_log.append(file)

    def get_files_from_added_log(self, list_of_added_files):
        # self.__take_snapshot_of_current_directory()
        for file in self.__added_files_log:
            if file not in list_of_added_files:
                list_of_added_files.append(file)
        list_of_added_files.insert(0, 'File(s) added: \n')
        return list_of_added_files

    def get_files_from_deleted_log(self, list_of_deleted_files):
        # self.__take_snapshot_of_current_directory()
        for file in self.__deleted_files_log:
            if file not in list_of_deleted_files:
                list_of_deleted_files.append(file)
        list_of_deleted_files.insert(0, 'File(s) removed: \n')
        return list_of_deleted_files

    def get_files_from_modified_log(self, list_of_modified_files):
        # removed take snapshot
        for file in self.__modified_files_log:
            if file not in list_of_modified_files:
                list_of_modified_files.append(file)
        list_of_modified_files.insert(0, 'File(s) Modified: \n')
        return list_of_modified_files


class _DirectoryWatcher(object):
    def __init__(self, initial_path):
        super(_DirectoryWatcher, self).__init__()
        self.__initial_path = initial_path
        self.__current_directory = None
        self.__updated_directory = None
        self.compare_directories = None
        self.number_of_files_before = 0
        self.number_of_files_after = 0

    def take_snapshot_of_current_directory(self):
        self.__current_directory = watchdog.utils.dirsnapshot. \
            DirectorySnapshot(self.__initial_path, recursive=False)
        self.number_of_files_before = len(self.__current_directory.paths)
        print('Length of old Files: ', len(self.__current_directory.paths))
        return self.__current_directory

    def take_snapshot_of_updated_directory(self):
        self.__updated_directory = watchdog.utils.dirsnapshot. \
            DirectorySnapshot(self.__initial_path, recursive=False)
        self.number_of_files_after = len(self.__updated_directory.paths)
        print('Length of updated list: ', len(self.__updated_directory.paths))
        return self.__updated_directory

    def compare_changes_in_directories(self):
        print(self.__updated_directory.paths)
        self.compare_directories = watchdog.utils.dirsnapshot. \
            DirectorySnapshotDiff(self.__current_directory,
                                  self.__updated_directory)
        return self.compare_directories


class _GetChanged(object):

    def __init__(self, initial_path, directory_watcher):
        # type: (str, _DirectoryWatcher) -> None
        super(_GetChanged, self).__init__()
        self.__initial_path = initial_path
        self.list_of_added_files = []
        self.list_of_deleted_files = []
        self.list_of_modified_files = []
        self.directory_watcher_elements = directory_watcher
        self.__stored_snapshot = directory_watcher.\
            compare_changes_in_directories()
        self.__get_list_of_files()
        self.__compare_lists_to_logs()

    def __get_list_of_files(self):
        self.list_of_added_files = self.__stored_snapshot.files_created
        self.list_of_deleted_files = self.__stored_snapshot.files_deleted
        self.list_of_modified_files = self.__stored_snapshot.files_modified
        print('Added : ', self.list_of_added_files)
        print(self.list_of_deleted_files)
        print(self.list_of_deleted_files)

    def __compare_lists_to_logs(self):
        for file in self.list_of_added_files:
            _CreateLogOfFiles().add_file_to_added_log(file)

        for file in self.list_of_deleted_files:
            _CreateLogOfFiles().add_file_to_deleted_log(file)

        for file in self.list_of_modified_files:
            _CreateLogOfFiles().add_file_to_modified_log(file)

    def return_log_of_files(self):
        number_of_files_before = self.directory_watcher_elements.\
            number_of_files_before
        number_of_files_after = self.directory_watcher_elements.\
            number_of_files_after
        print('After: ', number_of_files_after)
        print('Before: ', number_of_files_before)

        if number_of_files_after > number_of_files_before:
            old_list = self.list_of_added_files
            updated_added_files_list \
                = _CreateLogOfFiles().get_files_from_added_log(old_list)
            return updated_added_files_list

        elif number_of_files_after < number_of_files_before:
            old_list = self.list_of_deleted_files
            updated_deleted_files_list \
                = _CreateLogOfFiles().get_files_from_deleted_log(old_list)
            return updated_deleted_files_list

        elif len(self.list_of_modified_files) > 0:
            old_list = self.list_of_modified_files
            updated_modified_files_list \
                = _CreateLogOfFiles().get_files_from_modified_log(old_list)
            return updated_modified_files_list

        else:
            listeria = ['No New Files \n']
            return listeria


class _UpdateUserOnNewFileEntry(QtWidgets.QTextEdit):
    def __init__(self, initial_path):
        super(_UpdateUserOnNewFileEntry, self).__init__()
        self.setReadOnly(True)
        self.__directory_updater = _DirectoryWatcher(initial_path)
        self.__directory_updater.take_snapshot_of_current_directory()
        self.__initial_path = initial_path
        self.__trigger(initial_path)

    def __trigger(self, initial_path):
        self.__new_file_trigger = QtCore.QFileSystemWatcher(self)
        self.__new_file_trigger.addPath(initial_path)
        self.__new_file_trigger.directoryChanged.connect(
            self.__update_file_display)

    def __update_file_display(self):
        self.clear()
        self.__directory_updater.take_snapshot_of_updated_directory()
        updates_display = _GetChanged(self.__initial_path,
                                      self.__directory_updater)
        changed_list = updates_display.return_log_of_files()
        print('something happened')
        for file in changed_list:
            self.textCursor().insertText(file + '\n')
        # _DirectoryWatcher(self.__initial_path)


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
