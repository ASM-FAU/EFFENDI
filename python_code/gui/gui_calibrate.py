from asyncore import write
from gettext import find
import sys
import os
import json
import time
import math
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, QObject, pyqtSignal

import pyqtgraph as pg
from scipy import signal
import numpy as np
import pandas as pd


KEYBOARD_TRIGGER_THRESHOLD_FACTOR = 0.7#0.85
# KEYBOARD_RELEASE_THRESHOLD_FACTOR = 0.5#0.62
KEYBOARD_PEAK_THRESHOLD = 350
MOUSE_TRIGGER_THRESHOLD_FACTOR_F = 0.7#0.8
MOUSE_TRIGGER_THRESHOLD_FACTOR_P = 1.0#0.8
MOUSE_RELEASE_THRESHOLD_FACTOR_P = 0.95
MOUSE_PEAK_THRESHOLD = 100
# MOUSE_PEAK_THRESHOLD_PROX = 0.5
MOUSE_PEAK_THRESHOLD_PROX = 1.1
SCROLL_TRIGGER_THRESHOLD_FACTOR = 0.8
# SCROLL_RELEASE_THRESHOLD_FACTOR = 0.78

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


class CalibrateGUI(QtWidgets.QDialog):
    def __init__(self, event, mouse_queue, gui_queue, write_queue):
        super(CalibrateGUI, self).__init__()
        self.event = event
        self.mouse_queue = mouse_queue
        self.gui_queue = gui_queue
        self.write_queue = write_queue

        # print(os.path.join(os.getcwd(), 'python_code', 'ui', 'setup_dialog.ui'))
        # print(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ui', 'setup_dialog.ui'))
        # print(os.path.join(os.path.dirname(sys.executable), 'ui', 'setup_dialog.ui'))
        # if '_MEIPASS2' in os.environ:
        #     print(os.path.join(os.environ["_MEIPASS2"], 'ui', 'setup_dialog.ui'))
      
        uic.loadUi(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'ui', 'calibrate_study_proximity_v2.ui'), self)

        self.fileName = ""  # Path to parameter file
        self.sensor_data = None
        self.mouse_fit_active = False
        self.active_keys = [True]*10
        # Default keys for next and space
        self.next_key_idx = 4
        self.space_key_idx = 5

        ## Dialog buttons
        # Mouse Fit
        self.pushButton_next_mouse_fit.clicked.connect(lambda: self.nextTab())
        self.pushButton_calibrate_mouse_fit.clicked.connect(lambda: self.calibrateMouseFit())
        # Mouse Click
        self.pushButton_next_mouse_click.clicked.connect(lambda: self.nextTab())
        self.pushButton_calibrate_mouse_press.clicked.connect(lambda: self.calibrateMousePress())
        self.pushButton_export_mouse.clicked.connect(lambda: self.exportMouse())
        # Mouse Sensitivity
        self.pushButton_next_mouse_cursor.clicked.connect(lambda: self.nextTab())
        self.pushButton_calibrate_mouse_cursor.clicked.connect(lambda: self.calibrateMouseSensitivity())
        # Scroll
        self.pushButton_next_scroll.clicked.connect(lambda: self.nextTab())
        self.pushButton_calibrate_scroll.clicked.connect(lambda: self.calibrateScroll())
        # Keyboard Layout
        self.pushButton_next_layout.clicked.connect(lambda: self.nextTab())
        self.checkBox_keyboard_layout_lp.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.checkBox_keyboard_layout_lr.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.checkBox_keyboard_layout_lm.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.checkBox_keyboard_layout_li.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.checkBox_keyboard_layout_lt.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.checkBox_keyboard_layout_rt.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.checkBox_keyboard_layout_ri.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.checkBox_keyboard_layout_rm.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.checkBox_keyboard_layout_rr.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.checkBox_keyboard_layout_rp.stateChanged.connect(lambda: self.calibrateKeyboardLayout())
        self.keyboard_layout_checkBox = [
            self.checkBox_keyboard_layout_lp,
            self.checkBox_keyboard_layout_lr,
            self.checkBox_keyboard_layout_lm,
            self.checkBox_keyboard_layout_li,
            self.checkBox_keyboard_layout_lt,
            self.checkBox_keyboard_layout_rt,
            self.checkBox_keyboard_layout_ri,
            self.checkBox_keyboard_layout_rm,
            self.checkBox_keyboard_layout_rr,
            self.checkBox_keyboard_layout_rp
        ]
        self.keyboard_layout_label = [
            self.label_keyboard_layout_lp,
            self.label_keyboard_layout_lr,
            self.label_keyboard_layout_lm,
            self.label_keyboard_layout_li,
            self.label_keyboard_layout_lt,
            self.label_keyboard_layout_rt,
            self.label_keyboard_layout_ri,
            self.label_keyboard_layout_rm,
            self.label_keyboard_layout_rr,
            self.label_keyboard_layout_rp
        ]
        self.keyboard_layout_marker = [
            self.label_layout_marker_lp,
            self.label_layout_marker_lr,
            self.label_layout_marker_lm,
            self.label_layout_marker_li,
            self.label_layout_marker_lt,
            self.label_layout_marker_rt,
            self.label_layout_marker_ri,
            self.label_layout_marker_rm,
            self.label_layout_marker_rr,
            self.label_layout_marker_rp
        ]
        # Keyboard pressure
        self.pushButton_next_keyboard_pressure.clicked.connect(lambda: self.nextTab())
        self.pushButton_calibrate_keyboard_pressure.clicked.connect(lambda: self.calibrateKeyboardPressure())
        self.pushButton_export_keyboard_pressure.clicked.connect(lambda: self.exportKeyboardPressure())
        # Keyboard
        self.pushButton_next_keyboard.clicked.connect(lambda: self.nextTab())
        self.pushButton_calibrate_keyboard.clicked.connect(lambda: self.calibrateKeyboard())
        self.pushButton_export_keyboard.clicked.connect(lambda: self.exportKeyboard())
        # Long press
        self.pushButton_next_long_press.clicked.connect(lambda: self.nextTab())
        self.pushButton_calibrate_long_press.clicked.connect(lambda: self.calibrateLongPress())
        self.pushButton_export_long_press.clicked.connect(lambda: self.exportLongPress())
        # Summary
        self.pushButton_close.clicked.connect(lambda: self.closeDialog())
        self.pushButton_load_parameter.clicked.connect(lambda: self.loadParameters())
        self.pushButton_save_parameter.clicked.connect(lambda: self.saveParameters())

        # Window formatting
        self.graphWidget_keyboard.hide()
        self.graphWidget_keyboard.setBackground('w')
        self.graphWidget_keyboard.setYRange(0, 1020, padding=0)

        self.graphWidget_mouse.setBackground('w')
        self.graphWidget_mouse.setYRange(0, 100, padding=0)

        # Set default values
        self.comboBox_mouse_calibration_stroke.setCurrentText("10")
        self.comboBox_keyboard_calibration_stroke.setCurrentText("10")
        self.comboBox_long_press_calibration_stroke.setCurrentText("10")


    def nextTab(self):
        """Switch to next Tab on button press
        """
        cur_index = self.tabWidget.currentIndex()
        if cur_index < len(self.tabWidget)-1:
            self.tabWidget.setCurrentIndex(cur_index+1)


    def calibrateMouseFit(self):
        """Detects peaks in mouse press signal and determines trigger and release threshold
        """
        if self.mouse_fit_active is False:

            # self.graphWidget_mouse.clear()

            # Initiate Sensor Thread
            self.calibrateMouseFitThread = QThread(parent=self)
            self.fsr_intensity = FitGlasses(self.event, self.gui_queue, str(self.comboBox_mouse_click.currentText()))
            self.fsr_intensity.moveToThread(self.calibrateMouseFitThread)
            # Connect signals and slots
            self.calibrateMouseFitThread.started.connect(self.fsr_intensity.run)
            self.fsr_intensity.finished.connect(self.calibrateMouseFitThread.quit)
            self.fsr_intensity.finished.connect(self.fsr_intensity.deleteLater)
            self.calibrateMouseFitThread.finished.connect(self.calibrateMouseFitThread.deleteLater)
            self.fsr_intensity.fsr_mouse.connect(self.fsrIntensity)
            # Start Thread
            self.calibrateMouseFitThread.start()

            self.pushButton_calibrate_mouse_fit.setText("Finalize Calibration")
            self.mouse_fit_active = True
        else:
            self.fsr_intensity.active = False
            self.pushButton_calibrate_mouse_fit.setText("Calibrate Mouse Fit")
            self.mouse_fit_active = False

            mouse_pressure = 0
            if self.fsr_intensity.mouse_pressure is not None:
                mouse_pressure = self.fsr_intensity.mouse_pressure

            if str(self.comboBox_mouse_click.currentText()) == "Force":
                self.spinbox_mouse_pressure_f.setValue(mouse_pressure)

            if str(self.comboBox_mouse_click.currentText()) == "Proximity":
                self.spinbox_mouse_pressure_p.setValue(mouse_pressure)

            self.calibrateMouseFitThread.quit()
            # self.calibrateMouseFitThread.wait()


    def calibrateMousePress(self):
        """Detects peaks in mouse press signal and determines trigger and release threshold
        """
        self.graphWidget_mouse.clear()

        # Initiate Sensor Thread
        self.calibrateMouseClickThread = QThread()
        self.calibration_progress = ReadSensor(self.event, self.gui_queue, self.write_queue, float(self.comboBox_mouse_calibration_stroke.currentText()), "mouse", self.spinbox_mouse_pressure_f.value(), self.spinbox_mouse_pressure_p.value(), None, None, str(self.comboBox_mouse_click.currentText()))
        self.calibration_progress.moveToThread(self.calibrateMouseClickThread)
        print("start thread")
        # Connect signals and slots
        self.calibrateMouseClickThread.started.connect(self.calibration_progress.run)
        self.calibration_progress.finished.connect(self.calibrateMouseClickThread.quit)
        self.calibration_progress.finished.connect(self.calibration_progress.deleteLater)
        self.calibrateMouseClickThread.finished.connect(self.calibrateMouseClickThread.deleteLater)
        self.calibration_progress.countChanged.connect(self.progressMouseClick)
        self.calibration_progress.passSensorData.connect(self.processMouseClickSensorData)
        # Start Thread
        self.calibrateMouseClickThread.start()

        self.pushButton_calibrate_mouse_press.setEnabled(False)
        self.pushButton_export_mouse.setEnabled(False)
        self.calibrateMouseClickThread.finished.connect(lambda: self.pushButton_calibrate_mouse_press.setEnabled(True))
        self.calibrateMouseClickThread.finished.connect(lambda: self.pushButton_export_mouse.setEnabled(True))
        

    def calibrateMouseSensitivity(self):
        """Uses lower left and upper right corner of the screen to determine mouse movement sensitivity
        """
        # Initiate Sensor Thread
        self.calibrateMouseSensitivityThread = QThread()
        self.screen_boundaries = GetScreenBoundaries(self.event, self.gui_queue, self.write_queue, self.spinbox_mouse_click_sensitivity_f.value(), self.spinbox_mouse_click_sensitivity_p.value(), self.spinbox_mouse_release_sensitivity_f.value(), self.spinbox_mouse_release_sensitivity_p.value(), str(self.comboBox_mouse_click.currentText()))
        self.screen_boundaries.moveToThread(self.calibrateMouseSensitivityThread)
        # Connect signals and slots
        self.calibrateMouseSensitivityThread.started.connect(self.screen_boundaries.run)
        self.screen_boundaries.finished.connect(self.calibrateMouseSensitivityThread.quit)
        self.screen_boundaries.finished.connect(self.screen_boundaries.deleteLater)
        self.calibrateMouseSensitivityThread.finished.connect(self.calibrateMouseSensitivityThread.deleteLater)
        self.screen_boundaries.passBoundaries.connect(self.processScreenBoundaries)
        # Start Thread
        self.calibrateMouseSensitivityThread.start()

        self.pushButton_calibrate_mouse_cursor.setEnabled(False)
        self.calibrateMouseSensitivityThread.finished.connect(lambda: self.pushButton_calibrate_mouse_cursor.setEnabled(True))


    def calibrateScroll(self):
        """Determines threshold for scrolling up and down through rolling head left and right
        """
        # Initiate Sensor Thread
        self.calibrateScrollThread = QThread()
        self.scroll_boundaries = GetScrollBoundaries(self.event, self.gui_queue, self.write_queue, self.spinbox_mouse_click_sensitivity_f.value(), self.spinbox_mouse_click_sensitivity_p.value(), self.spinbox_mouse_release_sensitivity_f.value(), self.spinbox_mouse_release_sensitivity_p.value(), str(self.comboBox_mouse_click.currentText()))
        self.scroll_boundaries.moveToThread(self.calibrateScrollThread)
        # Connect signals and slots
        self.calibrateScrollThread.started.connect(self.scroll_boundaries.run)
        self.scroll_boundaries.finished.connect(self.calibrateScrollThread.quit)
        self.scroll_boundaries.finished.connect(self.scroll_boundaries.deleteLater)
        self.calibrateScrollThread.finished.connect(self.calibrateScrollThread.deleteLater)
        self.scroll_boundaries.passBoundaries.connect(self.processScrollBoundaries)
        # Start Thread
        self.calibrateScrollThread.start()

        self.pushButton_calibrate_scroll.setEnabled(False)
        self.calibrateScrollThread.finished.connect(lambda: self.pushButton_calibrate_scroll.setEnabled(True))


    def calibrateKeyboardLayout(self):
        
        # Set next and space button as close to thumbs as possible
        for i in range(len(self.keyboard_layout_checkBox)):
            self.active_keys[i] = self.keyboard_layout_checkBox[i].isChecked()
        
        letter_keys = self.active_keys.copy()
        
        # self.next_key_idx = None
        for i in range(5):
            if self.active_keys[4-i] is True:
                self.next_key_idx = 4-i
                letter_keys[4-i] = False
                self.keyboard_layout_label[self.next_key_idx].setText('next')
                break

        # space_key_idx = None
        for i in range(5):
            if self.active_keys[5+i] is True:
                self.space_key_idx = 5+i
                letter_keys[5+i] = False
                self.keyboard_layout_label[self.space_key_idx].setText('space')
                break

        # Distribute letters to keys
        available_keys = self.active_keys.count(True)
        letter_layout = [3, 3, 3, 3, 3, 4, 3, 4]
        if available_keys < 10:
            letters_per_key = int(26 / (available_keys - 2)) # subtract 2 for next and space button
            remaining_keys = 26 % (available_keys - 2)  # number of keys that contain more letters than general
            letter_layout = [letters_per_key]*(available_keys-2)
            # distribute the remaining letters
            for i in range(remaining_keys):
                letter_layout[-1-i] += 1

        # Distribute letters between keys
        keysLayout = ['']*(available_keys-2)
        letter_idx = 0  # alphabet counter
        for i in range(len(letter_layout)):
            for _ in range(letter_layout[i]):
                keysLayout[i] += ALPHABET[letter_idx]
                letter_idx += 1

        # Update UI
        letter_key_idx = 0
        for i in range(len(letter_keys)):
            if self.active_keys[i] is True:
                self.keyboard_layout_marker[i].setEnabled(True)
            else:
                self.keyboard_layout_marker[i].setEnabled(False)
                self.keyboard_layout_label[i].setText('')
            
            if letter_keys[i] is True:
                self.keyboard_layout_label[i].setText(keysLayout[letter_key_idx])
                letter_key_idx += 1
            # elif letter_keys[i] is False:
                
            #     if self.active_keys[i] is True:
            #         self.keyboard_layout_marker[i].setEnabled(True)
            #     else:
            #         self.keyboard_layout_marker[i].setEnabled(False)
            # else:
            #     raise ValueError('Letter Key State should be either True or False!')


    def calibrateKeyboardPressure(self):
        """Calibrates initial keyboard pressure.
        """
        # self.finger_marker_labels = [self.label_finger_marker_lp, self.label_finger_marker_lr, self.label_finger_marker_lm, self.label_finger_marker_li, self.label_finger_marker_lt, self.label_finger_marker_rt, self.label_finger_marker_ri, self.label_finger_marker_rm, self.label_finger_marker_rr, self.label_finger_marker_rp]

        # Initiate Sensor Thread
        self.calibrateKeyboardPressureThread = QThread()
        self.calibration_progress = ReadSensor(self.event, self.gui_queue, self.write_queue, None, "pressure", None, None, None, None)
        self.calibration_progress.moveToThread(self.calibrateKeyboardPressureThread)
        # Connect signals and slots
        self.calibrateKeyboardPressureThread.started.connect(self.calibration_progress.run)
        self.calibration_progress.finished.connect(self.calibrateKeyboardPressureThread.quit)
        self.calibration_progress.finished.connect(self.calibration_progress.deleteLater)
        self.calibrateKeyboardPressureThread.finished.connect(self.calibrateKeyboardPressureThread.deleteLater)
        self.calibration_progress.countChanged.connect(self.progressKeyboardPressure)
        # self.calibration_progress.updateFingerMarker.connect(self.updateFingerMarker)
        self.calibration_progress.passSensorData.connect(self.processKeyboardPressureData)
        # Start Thread
        self.calibrateKeyboardPressureThread.start()

        self.pushButton_calibrate_keyboard_pressure.setEnabled(False)
        self.pushButton_export_keyboard_pressure.setEnabled(False)
        self.calibrateKeyboardPressureThread.finished.connect(lambda: self.pushButton_calibrate_keyboard_pressure.setEnabled(True))
        self.calibrateKeyboardPressureThread.finished.connect(lambda: self.pushButton_export_keyboard_pressure.setEnabled(True))


    def calibrateKeyboard(self):
        """Calibrates keyboard by user input. Detects peaks from button presses to determine trigger and release threshold for the keyboard
        """
        # Hide peaks and show hand instructions
        self.graphWidget_keyboard.hide()
        self.graphWidget_keyboard.clear()
        self.finger_marker_labels = [self.label_finger_marker_lp, self.label_finger_marker_lr, self.label_finger_marker_lm, self.label_finger_marker_li, self.label_finger_marker_lt, self.label_finger_marker_rt, self.label_finger_marker_ri, self.label_finger_marker_rm, self.label_finger_marker_rr, self.label_finger_marker_rp]
        for finger_marker_label in self.finger_marker_labels:
            finger_marker_label.show()
        self.label_l.show()
        self.label_r.show()
        self.label_hand_l.show()
        self.label_hand_r.show()

        # Initiate Sensor Thread
        self.calibrateKeyboardThread = QThread()
        initial_pressure = [self.spinbox_keyboard_pressure_lp.value(), self.spinbox_keyboard_pressure_lr.value(), self.spinbox_keyboard_pressure_lm.value(), self.spinbox_keyboard_pressure_li.value(), self.spinbox_keyboard_pressure_lt.value(), self.spinbox_keyboard_pressure_rt.value(), self.spinbox_keyboard_pressure_ri.value(), self.spinbox_keyboard_pressure_rm.value(), self.spinbox_keyboard_pressure_rr.value(), self.spinbox_keyboard_pressure_rp.value()]
        self.calibration_progress = ReadSensor(self.event, self.gui_queue, self.write_queue, float(self.comboBox_keyboard_calibration_stroke.currentText()), "keyboard", None, None, initial_pressure, self.active_keys)
        self.calibration_progress.moveToThread(self.calibrateKeyboardThread)
        # Connect signals and slots
        self.calibrateKeyboardThread.started.connect(self.calibration_progress.run)
        self.calibration_progress.finished.connect(self.calibrateKeyboardThread.quit)
        self.calibration_progress.finished.connect(self.calibration_progress.deleteLater)
        self.calibrateKeyboardThread.finished.connect(self.calibrateKeyboardThread.deleteLater)
        self.calibration_progress.countChanged.connect(self.progressKeyboard)
        self.calibration_progress.updateFingerMarker.connect(self.updateFingerMarker)
        self.calibration_progress.passSensorData.connect(self.processKeyboardSensorData)
        # Start Thread
        self.calibrateKeyboardThread.start()

        self.pushButton_calibrate_keyboard.setEnabled(False)
        self.pushButton_export_keyboard.setEnabled(False)
        self.calibrateKeyboardThread.finished.connect(lambda: self.pushButton_calibrate_keyboard.setEnabled(True))
        self.calibrateKeyboardThread.finished.connect(lambda: self.pushButton_export_keyboard.setEnabled(True))


    def calibrateLongPress(self):
        """Press the button with right thumb multiple times to calibrate long press
        """
        # Initiate Sensor Thread
        self.calibrateLongPressThread = QThread()
        initial_pressure = [self.spinbox_keyboard_pressure_lp.value(), self.spinbox_keyboard_pressure_lr.value(), self.spinbox_keyboard_pressure_lm.value(), self.spinbox_keyboard_pressure_li.value(), self.spinbox_keyboard_pressure_lt.value(), self.spinbox_keyboard_pressure_rt.value(), self.spinbox_keyboard_pressure_ri.value(), self.spinbox_keyboard_pressure_rm.value(), self.spinbox_keyboard_pressure_rr.value(), self.spinbox_keyboard_pressure_rp.value()]
        self.calibration_progress = ReadSensor(self.event, self.gui_queue, self.write_queue, float(self.comboBox_long_press_calibration_stroke.currentText()), "long_press", None, None, initial_pressure, None)
        self.calibration_progress.moveToThread(self.calibrateLongPressThread)
        # Connect signals and slots
        self.calibrateLongPressThread.started.connect(self.calibration_progress.run)
        self.calibration_progress.finished.connect(self.calibrateLongPressThread.quit)
        self.calibration_progress.finished.connect(self.calibration_progress.deleteLater)
        self.calibrateLongPressThread.finished.connect(self.calibrateLongPressThread.deleteLater)
        self.calibration_progress.countChanged.connect(self.progressLongPress)
        # self.calibration_progress.updateFingerMarker.connect(self.updateFingerMarker)
        self.calibration_progress.passSensorData.connect(self.processLongPress)
        # Start Thread
        self.calibrateLongPressThread.start()

        self.pushButton_calibrate_long_press.setEnabled(False)
        self.pushButton_export_long_press.setEnabled(False)
        self.calibrateLongPressThread.finished.connect(lambda: self.pushButton_calibrate_long_press.setEnabled(True))
        self.calibrateLongPressThread.finished.connect(lambda: self.pushButton_export_long_press.setEnabled(True))


    def closeDialog(self):
        """Closes Window and active Thread
        """
        print("closing...")
        self.close()
        # print(reading_sensor.is_alive())
        # sys._exit()
        # self.accept()
        # QtWidgets.qApp.quit()
        # QtWidgets.QApplication.quit()
        
        # self.event.accept()
        # self.quit()
        sys.exit()
        #TODO program does not exit properly


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

                self.checkBox_keyboard_layout_lp.setChecked(parameter['keyboard_layout_lp'])
                self.checkBox_keyboard_layout_lr.setChecked(parameter['keyboard_layout_lr'])
                self.checkBox_keyboard_layout_lm.setChecked(parameter['keyboard_layout_lm'])
                self.checkBox_keyboard_layout_li.setChecked(parameter['keyboard_layout_li'])
                self.checkBox_keyboard_layout_lt.setChecked(parameter['keyboard_layout_lt'])
                self.checkBox_keyboard_layout_rp.setChecked(parameter['keyboard_layout_rp'])
                self.checkBox_keyboard_layout_rr.setChecked(parameter['keyboard_layout_rr'])
                self.checkBox_keyboard_layout_rm.setChecked(parameter['keyboard_layout_rm'])
                self.checkBox_keyboard_layout_ri.setChecked(parameter['keyboard_layout_ri'])
                self.checkBox_keyboard_layout_rt.setChecked(parameter['keyboard_layout_rt'])

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
        """Saves parameters in a json file that can then be loaded by the application
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

        parameter['keyboard_layout_lp'] = self.checkBox_keyboard_layout_lp.isChecked()
        parameter['keyboard_layout_lr'] = self.checkBox_keyboard_layout_lr.isChecked()
        parameter['keyboard_layout_lm'] = self.checkBox_keyboard_layout_lm.isChecked()
        parameter['keyboard_layout_li'] = self.checkBox_keyboard_layout_li.isChecked()
        parameter['keyboard_layout_lt'] = self.checkBox_keyboard_layout_lt.isChecked()
        parameter['keyboard_layout_rp'] = self.checkBox_keyboard_layout_rp.isChecked()
        parameter['keyboard_layout_rr'] = self.checkBox_keyboard_layout_rr.isChecked()
        parameter['keyboard_layout_rm'] = self.checkBox_keyboard_layout_rm.isChecked()
        parameter['keyboard_layout_ri'] = self.checkBox_keyboard_layout_ri.isChecked()
        parameter['keyboard_layout_rt'] = self.checkBox_keyboard_layout_rt.isChecked()

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

        # Save Dialog
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Parameter File", "", "JSON File (*.json)", options=options)
        if fileName:
            with open(fileName, 'w') as f:
                json.dump(parameter, f)


    def fsrIntensity(self, value_fsr):
        """Use Mouse FSR value to determine fit and enter into progressbar to see the initial pressure

        Args:
            value (tuple): Tuple of ints containing mouse FSR or proximity values
        """
        value = [0]*2
        if str(self.comboBox_mouse_click.currentText()) == "Force":
            value[0] = value_fsr[0]
            value[1] = value_fsr[1]
            self.progressBar_fsr_mouse_left.setMinimum(0)
            self.progressBar_fsr_mouse_right.setMinimum(0)
            self.progressBar_fsr_mouse_left.setMaximum(200)
            self.progressBar_fsr_mouse_right.setMaximum(200)
        elif str(self.comboBox_mouse_click.currentText()) == "Proximity":
            # value[0] = ((value_fsr[0] / self.fsr_intensity.mouse_pressure) - 1) * 400
            # value[1] = ((value_fsr[1] / self.fsr_intensity.mouse_pressure) - 1) * 400
            value[0] = value_fsr[0]
            value[1] = value_fsr[1]
            self.progressBar_fsr_mouse_left.setMinimum(self.fsr_intensity.mouse_pressure)
            self.progressBar_fsr_mouse_right.setMinimum(self.fsr_intensity.mouse_pressure)
            self.progressBar_fsr_mouse_left.setMaximum(1.2*self.fsr_intensity.mouse_pressure)
            self.progressBar_fsr_mouse_right.setMaximum(1.2*self.fsr_intensity.mouse_pressure)
            print(value[0])
            print(self.fsr_intensity.mouse_pressure)
            # print("here")
            #print(value_fsr[0])
            # proximity to mm: y = 123389.9 - (40522.52/0.3554498)*(1 - e^(-0.3554498*x))

        self.progressBar_fsr_mouse_left.setStyleSheet("QProgressBar::chunk {background-color: green;}")
        self.progressBar_fsr_mouse_right.setStyleSheet("QProgressBar::chunk {background-color: green;}")
        self.progressBar_fsr_mouse_left.setValue(value[0])
        self.progressBar_fsr_mouse_right.setValue(value[1])

        # if value[0] < 100:
        #     self.progressBar_fsr_mouse_left.setValue(value[0])
        #     self.progressBar_fsr_mouse_left.setStyleSheet("QProgressBar::chunk {background-color: green;}")
        # elif value[0] < 150:
        #     self.progressBar_fsr_mouse_left.setValue(value[0])
        #     self.progressBar_fsr_mouse_left.setStyleSheet("QProgressBar::chunk {background-color: yellow;}")
        # elif value[0] < 200:
        #     self.progressBar_fsr_mouse_left.setValue(value[0])
        #     self.progressBar_fsr_mouse_left.setStyleSheet("QProgressBar::chunk {background-color: red;}")
        # elif value[0] >= 200:
        #     self.progressBar_fsr_mouse_left.setValue(200)
        #     self.progressBar_fsr_mouse_left.setStyleSheet("QProgressBar::chunk {background-color: red;}")
        # if value[1] < 100:
        #     self.progressBar_fsr_mouse_right.setValue(value[1])
        #     self.progressBar_fsr_mouse_right.setStyleSheet("QProgressBar::chunk {background-color: green;}")
        # elif value[1] < 150:
        #     self.progressBar_fsr_mouse_right.setValue(value[1])
        #     self.progressBar_fsr_mouse_right.setStyleSheet("QProgressBar::chunk {background-color: yellow;}")
        # elif value[1] < 200:
        #     self.progressBar_fsr_mouse_right.setValue(value[1])
        #     self.progressBar_fsr_mouse_right.setStyleSheet("QProgressBar::chunk {background-color: red;}")
        # elif value[1] >= 200:
        #     self.progressBar_fsr_mouse_right.setValue(200)
        #     self.progressBar_fsr_mouse_right.setStyleSheet("QProgressBar::chunk {background-color: red;}")


    def progressMouseClick(self, value):
        """Updates value in progressbar

        Args:
            value (int): Percentage
        """
        self.progressBar_mouse_click.setValue(value)


    def progressKeyboard(self, value):
        """Updates value in progressbar

        Args:
            value (int): Percentage
        """
        self.progressBar_keyboard.setValue(value)

    
    def progressKeyboardPressure(self, value):
        """Updates value in progressbar

        Args:
            value (int): Percentage
        """
        self.progressBar_keyboard_pressure.setValue(value)


    def progressLongPress(self, value):
        """Updates value in progressbar

        Args:
            value (int): Percentage
        """
        self.progressBar_long_press.setValue(value)


    def updateFingerMarker(self, finger, stroke):
        """Updates the finder markers, so the user knows which finger to use for keyboard calibration

        Args:
            finger (int): Finger marker index starting from left pinky to right pinky
        """
        for finger_marker_label in self.finger_marker_labels:
            finger_marker_label.setEnabled(False)

        if type(finger) is int and finger < 10:
            self.finger_marker_labels[finger].setEnabled(True)

        if finger < 5:
            self.label_l.setText(str(stroke))
            self.label_r.setText("R")
        else:
            self.label_r.setText(str(stroke))
            self.label_l.setText("L")


    # def proximityToMillimeter(self, proximity):
    #     """Translate proximity measurement for mouse click into mm. Analytical formula determined experimentally. Might change for different lighting.

    #     Args:
    #         proximity (int): Proximity value without unit and exponential behavior

    #     Returns:
    #         float: Proximity in mm
    #     """
    #     proximity_mm = 18.90639 - (0.001051379/0.00006224794)*(1 - math.exp(-0.00006224794*proximity))
    #     return proximity_mm


    def processMouseClickSensorData(self, sensor_data):
        """Finds all peaks in mouse click calibration data and computes trigger and release threshold

        Args:
            sensor_data (numpy.ndarray): Array containing data from mouse click calibration
        """
        peakind = None
        peakind_min = 100000
        peakind_max = 0
        self.mouse_peaks = []

        if str(self.comboBox_mouse_click.currentText()) == "Force":
            mouse_signal = (sensor_data[:, 3] + sensor_data[:, 4]) / 2 # mean between both sensors
            peakind = signal.find_peaks_cwt(mouse_signal, np.arange(3,40))
            # Remove all peaks smaller than 20 + initial pressure
            if len(peakind) > 0:
                peakind = peakind[mouse_signal[peakind] > (MOUSE_PEAK_THRESHOLD + self.spinbox_mouse_pressure_f.value() * 10)]
        elif str(self.comboBox_mouse_click.currentText()) == "Proximity":
            mouse_signal = sensor_data[:, 15]
            peakind = signal.find_peaks_cwt(mouse_signal*100, np.arange(3,40))
            # Remove all peaks smaller than 20 + initial pressure
            if len(peakind) > 0:
                peakind = peakind[mouse_signal[peakind] > (MOUSE_PEAK_THRESHOLD_PROX + self.spinbox_mouse_pressure_p.value())]

        # Update min and max peak value
        if len(peakind) > 0:
            peakind_min = peakind.min()
            peakind_max = peakind.max()
        else:
            print("No peaks detected!")
            return

        for peak in peakind:
            self.mouse_peaks.append(mouse_signal[peak])

        # Add Legend to graph (must be called before curves)
        self.graphWidget_mouse.addLegend().setOffset((5,5))

        # Plot graph for each button and mark peaks with "x"
        if len(peakind) > 0:
            self.graphWidget_mouse.plot(peakind, mouse_signal[peakind], symbol="x", pen=pg.mkPen('w', width=0))
        self.graphWidget_mouse.plot(range(mouse_signal.size), mouse_signal)

        # Fit graph to peak range
        self.graphWidget_mouse.setXRange(peakind_min-100, peakind_max+100, padding=0) 
        if str(self.comboBox_mouse_click.currentText()) == "Force":
            self.graphWidget_mouse.setYRange(0, int(1.2*max(self.mouse_peaks)), padding=0) 
        elif str(self.comboBox_mouse_click.currentText()) == "Proximity":
            self.graphWidget_mouse.setYRange(self.spinbox_mouse_pressure_p.value(), int(1.2*max(self.mouse_peaks)), padding=0)  # start y axis at initial mouse pressure level
        
        # Calculate trigger and release threshold based on button inputs
        if len(self.mouse_peaks) > 0:
            if str(self.comboBox_mouse_click.currentText()) == "Force":
                self.spinbox_mouse_click_sensitivity_f.setValue((1000 - (MOUSE_TRIGGER_THRESHOLD_FACTOR_F * (sum(self.mouse_peaks) / len(self.mouse_peaks)))) / 10.)
                # Draw trigger and release threshold
                self.graphWidget_mouse.plot([peakind_min-100, peakind_max+100], [MOUSE_TRIGGER_THRESHOLD_FACTOR_F * (sum(self.mouse_peaks) / len(self.mouse_peaks)), MOUSE_TRIGGER_THRESHOLD_FACTOR_F * (sum(self.mouse_peaks) / len(self.mouse_peaks))], pen=pg.mkPen(color=(50, 168, 82)), name="Trigger").setZValue(11)
                self.graphWidget_mouse.plot([peakind_min-100, peakind_max+100], [(self.spinbox_mouse_release_sensitivity_f.value() / 100) * MOUSE_TRIGGER_THRESHOLD_FACTOR_F * (sum(self.mouse_peaks) / len(self.mouse_peaks)), (self.spinbox_mouse_release_sensitivity_f.value() / 100) * MOUSE_TRIGGER_THRESHOLD_FACTOR_F * (sum(self.mouse_peaks) / len(self.mouse_peaks))], pen=pg.mkPen(color=(237, 143, 50)), name="Release").setZValue(11)
            elif str(self.comboBox_mouse_click.currentText()) == "Proximity":
                self.spinbox_mouse_click_sensitivity_p.setValue(MOUSE_TRIGGER_THRESHOLD_FACTOR_P * ((sum(self.mouse_peaks) / len(self.mouse_peaks)) - self.spinbox_mouse_pressure_p.value()) + self.spinbox_mouse_pressure_p.value())
                self.spinbox_mouse_release_sensitivity_p.setValue(MOUSE_RELEASE_THRESHOLD_FACTOR_P * ((sum(self.mouse_peaks) / len(self.mouse_peaks)) - self.spinbox_mouse_pressure_p.value()) + self.spinbox_mouse_pressure_p.value())
                # Draw trigger and release threshold
                self.graphWidget_mouse.plot([peakind_min-100, peakind_max+100], [self.spinbox_mouse_click_sensitivity_p.value(), self.spinbox_mouse_click_sensitivity_p.value()], pen=pg.mkPen(color=(50, 168, 82)), name="Trigger").setZValue(11)
                self.graphWidget_mouse.plot([peakind_min-100, peakind_max+100], [self.spinbox_mouse_release_sensitivity_p.value(), self.spinbox_mouse_release_sensitivity_p.value()], pen=pg.mkPen(color=(237, 143, 50)), name="Release").setZValue(11)


    def processKeyboardPressureData(self, sensor_data):
        """Records the initial pressure of the resting hands on keyboard buttons. Records 5 seconds but only considers last time frame for calibration.

        Args:
            sensor_data (numpy.ndarray): Array containing data from keyboard pressure calibration
        """
        self.keyboard_pressure = []
        self.spinbox_keyboard_pressure = [self.spinbox_keyboard_pressure_lp, self.spinbox_keyboard_pressure_lr, self.spinbox_keyboard_pressure_lm, self.spinbox_keyboard_pressure_li, self.spinbox_keyboard_pressure_lt, self.spinbox_keyboard_pressure_rt, self.spinbox_keyboard_pressure_ri, self.spinbox_keyboard_pressure_rm, self.spinbox_keyboard_pressure_rr, self.spinbox_keyboard_pressure_rp]

        for i in range(10): # iterate through all buttons
            button_idx = i + 5  # buttons start with fifth index
            self.spinbox_keyboard_pressure[i].setValue(int(sensor_data[-1, button_idx] / 10.))
            self.keyboard_pressure.append(sensor_data[-1, button_idx])


    def processKeyboardSensorData(self, sensor_data):
        """Finds all peaks in keyboard calibration data and computes trigger and release threshold

        Args:
            sensor_data (numpy.ndarray): Array containing data from keyboard calibration
        """
        peakind = [0] * 10
        peakind_min = 100000
        peakind_max = 0
        self.keyboard_peaks = [[] for _ in range(10)]
        self.keyboard_peaks_std = []
        self.spinbox_trigger_sensitivity = [self.spinbox_trigger_sensitivity_lp, self.spinbox_trigger_sensitivity_lr, self.spinbox_trigger_sensitivity_lm, self.spinbox_trigger_sensitivity_li, self.spinbox_trigger_sensitivity_lt, self.spinbox_trigger_sensitivity_rt, self.spinbox_trigger_sensitivity_ri, self.spinbox_trigger_sensitivity_rm, self.spinbox_trigger_sensitivity_rr, self.spinbox_trigger_sensitivity_rp]

        # Hide Hands and markers for calibration and show graph
        self.label_hand_l.hide()
        self.label_hand_r.hide()
        
        # Find peaks for each button
        for i in range(10): # iterate through all buttons
            button_idx = i + 5  # buttons start with fifth index
            peakind[i] = signal.find_peaks_cwt(sensor_data[:, button_idx], np.arange(3,40))
            # Remove all peaks smaller than 250
            if len(peakind[i]) > 0:
                peakind[i] = peakind[i][sensor_data[:, button_idx][peakind[i]] > KEYBOARD_PEAK_THRESHOLD]   
            # Update min and max peak index value 
            if len(peakind[i]) > 0:
                if peakind[i].min() < peakind_min:
                    peakind_min = peakind[i].min()
                if peakind[i].max() > peakind_max:
                    peakind_max = peakind[i].max()

            # Collect peaks for each button and calc std for export
            for peak in peakind[i]:
                self.keyboard_peaks[i].append(sensor_data[:, button_idx][peak])

            if len(self.keyboard_peaks[i]) > 0:
                self.keyboard_peaks_std.append(np.std(self.keyboard_peaks[i]))
            else:
                self.keyboard_peaks_std.append(None)

            # Plot graph for each button and mark peaks with "x"
            if len(peakind[i]) > 0:
                self.graphWidget_keyboard.plot(peakind[i], sensor_data[:, button_idx][peakind[i]], symbol="x", pen=pg.mkPen('w', width=0))
            self.graphWidget_keyboard.plot(range(sensor_data[:, button_idx].size), sensor_data[:, button_idx]).setZValue(10)

            # Set button sensitivity
            if len(self.keyboard_peaks[i]) > 0:
                self.spinbox_trigger_sensitivity[i].setValue((1000 - KEYBOARD_TRIGGER_THRESHOLD_FACTOR * (sum(self.keyboard_peaks[i]) / len(self.keyboard_peaks[i]))) / 10.)

        # Add Legend to graph (must be called before curves)
        self.graphWidget_keyboard.addLegend().setOffset((5,5))
        # Fit graph to peak range
        self.graphWidget_keyboard.setXRange(peakind_min-100, peakind_max+100, padding=0) 
        
        # Calculate trigger and release threshhold based on button inputs
        # if len(self.keyboard_peaks) > 0:
        #     self.spinbox_trigger_threshold.setValue((1000 - KEYBOARD_TRIGGER_THRESHOLD_FACTOR * (sum(self.keyboard_peaks) / len(self.keyboard_peaks))) / 10.)
            # (1000 - (MOUSE_TRIGGER_THRESHOLD_FACTOR * (sum(self.mouse_peaks) / len(self.mouse_peaks)))) / 10.
            # self.spinbox_release_threshold.setValue(KEYBOARD_RELEASE_THRESHOLD_FACTOR * self.spinbox_trigger_threshold.value())
            # Draw trigger and release threshold
            # self.graphWidget_keyboard.plot([peakind_min-100, peakind_max+100], [KEYBOARD_TRIGGER_THRESHOLD_FACTOR * (sum(self.keyboard_peaks) / len(self.keyboard_peaks)), KEYBOARD_TRIGGER_THRESHOLD_FACTOR * (sum(self.keyboard_peaks) / len(self.keyboard_peaks))], pen=pg.mkPen(color=(50, 168, 82)), name="Trigger").setZValue(11)
            # self.graphWidget_keyboard.plot([peakind_min-100, peakind_max+100], [self.spinbox_release_threshold.value() / 100) * KEYBOARD_TRIGGER_THRESHOLD_FACTOR * (sum(self.keyboard_peaks) / len(self.keyboard_peaks)), self.spinbox_release_threshold.value()], pen=pg.mkPen(color=(237, 143, 50)), name="Release").setZValue(11)
            # Set labels with results
            # self.label_keyboard_trigger.setText(str(int(KEYBOARD_TRIGGER_THRESHOLD_FACTOR * (sum(self.keyboard_peaks) / len(self.keyboard_peaks)))))
            # self.label_keyboard_release.setText(str(int(KEYBOARD_RELEASE_THRESHOLD_FACTOR * self.spinbox_trigger_threshold.value())))
            # self.label_keyboard_std.setText("{:.2f}".format(np.std(self.keyboard_peaks)))

        # Hide instructions and show plot
        for finger_marker_label in self.finger_marker_labels:
            finger_marker_label.hide()
        self.label_l.hide()
        self.label_r.hide()
        self.graphWidget_keyboard.show()


    def processLongPress(self, sensor_data):
        """Saves the long press durations in the UI

        Args:
            sensor_data (list): List of floats for each button press duration
        """
        self.long_press_durations = sensor_data
        self.long_press_durations_std = np.std(sensor_data)
        self.spinbox_long_press_duration.setValue(np.mean(sensor_data))
        self.spinbox_retrigger_duration.setValue(np.mean(sensor_data))


    def processScreenBoundaries(self, screen_boundaries):
        """Set Screen boundary values in GUI

        Args:
            screen_boundaries (list): List of tuples with int containing screen boundaries
        """
        self.spinbox_left_boundary.setValue(screen_boundaries[0][0])
        self.spinbox_right_boundary.setValue(screen_boundaries[1][0])
        self.spinbox_upper_boundary.setValue(screen_boundaries[1][1])
        self.spinbox_lower_boundary.setValue(screen_boundaries[0][1])

        self.label_min_values.setText("({}, {})".format(screen_boundaries[0][0], screen_boundaries[0][1]))
        self.label_max_values.setText("({}, {})".format(screen_boundaries[1][0], screen_boundaries[1][1]))


    def processScrollBoundaries(self, scroll_boundaries):
        """Set Scroll boundary values in GUI

        Args:
            scroll_boundaries (list): List of tuples with float containing screen boundaries (trigger and release)
        """
        self.spinbox_scroll_up_trigger.setValue(scroll_boundaries[0])
        self.spinbox_scroll_down_trigger.setValue(scroll_boundaries[1])

        self.label_scroll_up.setText("{:.2f}°".format(scroll_boundaries[0]))
        self.label_scroll_down.setText("{:.2f}°".format(scroll_boundaries[1]))


    def exportMouse(self):
        # Save Dialog
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Mouse Calibration", "W:\EFFENDI/S_M{}.csv".format(self.comboBox_keyboard_calibration_stroke.currentText()), "CSV File (*.csv)", options=options)
        
        if file_path:
            # file_name = os.path.splitext(os.path.split(file_path)[1])[0]
            dict = {"mouse_peaks": self.mouse_peaks,
                    "standard_deviation": np.std(self.mouse_peaks)}
            df = pd.DataFrame(dict) 
    
            # saving the dataframe 
            df.to_csv(file_path, index=False)


    def exportKeyboard(self):
        # Save Dialog
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Keyboard Calibration", "W:\EFFENDI/S_K{}.csv".format(self.comboBox_keyboard_calibration_stroke.currentText()), "CSV File (*.csv)", options=options)
        
        if file_path:
            # file_name = os.path.splitext(os.path.split(file_path)[1])[0]
            dict = {"keyboard_peaks": self.keyboard_peaks,
                    "standard_deviation": self.keyboard_peaks_std}
            df = pd.DataFrame(dict) 
    
            # saving the dataframe 
            df.to_csv(file_path, index=False) 


    def exportKeyboardPressure(self):
        # Save Dialog
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Keyboard Pressure Calibration", "W:\EFFENDI/S_P.csv", "CSV File (*.csv)", options=options)
        
        if file_path:
            # file_name = os.path.splitext(os.path.split(file_path)[1])[0]
            dict = {"keyboard_pressure": self.keyboard_pressure}
                    # "standard_deviation": self.keyboard_peaks_std}
            df = pd.DataFrame(dict) 
    
            # saving the dataframe 
            df.to_csv(file_path, index=False) 


    def exportLongPress(self):
        # Save Dialog
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Long Press", "W:\EFFENDI/S_L{}.csv".format(self.comboBox_keyboard_calibration_stroke.currentText()), "CSV File (*.csv)", options=options)
        
        if file_path:
            dict = {"long_press_durations": self.long_press_durations,
                    "standard_deviation": self.long_press_durations_std}
            df = pd.DataFrame(dict) 
    
            # saving the dataframe 
            df.to_csv(file_path, index=False) 


