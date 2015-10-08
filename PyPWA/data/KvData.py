#!/usr/bin/env python

"""
KvData.py: A class that loads the kinematic variables from a text file and saves the data from the
calculations
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond"]
__license__ = "MIT"
__version__ = "0.6"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Alpha"

import fileinput, numpy, os, pickle, hashlib

class KvData(object):
    """
    This class reads and writes data from and to a Numpy Array.
    Data is accessible threw event_one and event_two
    """
    
    def __init__(self, config):
        """
        Sets the configuration
        """
        self.config = config


    def parse(self, data_type ):
        """
        A simple wrapper for parse_events and parse_qfactor, also checks for a cache and loads it if valid.

        params: data_type = type of data being parsed (data,accepted,qfactor)
        """
        if self.config["Use Cache"]:
            file_location = self.return_location(data_type)
            cache_location = self.cache_location(file_location)
            the_cache = self.load_cache(cache_location)
            the_hash = self.find_hash(file_location)
            if self.cache_success and the_hash == the_cache["files_hash"]:
                self.values = the_cache
        else:
            self.cache_success = None


        if not self.cache_success or self.cache_success == None:
            if data_type == "data" or data_type == "accepted":
                self.parse_events(data_type)
            elif data_type == "qfactor":
                self.parse_qfactor()
            elif data_type == "all":
                #todo, add threaded loading from disk
                pass
        if self.cache_success == False:
            self.values["files_hash"] = the_hash
            self.make_cache(self.values, cache_location)
        

    def parse_events(self, data_type):
        """
        This method loads the the events into two separate Numpy Arrays
        If you can find a better way of doing this please let me know

        Stores the values into self.values
        
        params: data_type = type of data being parsed (data,accepted)
        """

        data_file = self.return_location(data_type)


        length = self.file_length(data_file)

        with open(data_file, 'r') as the_file:
            first_line = the_file.readline().strip("\n")

        self.values = {}
        for x in range(len(first_line.split(","))):
            self.values[first_line.split(",")[x].split("=")[0]] = numpy.zeros(shape=length, dtype="float64")

        count = 0
        for line in fileinput.input([data_file]):
            the_line = line.strip("\n")

            for x in range(len(line.split(","))):
                self.values[the_line.split(",")[x].split("=")[0]][count] = numpy.float64(the_line.split(",")[x].split("=")[1])
            count += 1
        print("Finished loading " + data_type + " from " + data_file )


    def parse_qfactor(self):
        """
        This method is for parsing the Qfactors into a numpy array, stores the value in self.values["qfactor"]
        """

        if not self.config["Use QFactor"]:
            self.values = 1
            return 0

        data_file = self.config["QFactor List Location"]

        self.values = {}
        length = self.file_length(data_file)
        self.values["qfactor"] = numpy.zeros(shape=length, dtype="float64")

        count = 0
        for line in fileinput.input([data_file]):
            self.values["qfactor"][count] = numpy.float64(line)
            count += 1
        print("Finished loading qfactor from " + data_file )


    def file_length(self, file_name ):
        """
        Methods determines how many lines are in a file.
        params: file_name = the path to the file
        """
        try:
            with open(file_name) as the_file:
                for length, l in enumerate(the_file):
                    pass
            return length + 1
        except IOError:
            raise AttributeError(file_name + " doesn't exsist. Please check your configuration and try again.")

    def find_hash(self, the_file):
        """
        Fetches the hash for the data that is to be stored.

        Args: the_file - The file which you wish to find the hash too
        """
        try:   
            with open(the_file, "r") as a_file:
                for line in a_file.readlines():
                    line = line.strip("\n")
                    the_hash = hashlib.sha256(line)
        except IOError:
            raise AttributeError(the_file + " doesn't exsist. Please check your configuration and try again.")
        return the_hash.hexdigest()

 
    def cache_location(self, file_location):
        """
        Just fetches the location of the cache based off of the location of the original file.

        Params: file_location: the location of the original file.
        """
        the_path = file_location.split("/")
        path_length = len(the_path) - 1
        file_name = the_path[path_length]
        file_name = os.path.splitext(file_name)[0]
        file_name = "." + file_name + ".pickle-cache"
        the_path[path_length] = file_name
        return "/".join(the_path)

        

    def make_cache(self, data, the_file):
        """
        Writes the cache to file.

        Params: the_file: The location where you want the cache to be written.
        """
        with open(the_file, "wb") as a_file:
            pickle.dump(data, a_file, protocol=pickle.HIGHEST_PROTOCOL)


    def load_cache(self, the_file):
        """
        Attempts to load the cache if present.

        Params: the_file: The location of the cache.
        """
        try:
            with open(the_file, "r")  as a_file:
                cache = pickle.load(a_file)
            self.cache_success = True
            return cache
        except EOFError:
            self.cache_success = False
            return {"files_hash":0}
        except IOError:
            self.cache_success = False
            return {"files_hash":0}

    def return_location(self, data_type ):
        """
        Wrapper for data types, takes the data type, and returns the location of the requested file.

        Params: data_type: "data", "accepted", or "qfactor".
        """
        if data_type == "data":
            return self.config['Kinematic Variable File']
        elif data_type == "accepted":
            return self.config['Accepted Kinematic Variable File']
        elif data_type == "qfactor":
            return self.config["QFactor List Location"]
        else:
            return 0