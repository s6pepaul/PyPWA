#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" This is a widget to view a directory and display changes to that directory
 based on a button press.
"""

import sys
import os

from PyQt5.QtWidgets import (QVBoxLayout, QFileSystemModel, QTreeView,
                             QApplication, QTextEdit, QSplitter, QPushButton)

from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (QDir, Qt)


class DirectoryView(QTreeView):

    initial_path = QDir.homePath()

    def __init__(self):
        super(DirectoryView, self).__init__()
        self.__old_files = None
        self.__initui()

    def __initui(self):
        self.__defining_tree()
        self.__old_files = self.__make_list_of_files()
        self.setLayout(self.__set_window_attributes())
        self.show()

    def __defining_tree(self):
        self.tree = QTreeView()                                         
        self.tree.setModel(self.__creating_model())
        self.tree.setRootIndex(self.model.index(DirectoryView.initial_path))
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setWindowTitle("Dir View")
        return None

    def __creating_model(self):
        # set model attributes
        self.model = QFileSystemModel()
        self.model.setRootPath(DirectoryView.initial_path)
        return self.model

    def __make_list_of_files(self):
        original_file_list = []
        with os.scandir(DirectoryView.initial_path) as old_list_of_files:
            for file in old_list_of_files:
                if not file.name.startswith('.') and file.is_file():
                    original_file_list.append(file.name)
        return original_file_list

    def __set_window_attributes(self):
        self.setGeometry(300, 300, 600, 580)       
        self.setWindowTitle('Home Directory View')
        self.setWindowIcon(QIcon('web.png'))
        window_layout = QVBoxLayout(self)
        button = QPushButton('Recently Added Files', self)
        button.clicked.connect(self.__new_file_added_event)
        window_layout.addWidget(self.__make_splitter())
        window_layout.addWidget(button)
        return window_layout

    # compares current source of files to an updated source
    def __new_file_added_event(self):
        new_file_list = []                                                  
        path = QDir.homePath()
        new_file_display = QTextEdit()
        new_file_display.setReadOnly(True)
        with os.scandir(path) as updated_list_of_files:
            for file in updated_list_of_files:
                if not file.name.startswith('.') and file.is_file():
                    new_file_list.append(file.name)

        for filename in new_file_list:
            if filename not in self.__old_files:
                new_file_display.clear()
                new_file_display.textCursor().insertText(filename + '\n')

        if new_file_list == self.__old_files:
            new_file_display.clear()
            new_file_display.textCursor().insertText('No New Files \n')

        return new_file_display

    def __make_splitter(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree)                   
        splitter.addWidget(self.__new_file_added_event())
        return splitter

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dv = DirectoryView()
    sys.exit(app.exec_())
