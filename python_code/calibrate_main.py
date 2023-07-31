import threading
from queue import Queue
import sys
from PyQt5 import QtWidgets

from gui.gui_calibrate import CalibrateGUI
from sensor.sensor_thread import SensorReader
from utils import init_sensors


def main():
    # Search for connected devices
    try:
        connected_device_port = init_sensors.main()
        pass
    except EnvironmentError as error:
        print("Program stopped because of following error: ", error)
        sys.exit()

    try:
        event = threading.Event()
        gui_queue = Queue()
        mouse_queue = Queue()
        write_queue = Queue()
        desktop = False

        sensor = SensorReader("Sensor Reader", connected_device_port, event, mouse_queue, gui_queue, write_queue, desktop)
        sensor.start()

        calibrate_gui = CalibrateGUI(event, mouse_queue, gui_queue, write_queue)
        calibrate_gui.show()
        calibrate_gui.exec_()
        sensor.join()
        # print(calibrate_gui.is_alive())
        calibrate_gui.join()

    except (KeyboardInterrupt, SystemExit):
        print("Program cancelled due to keyboard interruption.")
        sys.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main()
    sys.exit(app.exec_())
