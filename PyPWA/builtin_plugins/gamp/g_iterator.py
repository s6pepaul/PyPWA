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
Gamp data reading and writing.

This file holds the Gamp Reader and Gamp Writer. These simply load the
data into memory one event at a time and write to file one event at a
time. Only the previous loaded events are stored, anything later than that
will not be saved in memory by these object.
"""

import io

import numpy

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs import misc_file_libs
from PyPWA.libs.components.data_processor import data_templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class GampParticleCount(object):

    def __init__(self):
        self.__particle_count = 0

    def get_particle_count(self, file_location):
        # type: (Path) -> None
        particle_count = self.__get_particle_count(file_location)
        file_length = misc_file_libs.get_file_length(file_location)
        self.__particle_count = int(file_length / particle_count)

    @staticmethod
    def __get_particle_count(file_location):
        with file_location.open() as stream:
            return int(stream.readline())

    @property
    def particle_count(self):
        return self.__particle_count


class GampReader(data_templates.Reader):

    def __init__(self, file_location):
        """
        This reads in Gamp events from disk, Gamp events are deque of
        named tuples, each named tuple representing a particle in the
        event.

        Args:
            file_location (Path): Name of the GAMP file, can be any size.
        """
        self.__event_count = None
        self._previous_event = None  # type: numpy.ndarray
        self._the_file = file_location
        self.__particle_count = GampParticleCount()
        self.__particle_count.get_particle_count(file_location)
        self._start_input()

    def _start_input(self):
        """
        Checks to see if the file is opened, and if it is close it so that
        it may be reopened.
        """
        try:
            if self._file:
                self._file.close()
        except AttributeError:
            pass
        self._file = self._the_file.open("rt")

    def reset(self):
        """
        Calls the _start_input method again which will close the file then
        reopen it back at the beginning of the file.
        """
        self._start_input()

    def next(self):
        """
        Structures the read in event from the GAMP file into a deque then
        passes it to the calling function.

        Returns:
            deque: The next deque event.

        Raises:
            StopIterator: End of file has been found.
        """
        first_line = self._file.readline().strip("\n")
        if first_line == "":
            raise StopIteration
        count = int(first_line)
        event = numpy.zeros((count, 6), numpy.float64)
        for index in range(count):
            event[index] = self._make_particle(self._file.readline())
        self._previous_event = event
        return self._previous_event

    @staticmethod
    def _make_particle(string):
        """
        Takes the string read in from the GAMP event and parses it into a
        named tuple to store the various values. All values are numpy data
        types.

        Args:
            string (str): The string containing the GAMP Particle

        Returns:
            numpy.ndarray: 2 dimensional array,
                [particle_index][particles]
        """
        the_list = string.strip("\n").split(" ")

        particle = numpy.zeros(6, dtype=numpy.float64)
        particle[0] = numpy.float64(the_list[0])  # Particle ID
        particle[1] = numpy.float64(the_list[1])  # Particle Charge
        particle[2] = numpy.float64(the_list[2])  # Particle X Momentum
        particle[3] = numpy.float64(the_list[3])  # Particle Y Momentum
        particle[4] = numpy.float64(the_list[4])  # Particle Z Momentum
        particle[5] = numpy.float64(the_list[5])  # Particle Energy

        return particle

    def get_event_count(self):
        return self.__particle_count.particle_count

    def close(self):
        self._file.close()


class GampWriter(data_templates.Writer):

    def __init__(self, file_location):
        """
        Takes GAMP events one at a time and attempts to write them in a
        standardized way to file so that other programs can read the
        output.

        Args:
            file_location (Path): Where to write the GAMP data.
        """
        self._file = file_location.open("w")

    def write(self, data):
        """
        Writes the events the disk one event at a time, wont close the
        disk access until the close function is called or until the object
        is deleted.

        Args:
            numpy.ndarray: the file that is to be written to disk.
        """
        self._file.write(u"%d\n" % len(data))
        for particle in data:
            self._file.write(u"{0} {1} {2} {3} {4} {5}\n".format(*particle))

    def close(self):
        self._file.close()