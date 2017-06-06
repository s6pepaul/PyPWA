#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import os

from PyQt5.QtWidgets import (QVBoxLayout, QFileSystemModel, QTreeView,
                             QApplication, QTextEdit, QSplitter, QPushButton)
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QDir, QObject, pyqtSignal, Qt

from filecmp import dircmp


class DirView(QTreeView):
    path = '/home/cjbanks/projects'
    dir_diff = dircmp(path, path)

    def __init__(self):
        super(DirView, self).__init__()
        self.__initui()

    def __initui(self):
        self.setGeometry(300, 300, 600, 580)
        self.setWindowTitle('Home Directory View')
        self.setWindowIcon(QIcon('web.png'))
        self.__definingtree()
        self.textbox = QTextEdit()

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

    def __definingtree(self):
        # define QTreeView widget as a QFileSystem model
        self.tree = QTreeView()
        self.tree.setModel(self.__creating_model())
        self.tree.setRootIndex(self.model.index(QDir.homePath()))
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setWindowTitle("Dir View")

    # this defines the signal
    def __file_added_event(self, dir_diff):
        for filename in dir_diff.common_files:
            if not dir_diff.common_files:
                print(filename)
                self.textbox.textCursor().insertText(filename+'\n')
        for sub_dir in dir_diff.subdirs.values():
            self.__file_added_event(sub_dir)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dv = DirView()
    sys.exit(app.exec_())
