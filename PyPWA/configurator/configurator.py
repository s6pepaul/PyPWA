#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This file is the main file for all of PyPWA. This file takes a
configuration file, processes it, then contacts the main module that is
requested to determine what information is needed to be loaded and how it needs
to be structured to be able to function in the users desired way.
"""

import logging

from PyPWA.libs import (process, data, minimizers)
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Configurator(object):

    _builtin_libraries = [process, data, minimizers]

    def __init__(self, starter):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._starter = starter