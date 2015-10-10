import serialcommunicator


if __name__ == "__main__":
    listener = serialcommunicator.DefaultListener()
    serial = serialcommunicator.DefaultCommunicator("COM4", listener)
    serial.start_reading()