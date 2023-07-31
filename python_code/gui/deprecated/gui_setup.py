# import threading
# from queue import Queue
import sys
import os
import json
from PyQt5 import QtWidgets, uic

# from gui import T8WordMatching
# from gui.gui_thread import Gui
# from sensor.sensor_thread import SensorReader
# from mouse.mouse_control import MouseControl
# from utils import init_sensors
# from utils import calibrate_keyboard

# from pyqtgraph import PlotWidget, plot
# import pyqtgraph as pg
# from scipy import signal
# import numpy as np


# TRIGGER_THRESHOLD_FACTOR = 0.75#0.9
# RELEASE_THRESHOLD_FACTOR = 0.5#0.62
# MOUSE_TRIGGER_THRESHOLD_FACTOR = 0.7#0.8
# MOUSE_RELEASE_THRESHOLD_FACTOR = 0.375
# PEAK_THRESHHOLD = 250


class SetupGUI(QtWidgets.QDialog):
    def __init__(self, event, mouse_queue, gui_queue):
        super(SetupGUI, self).__init__()
        self.event = event
        self.mouse_queue = mouse_queue
        self.gui_queue = gui_queue

        # print(os.path.join(os.getcwd(), 'python_code', 'ui', 'setup_dialog.ui'))
        # print(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ui', 'setup_dialog.ui'))
        # print(os.path.join(os.path.dirname(sys.executable), 'ui', 'setup_dialog.ui'))
        # if '_MEIPASS2' in os.environ:
        #     print(os.path.join(os.environ["_MEIPASS2"], 'ui', 'setup_dialog.ui'))

        uic.loadUi(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ui', 'setup_dialog_v4.ui'), self)

        # Dialog buttons
        self.pushButton_load_parameter.clicked.connect(lambda: self.loadParameters())
        self.pushButton_save_parameter.clicked.connect(lambda: self.saveParameters())
        self.pushButton_accept.clicked.connect(lambda: self.acceptParameters())


    def loadParameters(self):
        """Loads parameters from json file
        """
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Parameter File", "", "JSON File (*.json)", options=options)
        if fileName:
            with open(fileName, 'r') as f:
                parameter = json.load(f)
                self.spinbox_mouse_trigger_threshold.setValue(parameter['mouse_trigger_threshold'])
                self.spinbox_mouse_release_threshold.setValue(parameter['mouse_release_threshold'])
                self.spinbox_left_boundary.setValue(parameter['mouse_left_boundary'])
                self.spinbox_right_boundary.setValue(parameter['mouse_right_boundary'])
                self.spinbox_upper_boundary.setValue(parameter['mouse_upper_boundary'])
                self.spinbox_lower_boundary.setValue(parameter['mouse_lower_boundary'])
                self.spinbox_scroll_up_trigger.setValue(parameter['scroll_up_trigger'])
                self.spinbox_scroll_up_release.setValue(parameter['scroll_up_release'])
                self.spinbox_scroll_down_trigger.setValue(parameter['scroll_down_trigger'])
                self.spinbox_scroll_down_release.setValue(parameter['scroll_down_release'])
                self.spinbox_scroll_speed.setValue(parameter['scroll_speed'])

                self.spinbox_trigger_threshold.setValue(parameter['keyboard_trigger_threshold'])
                self.spinbox_release_threshold.setValue(parameter['keyboard_release_threshold'])
                self.spinbox_long_press_duration.setValue(parameter['long_press_duration'])
                self.spinbox_retrigger_duration.setValue(parameter['retrigger_duration'])    


    def saveParameters(self):
        """Saves parameters to json file
        """
        parameter = {}
        parameter['mouse_trigger_threshold'] = self.spinbox_mouse_trigger_threshold.value()
        parameter['mouse_release_threshold'] = self.spinbox_mouse_release_threshold.value()
        parameter['mouse_left_boundary'] = self.spinbox_left_boundary.value()
        parameter['mouse_right_boundary'] = self.spinbox_right_boundary.value()
        parameter['mouse_upper_boundary'] = self.spinbox_upper_boundary.value()
        parameter['mouse_lower_boundary'] = self.spinbox_lower_boundary.value()
        parameter['scroll_up_trigger'] = self.spinbox_scroll_up_trigger.value()
        parameter['scroll_up_release'] = self.spinbox_scroll_up_release.value()
        parameter['scroll_down_trigger'] = self.spinbox_scroll_down_trigger.value()
        parameter['scroll_down_release'] = self.spinbox_scroll_down_release.value()
        parameter['scroll_speed'] = self.spinbox_scroll_speed.value()

        parameter['keyboard_trigger_threshold'] = self.spinbox_trigger_threshold.value()
        parameter['keyboard_release_threshold'] = self.spinbox_release_threshold.value()
        parameter['long_press_duration'] = self.spinbox_long_press_duration.value()
        parameter['retrigger_duration'] = self.spinbox_retrigger_duration.value()

        # Save dialog
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Parameter File", "", "JSON File (*.json)", options=options)
        if fileName:
            with open(fileName, 'w') as f:
                json.dump(parameter, f)            


    def acceptParameters(self):
        """Accept currently set parameters for application usage
        """
        self.mouse_trigger_threshold = self.spinbox_mouse_trigger_threshold.value()
        self.mouse_release_threshold = self.spinbox_mouse_release_threshold.value()
        self.mouse_left_boundary = self.spinbox_left_boundary.value()
        self.mouse_right_boundary = self.spinbox_right_boundary.value()
        self.mouse_upper_boundary = self.spinbox_upper_boundary.value()
        self.mouse_lower_boundary = self.spinbox_lower_boundary.value()
        self.scroll_up_trigger = self.spinbox_scroll_up_trigger.value()
        self.scroll_up_release = self.spinbox_scroll_up_release.value()
        self.scroll_down_trigger = self.spinbox_scroll_down_trigger.value()
        self.scroll_down_release = self.spinbox_scroll_down_release.value()
        self.scroll_speed = self.spinbox_scroll_speed.value()

        self.keyboard_trigger_threshold = self.spinbox_trigger_threshold.value()
        self.keyboard_release_threshold = self.spinbox_release_threshold.value()
        self.long_press_duration = self.spinbox_long_press_duration.value()
        self.retrigger_duration = self.spinbox_retrigger_duration.value()
        
        self.close()
        