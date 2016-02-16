import serial #pyserial
import threading
import time

"""  DEFINITION """


class CommunicatorListener(object):

    """
    Default class for handling callbacks from the communicator
    """

    def __init__(self):
        super(CommunicatorListener, self).__init__()

    def callback(self, data):
        """
        :parameter data: Current line read from serial
        """
        raise NotImplementedError("This method should be overridden by the inherited class")


class Communicator(object):
    """
    DEFINES A COMMUNICATOR THAT WILL INTERACT WITH SERIAL PORT
    """

    def __init__(self):
        super(Communicator, self).__init__()
        self._thread = threading.Thread(target=self._run)
        self._serial = serial.Serial()
        self._interval_read = 0

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

    def _run(self):
        """
        :return: The method that will be the target of the thread.
        """
        raise NotImplementedError("This method should be overridden by the inherited class")

    @property
    def interval_read(self):
        """
        SET THE INTERVAL WITCH IS USED TO CALL THE CALLBACK FUNCTION WITH DATA FROM SERIAL
        :rtype : float
        :return: Interval current used between readings
        :raise: NotImplementedError if this method is call in this base class
        """
        return self._interval_read

    @interval_read.setter
    def interval_read(self, interval_seconds):
        """
        GET THE INTERVAL WITCH IS USED TO CALL THE CALLBACK FUNCTION WITH DATA FROM SERIAL
        :parameter interval: Interval in seconds to use between readings
        :raise:NotImplementedError if this method is call in this base class
        """
        self._interval_read = interval_seconds

    @property
    def thread(self):
        """
        :return: The thread that is running this communicator.
        """
        return self._thread

    @property
    def serial(self):
        """
        :return: The serial object used to communicate.
        """
        return self._serial


""" IMPLEMENTATIONS """


class DefaultCommunicator(Communicator):
    """
    IMPLEMENTS SOME DEFAULT BEHAVIOUR OF A COMMUNICATOR
    """
    def __init__(self, port, listener, baud_rate=9600, timeout=2, interval_read_seconds=1/60.0):
        """
        :param port: Port to read data
        :param listener: Listener to callback when read data from serial. Should implement CommunicatorListener or have
        callback method
        :param baud_rate: Baud rate to connect into port
        :param timeout: Timeout to read data
        :param interval_read_seconds: Interval between readings
        """
        super(DefaultCommunicator, self).__init__()
        self.name = "COMMUNICATOR"
        self._thread.daemon = False
        self._serial.baudrate = baud_rate
        self._serial.port = port
        self._serial.timeout = timeout
        self.listener = listener
        self._reading = False
        self.interval_read = interval_read_seconds
        self._started = False
        self._stop_event = threading.Event()

    def start_reading(self):
        if not self._started:
            self._thread.start()
        self._serial.open()
        self._reading = True

    def pause_reading(self):
        self._reading = False

    def finish(self):
        self.pause_reading()
        self._stop_event.set()

    def _run(self):
        while not self._stop_event.is_set():
            while self._reading:
                try:
                    if self.listener is not None:
                        line = self._serial.readline()
                        if line == '':
                            line = 0
                        self.listener.callback(int(line))
                        time.sleep(self.interval_read)
                except Exception, e:
                    print e
        self._serial.close()

    def __str__(self):
        return "Port: {0} | Baud rate: {1} : {1}".format(self._serial.port, self._serial.baudrate)


class DefaultListener(CommunicatorListener):
    """
    IMPLEMENTS AND EXTENDS THE BEHAVIOUR OF A COMMUNICATOR LISTENER
    """
    def __init__(self):
        CommunicatorListener.__init__(self)
        self._data = []

    def callback(self, data):
        self.data.append(data)

    @property
    def data(self):
        """
        :rtype : list
        :return: A LIST OF ALL DATA RECEIVE FROM START (OR LAST clear_data() call)
        """
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def clear_data(self):
        """
        CLEAR THE LIST DATA OF THIS LISTENER
        """
        self._data = list()

    def __str__(self):
        return self.data