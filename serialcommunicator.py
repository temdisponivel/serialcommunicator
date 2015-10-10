import serial
import threading
import time

"""  DEFINITION """


class CommunicatorListener(object):

    def callback(self, data):
        raise NotImplementedError("This method should be overridden by the inherited class")


class Communicator(threading.Thread, serial.Serial):
    """
    DEFINES A COMMUNICATOR THAT WILL INTERACT WITH SERIAL PORT
    """

    def start_reading(self):
        """
        START READING DATA FROM SERIAL PORT
        :raise:NotImplementedError if this method is call in this base class
        """
        raise NotImplementedError("This method should be overridden by the inherited class")

    def pause_reading(self):
        """
        PAUSE READING DATA FROM SERIAL PORT
        :raise:NotImplementedError if this method is call in this base class
        """
        raise NotImplementedError("This method should be overridden by the inherited class")

    def finish(self):
        """
        STOP READING DATA FROM SERIAL AND FINISH THE THREAD.
        AFTER THIS CALL, YOU SHOULDN'T USE THIS INSTANCE ANYMORE
        :raise:NotImplementedError if this method is call in this base class
        """
        raise NotImplementedError("This method should be overridden by the inherited class")

    @property
    def get_interval_read(self):
        """
        SET THE INTERVAL WITCH IS USED TO CALL THE CALLBACK FUNCTION WITH DATA FROM SERIAL
        :rtype : float
        :raise:NotImplementedError if this method is call in this base class
        """
        raise NotImplementedError("This method should be overridden by the inherited class")

    @property
    def set_interval_read(self):
        """
        GET THE INTERVAL WITCH IS USED TO CALL THE CALLBACK FUNCTION WITH DATA FROM SERIAL
        :raise:NotImplementedError if this method is call in this base class
        """
        raise NotImplementedError("This method should be overridden by the inherited class")


""" IMPLEMENTATIONS """


class DefaultCommunicator(Communicator):
    """
    IMPLEMENTS SOME DEFAULT BEHAVIOUR OF A COMMUNICATOR
    """
    def __init__(self, port, listener, baud_rate=9600, timeout=1, interval_read_seconds=1.0/60.0):
        threading.Thread.__init__(self)
        serial.Serial.__init__(self)
        self.name = "COMMUNICATOR"
        self.daemon = False
        self.setBaudrate(baud_rate)
        self.setPort(port)
        self.setTimeout(timeout)
        self.listener = listener
        self.reading = False
        self.interval_read = interval_read_seconds
        self.stop_event = threading.Event()
        self.start()

    def start_reading(self):
        self.open()
        self.reading = True

    def pause_reading(self):
        self.reading = False

    def finish(self):
        self.pause_reading()
        self.stop_evento.set()

    def get_interval_read(self):
        return self.interval_read

    def set_interval_read(self, interval_seconds):
        self.interval_read = interval_seconds

    def run(self):
        while not self.stop_event.is_set():
            while self.reading:
                if self.listener is not None:
                    self.listener.callback(self.readline())
                time.sleep(self.interval_read)
        self.close()

    def __str__(self):
        return "Port: {0} | Baud rate: {1} : {1}".format(self.port, self.baudrate)


class DefaultListener(CommunicatorListener):
    """
    IMPLEMENTS AND EXTENDS THE BEHAVIOUR OF A COMMUNICATOR LISTENER
    """
    def __init__(self):
        CommunicatorListener.__init__(self)
        self.data = list()

    def callback(self, data):
        print("Data: {0}".format(data))
        self.data.append(data)

    @property
    def get_data(self):
        """
        :rtype : list
        :return: A LIST OF ALL DATA RECEIVE FROM START (OR LAST clear_data() call)
        """
        return self.data

    def clear_data(self):
        """
        CLEAR THE LIST DATA OF THIS LISTENER
        """
        self.data = list()

    def __str__(self):
        concat_data = ""
        for d in self.data:
            concat_data += str(d)
        return concat_data