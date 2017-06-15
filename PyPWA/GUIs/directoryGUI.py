#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
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
based on file/directory modification.

- _TreeInitialization - Creates a tree of the directory specified by main
  window.

- _FileChangeHandler - is accessed by observer thread, once a file is
  modified/created/deleted, text box is updated.

- _Splitter - Creates a widget that vertically splits a display of a
  directory tree(_TreeInitialization) and a text box with file changes
  (_FileChangehandler textbox widget).

- _DirectoryView - Places splitter widget in a layout and initializes
  files observer object. Main object to create
  this widget.
"""

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


class _FileChangeHandler(QtWidgets.QTextEdit, events.FileSystemEventHandler):

    def __init__(self):
        super(_FileChangeHandler, self).__init__()
        self.setReadOnly(True)
        self.__text = str()

    def on_moved(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.__text = 'Moved {0}: from {1} to {2} \n'.format(
            what, event.src_path, event.dest_path
        )
        self.insertPlainText(self.__text)

    def on_created(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.__text = 'Created {0}: {1} \n'.format(what, event.src_path)
        self.insertPlainText(self.__text)

    def on_deleted(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.__text = 'Deleted {0}: {1} \n'.format(what, event.src_path)
        self.insertPlainText(self.__text)

    def on_modified(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.__text = 'Modified {0}: {1} \n'.format(what, event.src_path)
        self.insertPlainText(self.__text)


class _Splitter(QtWidgets.QSplitter):

    def __init__(self, initial_path, event_handler):
        super(_Splitter, self).__init__()
        self.addWidget(_TreeInitialization(initial_path))
        self.addWidget(event_handler)


class DirectoryView(QtWidgets.QWidget):

    def __init__(self, initial_path):
        super(DirectoryView, self).__init__()
        self.__initial_path = initial_path
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
        vertical_box = QtWidgets.QVBoxLayout()
        vertical_box.addWidget(
            _Splitter(self.__initial_path, self.__event_handler)
        )
        self.setLayout(vertical_box)

    def __del__(self):
        self.__observer.stop()
