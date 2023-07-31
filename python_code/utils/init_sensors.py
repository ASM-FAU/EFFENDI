import glob
import sys
import serial


# a function that allows you to list all active ports
# If the code runs on WINDOWS
def main():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]

    # If the code runs on LINUX
    elif sys.platform.startswith('linux'):
        ports = glob.glob('/dev/tty[A-Za-z]*')

    else:
        raise EnvironmentError('Unsupported Platform.')

    # Test the ports that are active and add them as a result
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            return port
        except (OSError, serial.SerialException):
            pass

    raise EnvironmentError('No connected device found.')
