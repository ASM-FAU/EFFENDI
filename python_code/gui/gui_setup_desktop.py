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


# TRIGGER_THRESHOLD_FACTOR = 0.9
# RELEASE_THRESHOLD_FACTOR = 0.62
# MOUSE_TRIGGER_THRESHOLD_FACTOR = 0.8
# MOUSE_RELEASE_THRESHOLD_FACTOR = 0.375
# PEAK_THRESHHOLD = 250


class SetupDesktopGUI(QtWidgets.QDialog):
    def __init__(self, event, mouse_queue, gui_queue):
        super(SetupDesktopGUI, self).__init__()
        self.event = event
        self.mouse_queue = mouse_queue
        self.gui_queue = gui_queue
        self.keyboard_layout = [None]*10
        self.keyboard_trigger_sensitivity = [None]*10
        self.keyboard_pressure = [None]*10
        self.next_key_idx = None
        self.space_key_idx = None
        self.dict_path = ""

        uic.loadUi(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ui', 'setup_dialog_v4.ui'), self)

        # Dialog buttons
        self.pushButton_load_parameter.clicked.connect(lambda: self.loadParameters())
        self.pushButton_save_parameter.clicked.connect(lambda: self.saveParameters())
        self.pushButton_accept.clicked.connect(lambda: self.acceptParameters())

        self.pushButton_load_dict.clicked.connect(lambda: self.loadDictionary())


    def loadParameters(self):
        """Loads parameters from json file
        """
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Parameter File", "", "JSON File (*.json)", options=options)
        if fileName:
            with open(fileName, 'r') as f:
                parameter = json.load(f)
                # Mouse
                self.spinbox_mouse_click_sensitivity_f.setValue(parameter['mouse_click_sensitivity_f'])
                self.spinbox_mouse_pressure_f.setValue(parameter['mouse_pressure_f'])
                self.spinbox_mouse_release_sensitivity_f.setValue(parameter['mouse_release_sensitivity_f'])
                self.spinbox_mouse_click_sensitivity_p.setValue(parameter['mouse_click_sensitivity_p'])
                self.spinbox_mouse_pressure_p.setValue(parameter['mouse_pressure_p'])
                self.spinbox_mouse_release_sensitivity_p.setValue(parameter['mouse_release_sensitivity_p'])
                self.spinbox_mouse_cursor_sensitivity.setValue(parameter['mouse_cursor_sensitivity'])
                # Screen
                self.spinbox_left_boundary.setValue(parameter['mouse_left_boundary'])
                self.spinbox_right_boundary.setValue(parameter['mouse_right_boundary'])
                self.spinbox_upper_boundary.setValue(parameter['mouse_upper_boundary'])
                self.spinbox_lower_boundary.setValue(parameter['mouse_lower_boundary'])
                # Scroll
                self.spinbox_scroll_up_trigger.setValue(parameter['scroll_up_trigger'])
                self.spinbox_scroll_down_trigger.setValue(parameter['scroll_down_trigger'])
                self.spinbox_scroll_release_sensitivity.setValue(parameter['scroll_release_sensitivity'])
                self.spinbox_scroll_speed.setValue(parameter['scroll_speed'])
                # Keyboard
                self.next_key_idx = parameter['keyboard_next_key_idx']
                self.space_key_idx = parameter['keyboard_space_key_idx']

                self.keyboard_layout[0] = parameter['keyboard_layout_lp']
                self.keyboard_layout[1] = parameter['keyboard_layout_lr']
                self.keyboard_layout[2] = parameter['keyboard_layout_lm']
                self.keyboard_layout[3] = parameter['keyboard_layout_li']
                self.keyboard_layout[4] = parameter['keyboard_layout_lt']
                self.keyboard_layout[5] = parameter['keyboard_layout_rt']
                self.keyboard_layout[6] = parameter['keyboard_layout_ri']
                self.keyboard_layout[7] = parameter['keyboard_layout_rm']
                self.keyboard_layout[8] = parameter['keyboard_layout_rr']
                self.keyboard_layout[9] = parameter['keyboard_layout_rp']

                self.spinbox_trigger_sensitivity_lp.setValue(parameter['keyboard_trigger_sensitivity_lp'])
                self.spinbox_trigger_sensitivity_lr.setValue(parameter['keyboard_trigger_sensitivity_lr'])
                self.spinbox_trigger_sensitivity_lm.setValue(parameter['keyboard_trigger_sensitivity_lm'])
                self.spinbox_trigger_sensitivity_li.setValue(parameter['keyboard_trigger_sensitivity_li'])
                self.spinbox_trigger_sensitivity_lt.setValue(parameter['keyboard_trigger_sensitivity_lt'])
                self.spinbox_trigger_sensitivity_rp.setValue(parameter['keyboard_trigger_sensitivity_rp'])
                self.spinbox_trigger_sensitivity_rr.setValue(parameter['keyboard_trigger_sensitivity_rr'])
                self.spinbox_trigger_sensitivity_rm.setValue(parameter['keyboard_trigger_sensitivity_rm'])
                self.spinbox_trigger_sensitivity_ri.setValue(parameter['keyboard_trigger_sensitivity_ri'])
                self.spinbox_trigger_sensitivity_rt.setValue(parameter['keyboard_trigger_sensitivity_rt'])

                self.spinbox_keyboard_pressure_lp.setValue(parameter['keyboard_pressure_lp'])
                self.spinbox_keyboard_pressure_lr.setValue(parameter['keyboard_pressure_lr'])
                self.spinbox_keyboard_pressure_lm.setValue(parameter['keyboard_pressure_lm'])
                self.spinbox_keyboard_pressure_li.setValue(parameter['keyboard_pressure_li'])
                self.spinbox_keyboard_pressure_lt.setValue(parameter['keyboard_pressure_lt'])
                self.spinbox_keyboard_pressure_rp.setValue(parameter['keyboard_pressure_rp'])
                self.spinbox_keyboard_pressure_rr.setValue(parameter['keyboard_pressure_rr'])
                self.spinbox_keyboard_pressure_rm.setValue(parameter['keyboard_pressure_rm'])
                self.spinbox_keyboard_pressure_ri.setValue(parameter['keyboard_pressure_ri'])
                self.spinbox_keyboard_pressure_rt.setValue(parameter['keyboard_pressure_rt'])

                self.spinbox_release_sensitivity.setValue(parameter['keyboard_release_sensitivity'])
                self.spinbox_long_press_duration.setValue(parameter['long_press_duration'])
                self.spinbox_retrigger_duration.setValue(parameter['retrigger_duration'])    

                self.spinbox_right_click_duration.setValue(parameter['right_click_duration'])
                self.spinbox_recenter_mouse.setValue(parameter['recenter_mouse_duration'])
                self.spinbox_motion_tolerance.setValue(parameter['motion_tolerance'])

                # Checkbox Options
                self.checkBox_trigger_mouse_down.setChecked(parameter['trigger_mouse_down'])
                self.checkBox_mouse_acceleration.setChecked(parameter['mouse_acceleration'])
                self.checkBox_proximity_sensor.setChecked(parameter['proximity_sensor'])
                # Language
                self.comboBox_language.setCurrentText(parameter['language'])


    def saveParameters(self):
        """Saves parameters to json file
        """
        parameter = {}
        # Mouse
        parameter['mouse_click_sensitivity_f'] = self.spinbox_mouse_click_sensitivity_f.value()
        parameter['mouse_pressure_f'] = self.spinbox_mouse_pressure_f.value()
        parameter['mouse_release_sensitivity_f'] = self.spinbox_mouse_release_sensitivity_f.value()
        parameter['mouse_click_sensitivity_p'] = self.spinbox_mouse_click_sensitivity_p.value()
        parameter['mouse_pressure_p'] = self.spinbox_mouse_pressure_p.value()
        parameter['mouse_release_sensitivity_p'] = self.spinbox_mouse_release_sensitivity_p.value()
        parameter['mouse_cursor_sensitivity'] = self.spinbox_mouse_cursor_sensitivity.value()
        # Screen
        parameter['mouse_left_boundary'] = self.spinbox_left_boundary.value()
        parameter['mouse_right_boundary'] = self.spinbox_right_boundary.value()
        parameter['mouse_upper_boundary'] = self.spinbox_upper_boundary.value()
        parameter['mouse_lower_boundary'] = self.spinbox_lower_boundary.value()
        # Scroll
        parameter['scroll_up_trigger'] = self.spinbox_scroll_up_trigger.value()
        parameter['scroll_down_trigger'] = self.spinbox_scroll_down_trigger.value()
        parameter['scroll_release_sensitivity'] = self.spinbox_scroll_release_sensitivity.value()
        parameter['scroll_speed'] = self.spinbox_scroll_speed.value()
        # Keyboard
        parameter['keyboard_next_key_idx'] = self.next_key_idx
        parameter['keyboard_space_key_idx'] = self.space_key_idx
    
        parameter['keyboard_layout_lp'] = self.keyboard_layout[0]
        parameter['keyboard_layout_lr'] = self.keyboard_layout[1]
        parameter['keyboard_layout_lm'] = self.keyboard_layout[2]
        parameter['keyboard_layout_li'] = self.keyboard_layout[3]
        parameter['keyboard_layout_lt'] = self.keyboard_layout[4]
        parameter['keyboard_layout_rt'] = self.keyboard_layout[5]
        parameter['keyboard_layout_ri'] = self.keyboard_layout[6]
        parameter['keyboard_layout_rm'] = self.keyboard_layout[7]
        parameter['keyboard_layout_rr'] = self.keyboard_layout[8]
        parameter['keyboard_layout_rp'] = self.keyboard_layout[9]

        parameter['keyboard_trigger_sensitivity_lp'] = self.spinbox_trigger_sensitivity_lp.value()
        parameter['keyboard_trigger_sensitivity_lr'] = self.spinbox_trigger_sensitivity_lr.value()
        parameter['keyboard_trigger_sensitivity_lm'] = self.spinbox_trigger_sensitivity_lm.value()
        parameter['keyboard_trigger_sensitivity_li'] = self.spinbox_trigger_sensitivity_li.value()
        parameter['keyboard_trigger_sensitivity_lt'] = self.spinbox_trigger_sensitivity_lt.value()
        parameter['keyboard_trigger_sensitivity_rp'] = self.spinbox_trigger_sensitivity_rp.value()
        parameter['keyboard_trigger_sensitivity_rr'] = self.spinbox_trigger_sensitivity_rr.value()
        parameter['keyboard_trigger_sensitivity_rm'] = self.spinbox_trigger_sensitivity_rm.value()
        parameter['keyboard_trigger_sensitivity_ri'] = self.spinbox_trigger_sensitivity_ri.value()
        parameter['keyboard_trigger_sensitivity_rt'] = self.spinbox_trigger_sensitivity_rt.value()

        parameter['keyboard_pressure_lp'] = self.spinbox_keyboard_pressure_lp.value()
        parameter['keyboard_pressure_lr'] = self.spinbox_keyboard_pressure_lr.value()
        parameter['keyboard_pressure_lm'] = self.spinbox_keyboard_pressure_lm.value()
        parameter['keyboard_pressure_li'] = self.spinbox_keyboard_pressure_li.value()
        parameter['keyboard_pressure_lt'] = self.spinbox_keyboard_pressure_lt.value()
        parameter['keyboard_pressure_rp'] = self.spinbox_keyboard_pressure_rp.value()
        parameter['keyboard_pressure_rr'] = self.spinbox_keyboard_pressure_rr.value()
        parameter['keyboard_pressure_rm'] = self.spinbox_keyboard_pressure_rm.value()
        parameter['keyboard_pressure_ri'] = self.spinbox_keyboard_pressure_ri.value()
        parameter['keyboard_pressure_rt'] = self.spinbox_keyboard_pressure_rt.value()

        parameter['keyboard_release_sensitivity'] = self.spinbox_release_sensitivity.value()
        parameter['long_press_duration'] = self.spinbox_long_press_duration.value()
        parameter['retrigger_duration'] = self.spinbox_retrigger_duration.value()

        parameter['right_click_duration'] = self.spinbox_right_click_duration.value()
        parameter['recenter_mouse_duration'] = self.spinbox_recenter_mouse.value()
        parameter['motion_tolerance'] = self.spinbox_motion_tolerance.value()

        # Checkbox Options
        parameter['trigger_mouse_down'] = self.checkBox_trigger_mouse_down.isChecked()
        parameter['mouse_acceleration'] = self.checkBox_mouse_acceleration.isChecked()
        parameter['proximity_sensor'] = self.checkBox_proximity_sensor.isChecked()
        # Language
        parameter['language'] = str(self.comboBox_language.currentText())

        # Save dialog
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Parameter File", "", "JSON File (*.json)", options=options)
        if fileName:
            with open(fileName, 'w') as f:
                json.dump(parameter, f)            


    def acceptParameters(self):
        """Accept currently set parameters for application usage
        """
        # Mouse
        self.mouse_click_sensitivity_f = self.spinbox_mouse_click_sensitivity_f.value()
        self.mouse_click_sensitivity_p = self.spinbox_mouse_click_sensitivity_p.value()
        self.mouse_pressure_f = self.spinbox_mouse_pressure_f.value()
        self.mouse_pressure_p = self.spinbox_mouse_pressure_p.value()
        self.mouse_release_sensitivity_f = self.spinbox_mouse_release_sensitivity_f.value()
        self.mouse_release_sensitivity_p = self.spinbox_mouse_release_sensitivity_p.value()
        self.mouse_cursor_sensitivity = self.spinbox_mouse_cursor_sensitivity.value()
        # Screen
        self.mouse_left_boundary = self.spinbox_left_boundary.value()
        self.mouse_right_boundary = self.spinbox_right_boundary.value()
        self.mouse_upper_boundary = self.spinbox_upper_boundary.value()
        self.mouse_lower_boundary = self.spinbox_lower_boundary.value()
        # Scroll
        self.scroll_up_trigger = self.spinbox_scroll_up_trigger.value()
        self.scroll_down_trigger = self.spinbox_scroll_down_trigger.value()
        self.scroll_release_sensitivity = self.spinbox_scroll_release_sensitivity.value()
        self.scroll_speed = self.spinbox_scroll_speed.value()
        # Keyboard
        if self.next_key_idx is None:
            self.next_key_idx = 4
        if self.space_key_idx is None:
            self.space_key_idx = 5

        if self.keyboard_layout[0] is None: # if it is not set, then default to setting all True
            self.keyboard_layout = [True]*10

        self.keyboard_trigger_sensitivity[0] = self.spinbox_trigger_sensitivity_lp.value()
        self.keyboard_trigger_sensitivity[1] = self.spinbox_trigger_sensitivity_lr.value()
        self.keyboard_trigger_sensitivity[2] = self.spinbox_trigger_sensitivity_lm.value()
        self.keyboard_trigger_sensitivity[3] = self.spinbox_trigger_sensitivity_li.value()
        self.keyboard_trigger_sensitivity[4] = self.spinbox_trigger_sensitivity_lt.value()
        self.keyboard_trigger_sensitivity[5] = self.spinbox_trigger_sensitivity_rt.value()
        self.keyboard_trigger_sensitivity[6] = self.spinbox_trigger_sensitivity_ri.value()
        self.keyboard_trigger_sensitivity[7] = self.spinbox_trigger_sensitivity_rm.value()
        self.keyboard_trigger_sensitivity[8] = self.spinbox_trigger_sensitivity_rr.value()
        self.keyboard_trigger_sensitivity[9] = self.spinbox_trigger_sensitivity_rp.value()

        self.keyboard_pressure[0] = self.spinbox_keyboard_pressure_lp.value()
        self.keyboard_pressure[1] = self.spinbox_keyboard_pressure_lr.value()
        self.keyboard_pressure[2] = self.spinbox_keyboard_pressure_lm.value()
        self.keyboard_pressure[3] = self.spinbox_keyboard_pressure_li.value()
        self.keyboard_pressure[4] = self.spinbox_keyboard_pressure_lt.value()
        self.keyboard_pressure[5] = self.spinbox_keyboard_pressure_rt.value()
        self.keyboard_pressure[6] = self.spinbox_keyboard_pressure_ri.value()
        self.keyboard_pressure[7] = self.spinbox_keyboard_pressure_rm.value()
        self.keyboard_pressure[8] = self.spinbox_keyboard_pressure_rr.value()
        self.keyboard_pressure[9] = self.spinbox_keyboard_pressure_rp.value()
        
        self.keyboard_release_sensitivity = self.spinbox_release_sensitivity.value()
        self.long_press_duration = self.spinbox_long_press_duration.value()
        self.retrigger_duration = self.spinbox_retrigger_duration.value()

        self.right_click_duration = self.spinbox_right_click_duration.value()
        self.recenter_mouse_duration = self.spinbox_recenter_mouse.value()
        self.tolerated_mouse_movement = self.spinbox_motion_tolerance.value()
        # Checkbox Options
        self.trigger_mouse_down = self.checkBox_trigger_mouse_down.isChecked()
        self.mouse_acceleration = self.checkBox_mouse_acceleration.isChecked()
        self.proximity_sensor = self.checkBox_proximity_sensor.isChecked()
        # Language
        self.language = str(self.comboBox_language.currentText())
        # UI and mouse checkbox
        self.hide_ui = self.checkBox_hide_ui.isChecked()
        self.disable_mouse = self.checkBox_disable_mouse.isChecked()
        
        self.close()


    def loadDictionary(self):
        """Loads dictionary from json file
        """
        options = QtWidgets.QFileDialog.Options()
        self.dict_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Dictionary File", os.path.join("python_code", "personal_dicts"), "JSON File (*.json)", options=options)
        self.lineEdit_load_dict.setText(self.dict_path)