class FitGlasses(QObject):

    fsr_mouse = pyqtSignal(tuple)
    finished = pyqtSignal()

    def __init__(self, event, gui_queue, mode):
        super(FitGlasses, self).__init__()
        self.event = event
        self.gui_queue = gui_queue
        self.mode = mode
        self.active = True
        self.mouse_pressure = None

        # Empty queue before calibration
        with self.gui_queue.mutex:
            self.gui_queue.queue.clear()

    # def proximityToMillimeter(self, proximity):
    #     """Translate proximity measurement for mouse click into mm

    #     Args:
    #         proximity (int): Proximity value without unit and exponential behavior

    #     Returns:
    #         float: Proximity in mm
    #     """
    #     proximity_mm = 18.90639 - (0.001051379/0.00006224794)*(1 - math.exp(-0.00006224794*proximity))
    #     return proximity_mm

    def run(self):
        """ Measures Mouse Fit based on FSR values.
        """
        if self.mode == "Proximity":
            data = self.gui_queue.get()
            coordinate = data.split(',')
            #self.mouse_pressure = self.proximityToMillimeter(int(coordinate[15]))    # returns initial pressure
            self.mouse_pressure = int(coordinate[15])   # returns initial pressure
            print(self.mouse_pressure)
            print(int(coordinate[15]))
        
        while self.active is True:
            data = self.gui_queue.get()
            coordinate = data.split(',')

            try:
                if self.mode == "Force":
                    mouse_press = (int(coordinate[3]), int(coordinate[4]))
                    self.mouse_pressure = (int(coordinate[3]) + int(coordinate[4])) / (2 * 10)    # returns initial pressure in %
                elif self.mode == "Proximity":
                    #mouse_press = (self.proximityToMillimeter(int(coordinate[15])), self.proximityToMillimeter(int(coordinate[15])))
                    mouse_press = (int(coordinate[15]), int(coordinate[15]))
                    #self.mouse_pressure = int(coordinate[15])
                    # print(mouse_press[0])
                    # print(int(coordinate[15]))

                self.fsr_mouse.emit(mouse_press)
            
            except Exception as e:
                print("Exception: {}".format(str(e)))

        self.finished.emit()    # reactivate pushbutton
        return # to trigger delete later


