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
        """
        raise NotImplementedError("This method should be overridden by the inherited class")

    def pause_reading(self):
        """
        PAUSE READING DATA FROM SERIAL PORT
        """
        raise NotImplementedError("This method should be overridden by the inherited class")

    def finish(self):
        """
        STOP READING DATA FROM SERIAL AND FINISH THE THREAD.
        AFTER THIS CALL, YOU SHOULDN'T USE THIS INSTANCE ANYMORE
        """
        raise NotImplementedError("This method should be overridden by the inherited class")

    def set_interval_read(self):
        """
        SET THE INTERVAL WITCH IS USED TO CALL THE CALLBACK FUNCTION WITH DATA FROM SERIAL
        """
        raise NotImplementedError("This method should be overridden by the inherited class")

    def set_interval_read(self):
        """
        GET THE INTERVAL WITCH IS USED TO CALL THE CALLBACK FUNCTION WITH DATA FROM SERIAL
        """
        raise NotImplementedError("This method should be overridden by the inherited class")


""" IMPLEMENTATIONS """


class DefaultCommunicator(Communicator):
    """
    IMPLEMENTS SOME DEFAULT BEHAVIOUR OF A COMMUNICATOR
    """
    def __init__(self, port, listener, baud_rate=9600, timeout=1, interval_read_seconds=1/60):
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

    def set_interval_read(self, interval_seconds):
        self.interval_read = interval_seconds

    def get_interval_read(self):
        return self.interval_read

    def run(self):
        while not self.stop_event.is_set():
            while self.reading:
                if self.listener is not None:
                    self.listener.callback(self.readline())
                time.sleep(self.interval_read)
        self.close()


class DefaultListener(CommunicatorListener):

    def __init__(self):
        CommunicatorListener.__init__(self)
        self.time_read = 0
        self.last_time_read = time.clock()

    def callback(self, data):
        print("TIME:{0} | DATA: {1}".format(self.time_read, data))
        self.time_read = time.clock() - self.last_time_read
        self.last_time_read = self.time_read