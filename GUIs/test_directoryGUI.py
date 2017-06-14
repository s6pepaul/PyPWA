import os
import PyQt5
import pytest
import sys
import logging


from PyQt5 import QtCore
from GUIs import directoryGUI
from testfixtures import LogCapture

@pytest.fixture()
def main_window():
    return directoryGUI._MainWindow()


def test_main_window_opens(qtbot, main_window):
    qtbot.addWidget(main_window)
    qtbot.waitExposed(main_window, timeout=1000)


@pytest.fixture()
def directory_view():
    return directoryGUI._DirectoryView('.')


def test_directory_view(qtbot, directory_view):
    qtbot.addWidget(directory_view)
    qtbot.waitExposed(directory_view, timeout=1000)


@pytest.fixture()
def tree_viewer():
    return directoryGUI._TreeInitialization('.')


def test_tree_opens(qtbot, tree_viewer):
    qtbot.addWidget(tree_viewer)
    qtbot.waitExposed(tree_viewer, timeout=1000)


@pytest.fixture()
def text_box():
    return directoryGUI._TextBoxHandler()