class ReadSensor(QObject):
    """Reads Sensor information and emits signal to update progress bar

    Args:
        QObject (QObject): PyQt Object
    """

    countChanged = pyqtSignal(float)
    updateFingerMarker = pyqtSignal(int, int)
    passSensorData = pyqtSignal(np.ndarray)
    finished = pyqtSignal()

    def __init__(self, event, gui_queue, write_queue, calibration_strokes, device, mouse_pressure_f, mouse_pressure_p, keyboard_pressure, active_keys, mode=0):
        super(ReadSensor, self).__init__()
        self.event = event
        self.gui_queue = gui_queue
        self.write_queue = write_queue
        self.device = device
        self.mouse_pressure_f = mouse_pressure_f
        self.mouse_pressure_p = mouse_pressure_p
        self.keyboard_pressure = keyboard_pressure
        self.active_keys = active_keys
        self.mode = mode

        self.strokes = 0
        self.sensor_input = []
        self.long_press = []
        self.long_press_start = None
        self.start_time = time.time()
        self.running = True

        # is True when sensor value is above defined threshold
        if device == "mouse":
            self.above_threshold = [False]*2    
            self.calibration_strokes = calibration_strokes
        elif device == "keyboard":
            self.above_threshold = False
            # self.above_threshold = [False]*10
            self.calibration_strokes = calibration_strokes * len(active_keys)
        elif device == "long_press":
            # self.above_threshold = False
            self.calibration_strokes = calibration_strokes

        # Empty queue before calibration
        with self.gui_queue.mutex:
            self.gui_queue.queue.clear()

    # def proximityToMillimeter(self, proximity):
    #     """Translate proximity measurement for mouse click into mm

    #     Args:
    #         proximity (int): Proximity value without unit and exponential behavior

    #     Returns:
    #         float: Proximity in mm
    #     """
    #     proximity_mm = 18.90639 - (0.001051379/0.00006224794)*(1 - math.exp(-0.00006224794*proximity))
    #     return proximity_mm

    def run(self):

        while not self.event.is_set() and self.running is True:
            data = self.gui_queue.get()
            coordinate = data.split(',')
            try:
                np.asarray(coordinate).astype(float)    # validate coordinate list, throw exception else
                if len(coordinate) > 16:
                    print("Data corrupted")
                    continue
            except Exception as e:
                print("Exception: invalid argument in list")

            # Count strokes for keyboard or mouse calibration
            if self.device == "mouse":
                if self.mode == "Force":
                    if ((int(coordinate[3]) + int(coordinate[4])) / 2) > (MOUSE_PEAK_THRESHOLD + self.mouse_pressure_f * 10):
                        self.above_threshold = True
                        self.write_queue.put(b'2')
                        self.write_queue.put(b'1')
                    elif ((int(coordinate[3]) + int(coordinate[4])) / 2) < (MOUSE_PEAK_THRESHOLD + self.mouse_pressure_f * 10) and self.above_threshold == True:
                        self.strokes += 1
                        self.above_threshold = False
                # elif self.mode == "Proximity":
                #     print(self.proximityToMillimeter(int(coordinate[15])))
                #     print(self.mouse_pressure)
                #     print(self.proximityToMillimeter(int(coordinate[15])) - self.mouse_pressure)
                #     print(abs(self.proximityToMillimeter(int(coordinate[15])) - self.mouse_pressure))
                #     if abs(self.proximityToMillimeter(int(coordinate[15])) - self.mouse_pressure) > MOUSE_PEAK_THRESHOLD_PROX:
                #         self.above_threshold = True
                #         self.write_queue.put(b'2')
                #         self.write_queue.put(b'1')
                #     elif abs(self.proximityToMillimeter(int(coordinate[15])) - self.mouse_pressure) < MOUSE_PEAK_THRESHOLD_PROX and self.above_threshold == True:
                #         self.strokes += 1
                #         self.above_threshold = False

                #     coordinate[15] = abs(self.proximityToMillimeter(int(coordinate[15])) - self.mouse_pressure)

                elif self.mode == "Proximity":
                    # if int(coordinate[15]) - self.mouse_pressure_p > MOUSE_PEAK_THRESHOLD_PROX * self.mouse_pressure_p:
                    if int(coordinate[15]) > MOUSE_PEAK_THRESHOLD_PROX * self.mouse_pressure_p:
                        self.above_threshold = True
                        self.write_queue.put(b'2')
                        self.write_queue.put(b'1')
                    # elif int(coordinate[15]) - self.mouse_pressure_p < MOUSE_PEAK_THRESHOLD_PROX * self.mouse_pressure_p and self.above_threshold == True:
                    elif int(coordinate[15]) < MOUSE_PEAK_THRESHOLD_PROX * self.mouse_pressure_p and self.above_threshold == True:
                        self.strokes += 1
                        self.above_threshold = False

                    # coordinate[15] = int(coordinate[15]) - self.mouse_pressure_p

                progress = round(100 * self.strokes / self.calibration_strokes)

                self.sensor_input.append(coordinate)

                if self.strokes >= self.calibration_strokes:
                    self.running = False

            elif self.device == "keyboard":
                # determine the key to be calibrated
                idx = int(np.floor(self.strokes / (self.calibration_strokes / len(self.active_keys))))
                
                while self.active_keys[idx] is False:
                    idx += 1
                    self.strokes += int(self.calibration_strokes / len(self.active_keys))
                    if idx >= len(self.active_keys):
                        self.running = False
                        idx = len(self.active_keys) - 1
                        break


                self.updateFingerMarker.emit(idx, int((self.calibration_strokes / len(self.active_keys)) - (self.strokes % (self.calibration_strokes / len(self.active_keys)))))

                # set all values to 0 that are not from the current key of interest
                for i in range(10):
                    if i != idx:
                        coordinate[i+5] = 0
                # Press
                if int(coordinate[idx+5]) > (KEYBOARD_PEAK_THRESHOLD + self.keyboard_pressure[idx]*10):
                    self.above_threshold = True
                    # causes misclassifications
                    # if i < 5:
                    #     self.write_queue.put(b'2')
                    # else:
                    #     self.write_queue.put(b'1')
                # Release
                elif int(coordinate[idx+5]) < (KEYBOARD_PEAK_THRESHOLD + self.keyboard_pressure[idx]*10) and self.above_threshold == True:
                    self.strokes += 1
                    self.above_threshold = False

                progress = round(100 * self.strokes / self.calibration_strokes)
                # self.updateFingerMarker.emit(int(np.floor(self.strokes / (self.calibration_strokes / len(self.active_keys)))), int((self.calibration_strokes / len(self.active_keys)) - (self.strokes % (self.calibration_strokes / len(self.active_keys)))))

                self.sensor_input.append(coordinate)

                if self.strokes >= self.calibration_strokes-1:
                    self.running = False

            elif self.device == "pressure":
                progress = round(100 * (time.time() - self.start_time) / 5.)

                self.sensor_input.append(coordinate)

                if (time.time() - self.start_time) > 5.:
                    self.running = False

            elif self.device == "long_press":
                if int(coordinate[10]) > (KEYBOARD_PEAK_THRESHOLD + self.keyboard_pressure[5]*10) and self.long_press_start is None:
                    # self.above_threshold = True
                    self.long_press_start = time.time()
                    self.write_queue.put(b'1')
                elif int(coordinate[10]) < (KEYBOARD_PEAK_THRESHOLD + self.keyboard_pressure[5]*10) and self.long_press_start is not None:
                    self.strokes += 1
                    # self.above_threshold = False
                    self.long_press.append(time.time() - self.long_press_start)
                    self.long_press_start = None

                progress = round(100 * self.strokes / self.calibration_strokes)

                if self.strokes >= self.calibration_strokes:
                    self.running = False
                
            # Update progress bar
            self.countChanged.emit(progress)
            
        if self.device == "long_press":
            sensor_data = np.array(self.long_press, dtype=float)
        else:
            sensor_data = np.array(self.sensor_input, dtype=float)
        self.passSensorData.emit(sensor_data)   # pass Sensor data to other class for further processing
        self.finished.emit()    # reactivate pushbutton
        return # to trigger delete later


