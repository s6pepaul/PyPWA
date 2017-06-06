#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import os

from PyQt5.QtWidgets import (QVBoxLayout, QFileSystemModel, QTreeView,
                             QApplication, QTextEdit, QSplitter, QPushButton)
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QDir, QObject, pyqtSignal, Qt


class DirView(QTreeView):

    def __init__(self):
        super(DirView, self).__init__()
        self.__old_files = None
        self.__initui()

    def __initui(self):
        self.setGeometry(300, 300, 600, 580)
        self.setWindowTitle('Home Directory View')
        self.setWindowIcon(QIcon('web.png'))
        self.__defining_tree()
        self.textbox = QTextEdit()
        self.textbox.setReadOnly(True)

        self.__old_files = self.__make_list_of_files()

        btn = QPushButton('Recently Added Files', self)
        btn.clicked.connect(self.__file_added_event)
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.tree)
        splitter1.addWidget(self.textbox)

        windowlayout = QVBoxLayout(self)
        windowlayout.addWidget(splitter1)
        windowlayout.addWidget(btn)

        self.setLayout(windowlayout)
        self.show()

    def __creating_model(self):
        # set model attributes
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.homePath())
        return self.model

    def __defining_tree(self):
        # define QTreeView widget as a QFileSystem model
        self.tree = QTreeView()
        self.tree.setModel(self.__creating_model())
        self.tree.setRootIndex(self.model.index(QDir.homePath()))
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setWindowTitle("Dir View")

    def __make_list_of_files(self):
        path1 = '/home/cjbanks/dir1'
        orig_files = []
        with os.scandir(path1) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    orig_files.append(entry.name)
        return orig_files

    # this defines the signal
    def __file_added_event(self):
        new_files = []

        with os.scandir('/home/cjbanks/dir1') as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    new_files.append(entry.name)

        for filename in new_files:
            if filename not in self.__old_files:
                self.textbox.textCursor().insertText(filename+'\n')

        if new_files == self.__old_files:
            self.textbox.textCursor().insertText('No New Files \n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dv = DirView()
    sys.exit(app.exec_())
