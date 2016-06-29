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
import argparse
import os
import sys

from PyPWA.configuratr import internal_logging
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class StartConfiguratr(object):
    def __init__(self, builder, *args):
        self.builder = builder(args)

    def __call__(self, function):
        def decorated_builder(*args):
            application_configuration = function(args)
            if application_configuration["Extras"]:
                return
            arguments = self.parse_arguments(application_configuration)

            if arguments.WriteConfig:
                self.write_config(application_configuration["Configuration"],
                                  application_configuration["Python File"])

            sys.stdout.write("\x1b[2J\x1b[H")

            self.builder.run(application_configuration["Calculation"],
                             arguments.configuration)

        return decorated_builder()

    @staticmethod
    def parse_arguments(app_config):
        parser = argparse.ArgumentParser(description=app_config["Description"])
        parser.add_argument("configuration", type=str, default="", nargs="?")
        parser.add_argument("--WriteConfig", "-wc", action="store_true",
                            help="Write an example configuration to the current"
                                 " working directory")

        parser.add_argument("--Version", "-V", action="version",
                            version="%(prog)s (version " + __version__ + ")")
        parser.add_argument("--verbose", "-v", action="count",
                            help="Adds logging, defaults to errors, "
                                 "then setups up on from there. -v will "
                                 "include warning, -vvv will show debugging.")

        if app_config["AdvancedHelp"]:
            parser.add_argument("--AdvancedHelp", "-ah", action="store_true",
                                help="Prints the in depth advanced help to "
                                     "the terminal")

        arguments = parser.parse_args()

        if arguments.verbose == 1:
            internal_logging.define_logger(logging.WARNING)
        elif arguments.verbose == 2:
            internal_logging.define_logger(logging.INFO)
        elif arguments.verbose >= 3:
            internal_logging.define_logger(logging.DEBUG)
        else:
            internal_logging.define_logger(logging.ERROR)

        if app_config["AdvancedHelp"] and arguments.AdvancedHelp:
            raise NotImplementedError("Currently advanced help output is "
                                      "undeveloped")

        if not arguments.WriteConfig and arguments.configuration == "":
            parser.print_help()

        return arguments

    @staticmethod
    def write_config(configuration, python, cwd=os.getcwd()):
        with open(cwd + "/Example.yml", "w") as stream:
            stream.write(configuration)
        with open(cwd + "/Example.py", "w") as stream:
            stream.write(python)