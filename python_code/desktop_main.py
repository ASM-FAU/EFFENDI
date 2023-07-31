import threading
from queue import Queue
import sys
from PyQt5 import QtWidgets

from gui.T8WordMatching import T8WordMatching
from gui.gui_thread_desktop import DesktopGui
from gui.gui_setup_desktop import SetupDesktopGUI
from sensor.sensor_thread import SensorReader
from utils import init_sensors

from mouse.mouse_control import MouseControl


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
        desktop = True

        sensor = SensorReader("Sensor Reader", connected_device_port, event, mouse_queue, gui_queue, write_queue, desktop)
        sensor.start()

        setup_gui = SetupDesktopGUI(event, mouse_queue, gui_queue)
        setup_gui.show()
        setup_gui.exec_()

        t8_word_matching = T8WordMatching(setup_gui.language, setup_gui.dict_path, setup_gui.keyboard_layout)   # load and optimize library

        setup_gui.close()

        gui = DesktopGui("Keyboard", event, gui_queue, write_queue, t8_word_matching, setup_gui.keyboard_trigger_sensitivity, setup_gui.keyboard_release_sensitivity, setup_gui.keyboard_pressure, setup_gui.long_press_duration, setup_gui.retrigger_duration, setup_gui.keyboard_layout, setup_gui.next_key_idx, setup_gui.space_key_idx)
    
        if setup_gui.disable_mouse is False:
            mouse = MouseControl("Mouse Control", True, gui, setup_gui.mouse_left_boundary, setup_gui.mouse_right_boundary, setup_gui.mouse_lower_boundary, setup_gui.mouse_upper_boundary, setup_gui.mouse_click_sensitivity_f, setup_gui.mouse_click_sensitivity_p, setup_gui.mouse_release_sensitivity_f, setup_gui.mouse_release_sensitivity_p, setup_gui.mouse_cursor_sensitivity, setup_gui.scroll_up_trigger, setup_gui.scroll_down_trigger, setup_gui.scroll_release_sensitivity, setup_gui.scroll_speed, setup_gui.right_click_duration, setup_gui.recenter_mouse_duration, setup_gui.tolerated_mouse_movement, setup_gui.trigger_mouse_down, setup_gui.mouse_acceleration, event, mouse_queue, write_queue, setup_gui.proximity_sensor)
            mouse.start()
        
        if setup_gui.hide_ui is False:
            gui.ui.show()
        elif setup_gui.hide_ui is True:
            gui.ui.hide()
        gui.gui.exec_()

        sensor.join()

    except (KeyboardInterrupt, SystemExit):
        print("Program cancelled due to keyboard interruption.")
        sys.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main()
    sys.exit(app.exec_())
