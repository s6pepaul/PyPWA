#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import (QVBoxLayout, QFileSystemModel, QTreeView,
                             QApplication)
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QDir


class DirView(QTreeView):

    def __init__(self):
        super(DirView, self).__init__()
        self.__initui()

    def __initui(self):
        self.setGeometry(300, 300, 600, 480)
        self.setWindowTitle('Home Directory View')
        self.setWindowIcon(QIcon('web.png'))


        #set model attributes
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.homePath())


        #define QTreeView as a QFileSystem model
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.homePath()))
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setWindowTitle("Dir View")
        self.tree.resize(600, 480)

        #make path bold
        self.doubleClicked.connect(self.__fileClicked)

        #set properties of the window, display widget
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)

    def __fileClicked(self, signal):
        file_path = QDir.currentPath()
        print(file_path)
        '''        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            self.myFont = QFont(fname[0])
            self.myFont.setBold(enable=True) '''




if __name__ == '__main__':
    app = QApplication(sys.argv)
    dv = DirView()
    dv.show()
    sys.exit(app.exec_())
