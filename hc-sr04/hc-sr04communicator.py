__author__ = 'matheus'

import time
import serialcommunicator.serialcommunicator as communicator


class SupersonicData(object):
    """
    DEFINES USEFUL DATA WHEN USING SUPERSONIC SENSOR
    """
    def __init__(self, time, raw_data):
        self.time = time
        self.centimeter = raw_data
        self.inches = raw_data
        self.raw = raw_data

    def __str__(self):
        return "Time: {0} | Centimeters: {1} | Inches: {2} | Raw: {3}".format(self.time, self.centimeter,
                                                                              self.inches, self.raw)


class SupersonicCommunicatorListener(communicator.DefaultListener):
    """
    DEFINES A USEFUL LISTENER WHEN USING SUPERSONIC SENSOR
    """
    def __init__(self):
        communicator.DefaultListener.__init__()
        self.time_read = 0
        self.last_read = 0

    def callback(self, data):
        self.time_read = time.clock() - self.last_read
        supersonic_data = SupersonicData(time=self.time_read, raw_data=data)
        communicator.DefaultListener.callback(self, supersonic_data)
        self.last_read = self.time_read