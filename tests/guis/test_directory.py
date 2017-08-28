import os
import time

import pytest
from watchdog import observers

from PyPWA.guis import directory


@pytest.fixture()
def directory_view():
    directory_view_object = directory.DirectoryView('.')
    yield directory_view_object
    directory_view_object.stop()


def test_directory_view(qtbot, directory_view):
    qtbot.addWidget(directory_view)
    assert qtbot.waitExposed(directory_view, timeout=1000)


@pytest.fixture()
def tree_viewer():
    return directory._TreeInitialization('.')


def test_tree_opens(qtbot, tree_viewer):
    qtbot.addWidget(tree_viewer)
    assert qtbot.waitExposed(tree_viewer, timeout=1000)


@pytest.fixture()
def text_box_handler():
    return directory._FileChangeHandler()


@pytest.fixture()
def dir_thread(text_box_handler):
    directory_thread = observers.Observer()
    directory_thread.schedule(text_box_handler, '.', recursive=True)
    directory_thread.start()
    yield text_box_handler
    directory_thread.stop()


def test_text_box_output(dir_thread):
    with open('file2.txt', 'w+'):
        time.sleep(.5)
        os.rename('file2.txt', 'file3.txt')
        time.sleep(.2)
        assert 'file2.txt' in dir_thread.toPlainText()
        os.remove('file3.txt')
