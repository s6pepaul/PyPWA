#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import os

from PyQt5.QtWidgets import (QVBoxLayout, QFileSystemModel, QTreeView,
                             QApplication, QLabel)
from PyQt5.QtGui import QIcon, QFont

from PyQt5.QtCore import QDir, QObject, pyqtSignal


class Signal(QObject):
    FileAdded = pyqtSignal()


class DirView(QTreeView):

    def __init__(self):
        super(DirView, self).__init__()
        self.__initui()

    def __initui(self):
        self.setGeometry(300, 300, 600, 480)
        self.setWindowTitle('Home Directory View')
        self.setWindowIcon(QIcon('web.png'))
        self.__definingtree()
        self.__changestodirectory()
        windowlayout = QVBoxLayout()
        windowlayout.addWidget(self.tree)
        windowlayout.addWidget(self.label)
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
        self.tree.resize(600, 480)

    def __changestodirectory(self):
        self.directorychanged = Signal()
        self.directorychanged.FileAdded.connect(self.__file_added_event)

    #this defines the signal
    def __file_added_event(self, event):
        with os.scandir(QDir.homePath()) as home_path:
            for pathname in home_path:
                if pathname.is_file() and max(home_path, key=os.path.getctime):
                    print(pathname)
                    myFont = QFont()
                    myFont.setBold(True)
                    self.label = QLabel(pathname, self)
                    self.label.setFont(myFont)
                    self.directorychanged.FileAdded.emit()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    dv = DirView()
    sys.exit(app.exec_())
