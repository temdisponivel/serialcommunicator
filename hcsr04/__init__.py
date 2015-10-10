import hcsr04communicator
import serialcommunicator.serialcommunicator as serialcommunicator

if __name__ == "__main__":
    listener = hcsr04communicator.SupersonicCommunicatorListener()
    serial = serialcommunicator.DefaultCommunicator("COM4", listener)
    serial.start_reading()