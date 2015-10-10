import time
import serialcommunicator.serialcommunicator as communicator


class SupersonicData(object):
    """
    DEFINES USEFUL DATA WHEN USING SUPERSONIC SENSOR
    """
    def __init__(self, time_read, raw_data):
        """
        :param time_read: Time of the reading. Should be incremental of every read since the beginning
        :param raw_data: Data get from serial
        """
        self.time = time_read
        self.centimeter = float(raw_data) / 29.0 / 2
        self.raw = raw_data

    def get_time(self):
        """
        :return: Time of reading of this data
        """
        return self.time

    def get_centimeter(self):
        """
        :return: The equivalent value of the data in centimeter. Calculate using DATA/29.0/2
        """
        return self.centimeter

    def get_raw(self):
        """
        :return: The raw data read from serial
        """
        return self.raw

    def __str__(self):
        return "Time: {0} | Centimeters: {1} | Raw: {2}".format(self.time, self.centimeter, self.raw)


class SupersonicCommunicatorListener(communicator.DefaultListener):
    """
    DEFINES A USEFUL LISTENER WHEN USING SUPERSONIC SENSOR
    """
    def __init__(self):
        communicator.DefaultListener.__init__(self)
        self.time_read = 0
        self.last_read = 0

    def callback(self, data):
        self.time_read = time.clock() - self.last_read
        self.last_read = self.time_read
        try:
            fdata = float(data)
            supersonic_data = SupersonicData(time_read=self.time_read, raw_data=fdata)
            communicator.DefaultListener.callback(self, supersonic_data)
        except Exception as ex:
            print(ex)