class GetScreenBoundaries(QObject):

    passBoundaries = pyqtSignal(list)
    finished = pyqtSignal()

    def __init__(self, event, gui_queue, write_queue, mouse_click_sensitivity_f, mouse_click_sensitivity_p, mouse_release_sensitivity_f, mouse_release_sensitivity_p, mode):
        super(GetScreenBoundaries, self).__init__()
        self.event = event
        self.gui_queue = gui_queue
        self.write_queue = write_queue
        self.mouse_click_sensitivity_f = mouse_click_sensitivity_f
        self.mouse_click_sensitivity_p = mouse_click_sensitivity_p
        self.mouse_release_sensitivity_f = mouse_release_sensitivity_f
        self.mouse_release_sensitivity_p = mouse_release_sensitivity_p
        self.mode = mode
        self.screen_boundaries = []
        self.mouse_pressed = False

        # Empty queue before calibration
        with self.gui_queue.mutex:
            self.gui_queue.queue.clear()

    def run(self):
        """ Gets screen boundaries during mouse movement calibration on mouse click trigger.
        First click will determine lower left boundary and second click upper right boundary.
        """
        
        while not self.event.is_set() and len(self.screen_boundaries) < 2:
            data = self.gui_queue.get()
            coordinate = data.split(',')

            try:
                if self.mode == "Force":
                    mouse_press = (int(coordinate[3]) + int(coordinate[4])) / 2
                        
                    # Read boundary value when mouse button pressed
                    if self.mouse_pressed is False and mouse_press >= 10 * (100 - self.mouse_click_sensitivity_f):
                        # Activate vibration motors
                        if len(self.screen_boundaries) == 0:
                            self.write_queue.put(b'1')
                        else:
                            self.write_queue.put(b'2')
                        # Save boundary value
                        self.screen_boundaries.append((float(coordinate[0]), float(coordinate[1])))
                        self.mouse_pressed = True

                    if self.mouse_pressed is True and mouse_press < (self.mouse_release_sensitivity_f / 100) * 10 * (100 - self.mouse_click_sensitivity_f):
                        self.mouse_pressed = False

                elif self.mode == "Proximity":
                    mouse_press = int(coordinate[15])
                    #print(coordinate[15])
                        
                    # Read boundary value when mouse button pressed
                    if self.mouse_pressed is False and mouse_press >= self.mouse_click_sensitivity_p:
                        # Activate vibration motors
                        if len(self.screen_boundaries) == 0:
                            self.write_queue.put(b'1')
                        else:
                            self.write_queue.put(b'2')
                        # Save boundary value
                        print("mouse pressed")
                        #print(coordinate[0])
                        self.screen_boundaries.append((float(coordinate[0]), float(coordinate[1])))
                        self.mouse_pressed = True
                        print(self.screen_boundaries)
                        print(self.mouse_release_sensitivity_p)

                    if self.mouse_pressed is True and mouse_press < self.mouse_release_sensitivity_p:
                        self.mouse_pressed = False
                        print("mouse released")
                        print(self.screen_boundaries)
            
            except Exception as e:
                print("Exception: {}".format(str(e)))

        self.passBoundaries.emit(self.screen_boundaries)    # pass boundaries to other class
        self.finished.emit()    # reactivate pushbutton
        return # to trigger delete later


