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

-_TextBoxHandler - sends all log output from console to QTextEdit Widget

-_DirectoryWatcher - Checks current directory for created, deleted or modified
files. Returns any changes to a text box.

-_Splitter - Creates a widget that vertically splits a display of a
directory tree(_TreeInitialization) and a text box with file changes
(_UpdateUserOnNewFileEntry).

-_DirectoryView - Places splitter widget in a layout and initializes
 files observer object. Main object to create
this widget.

"""

import logging
import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from watchdog import events
from watchdog import observers


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


class _TextBoxHandler(logging.Handler):
    def __init__(self):
        super(_TextBoxHandler, self).__init__()
        self.text_box = QtWidgets.QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.textCursor().atEnd()
        self.__initialize_text_box_handler()

    def emit(self, record):
        message = self.format(record)
        self.text_box.insertPlainText(message)

    def __initialize_text_box_handler(self):
        self.setFormatter(logging.Formatter(
            '%(message)s '))
        logging.getLogger().addHandler(self)
        logging.getLogger().setLevel(logging.INFO)


class _Splitter(QtWidgets.QSplitter):
    def __init__(self, initial_path):
        super(_Splitter, self).__init__()
        self.addWidget(_TreeInitialization(initial_path))
        __text_box_handle = _TextBoxHandler()
        self.addWidget(__text_box_handle.text_box)


class _DirectoryView(QtWidgets.QWidget):
    def __init__(self, initial_path):
        super(_DirectoryView, self).__init__()
        self.__initialize_observer(initial_path)
        self.__initialize_ui(initial_path)

    def __initialize_observer(self, initial_path):
        __event_handler = events.LoggingEventHandler()
        self.__observer = observers.Observer()
        self.__observer.schedule(__event_handler,
                                 initial_path, recursive=True)
        self.__observer.start()

    def __initialize_ui(self, initial_path):
        __vertical_box = QtWidgets.QVBoxLayout()
        __vertical_box.addWidget(_Splitter(initial_path))
        self.setLayout(__vertical_box)


class _MainWindow(QtWidgets.QMainWindow):

    __LOGGER = logging.getLogger(__name__ + "._MainWindow")

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