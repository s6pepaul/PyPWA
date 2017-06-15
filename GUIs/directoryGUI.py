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

-_FileChangeHandler - is accessed by observer thread, once a file is
modified/created/deleted, text box is updated.

-_Splitter - Creates a widget that vertically splits a display of a
directory tree(_TreeInitialization) and a text box with file changes
(_UpdateUserOnNewFileEntry).

-_DirectoryView - Places splitter widget in a layout and initializes
 files observer object. Main object to create
this widget.

"""

import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from watchdog import events
from watchdog import observers


class _TreeInitialization(QtWidgets.QTreeView):
    def __init__(self, __initial_path):
        super(_TreeInitialization, self).__init__()
        self.__model = None
        self.__creating_model(__initial_path)
        self.__defining_tree(__initial_path)

    def __creating_model(self, __initial_path):
        self.__model = QtWidgets.QFileSystemModel()
        self.__model.setRootPath(__initial_path)

    def __defining_tree(self, initial_path):
        self.setModel(self.__model)
        self.setRootIndex(self.__model.index(initial_path))
        self.setAnimated(True)
        self.setIndentation(20)
        self.setSortingEnabled(True)
        self.setWindowTitle("Dir View")


class _FileChangeHandler(events.FileSystemEventHandler):

    def __init__(self):
        super(_FileChangeHandler, self).__init__()
        self.text_box = QtWidgets.QTextEdit()
        self.text_box.setReadOnly(True)
        self.__text = str()

    def on_moved(self, __event):
        __what = 'directory' if __event.is_directory else 'file'
        self.__text = 'Moved {0}: from {1} to {2} \n'.format(
            __what, __event.src_path, __event.dest_path
        )
        self.text_box.insertPlainText(self.__text)

    def on_created(self, __event):
        __what = 'directory' if __event.is_directory else 'file'
        self.__text = 'Created {0}: {1} \n'.format(__what, __event.src_path)
        self.text_box.insertPlainText(self.__text)

    def on_deleted(self, __event):
        __what = 'directory' if __event.is_directory else 'file'
        self.__text = 'Deleted {0}: {1} \n'.format(__what, __event.src_path)
        self.text_box.insertPlainText(self.__text)

    def on_modified(self, __event):
        __what = 'directory' if __event.is_directory else 'file'
        self.__text = 'Modified {0}: {1} \n'.format(__what, __event.src_path)
        self.text_box.insertPlainText(self.__text)


class _Splitter(QtWidgets.QSplitter):

    def __init__(self, initial_path, __event_handler):
        super(_Splitter, self).__init__()
        self.addWidget(_TreeInitialization(initial_path))
        self.addWidget(__event_handler.text_box)


class _DirectoryView(QtWidgets.QWidget):

    def __init__(self, __initial_path):
        super(_DirectoryView, self).__init__()
        self.__initial_path = __initial_path
        self.__event_handler = _FileChangeHandler()
        self.__initialize_observer()
        self.__initialize_ui()

    def __initialize_observer(self):
        self.__observer = observers.Observer()
        self.__observer.schedule(
            self.__event_handler, self.__initial_path, recursive=True
        )
        self.__observer.start()

    def __initialize_ui(self):
        __vertical_box = QtWidgets.QVBoxLayout()
        __vertical_box.addWidget(_Splitter(
            self.__initial_path, self.__event_handler
        ))
        self.setLayout(__vertical_box)

    def __del__(self):
        self.__observer.stop()


class _MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(_MainWindow, self).__init__()
        self.setGeometry(300, 300, 600, 580)
        self.setWindowTitle('Home Directory View')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        self.setCentralWidget(_DirectoryView(QtCore.QDir.currentPath()))
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dir_view = _MainWindow()
    sys.exit(app.exec_())