class GetScrollBoundaries(QObject):

    passBoundaries = pyqtSignal(list)
    finished = pyqtSignal()

    def __init__(self, event, gui_queue, write_queue, mouse_click_sensitivity_f, mouse_click_sensitivity_p, mouse_release_sensitivity_f, mouse_release_sensitivity_p, mode):
        super(GetScrollBoundaries, self).__init__()
        self.event = event
        self.gui_queue = gui_queue
        self.write_queue = write_queue
        self.mouse_click_sensitivity_f = mouse_click_sensitivity_f
        self.mouse_click_sensitivity_p = mouse_click_sensitivity_p
        self.mouse_release_sensitivity_f = mouse_release_sensitivity_f
        self.mouse_release_sensitivity_p = mouse_release_sensitivity_p
        self.mode = mode
        self.scroll_boundaries = []
        self.mouse_pressed = False

        # Empty queue before calibration
        with self.gui_queue.mutex:
            self.gui_queue.queue.clear()

    def run(self):
        """ Gets scroll boundaries mouse click trigger.
        First click will determine boundary of left head roll to scroll up and second click right head roll for scrolling down.
        """
        
        while not self.event.is_set() and len(self.scroll_boundaries) < 2:
            data = self.gui_queue.get()
            coordinate = data.split(',')

            try:
                if self.mode == "Force":
                    mouse_press = (int(coordinate[3]) + int(coordinate[4])) / 2
                        
                    # Read boundary value when mouse button pressed
                    if self.mouse_pressed is False and mouse_press >= 10 * (100 - self.mouse_click_sensitivity_f):
                        # Activate vibration motors
                        if len(self.scroll_boundaries) == 0:
                            self.write_queue.put(b'1')
                        else:
                            self.write_queue.put(b'2')
                        # Save boundary value
                        self.scroll_boundaries.append(SCROLL_TRIGGER_THRESHOLD_FACTOR * float(coordinate[2]))
                        self.mouse_pressed = True

                    if self.mouse_pressed is True and mouse_press < (self.mouse_release_sensitivity_f / 100) * 10 * (100 - self.mouse_click_sensitivity_f):
                        self.mouse_pressed = False

                elif self.mode == "Proximity":
                    mouse_press = int(coordinate[15])
                        
                    # Read boundary value when mouse button pressed
                    if self.mouse_pressed is False and mouse_press >= self.mouse_click_sensitivity_p:
                        # Activate vibration motors
                        if len(self.scroll_boundaries) == 0:
                            self.write_queue.put(b'1')
                        else:
                            self.write_queue.put(b'2')
                        # Save boundary value
                        self.scroll_boundaries.append(SCROLL_TRIGGER_THRESHOLD_FACTOR * float(coordinate[2]))
                        self.mouse_pressed = True

                    if self.mouse_pressed is True and mouse_press < self.mouse_release_sensitivity_p:
                        self.mouse_pressed = False
            
            except Exception as e:
                print("Exception: {}".format(str(e)))

        self.passBoundaries.emit(self.scroll_boundaries)    # pass boundaries to other class
        self.finished.emit()    # reactivate pushbutton
        return # to trigger delete later