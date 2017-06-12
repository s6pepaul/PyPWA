import pytest
import sys
import os

sys.path.append(".")

from GUIs.directoryGUI import _DirectoryWatcher


@pytest.fixture()
def file_watcher():
    return _DirectoryWatcher(sys.path[-1])


def test_detects_file_change(file_watcher):
    open("testfile", "w").close()
    files = file_watcher.get_changed_files()
    assert "testfile" in files
    os.remove("testfile")
    assert "testfile" in files
