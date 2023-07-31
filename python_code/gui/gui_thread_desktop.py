import logging
import sys
import threading
import time

from PyQt5 import QtWidgets

from gui.openDesktopGui import DesktopUi


class DesktopGui:

    def __init__(self, name, event, queue, write_queue, t8_word_matching, keyboard_trigger_sensitivity, keyboard_release_sensitivity, keyboard_pressure, long_press_duration, retrigger_duration, keyboard_layout, next_key_idx, space_key_idx):
        self.name = name
        self.event = event
        self.queue = queue
        self.write_queue = write_queue
        self.keyboard_trigger_sensitivity = keyboard_trigger_sensitivity
        self.keyboard_release_sensitivity = keyboard_release_sensitivity
        self.keyboard_pressure = keyboard_pressure
        self.long_press_duration = long_press_duration
        self.retrigger_duration = retrigger_duration
        self.keyboard_layout = keyboard_layout
        self.next_key_idx = next_key_idx
        self.space_key_idx = space_key_idx

        self.gui = QtWidgets.QApplication(sys.argv)
        self.ui = DesktopUi(t8_word_matching)
        self.reading_sensor = threading.Thread(target=self.read_sensor)
        self.reading_sensor.start()

        # Distribute T9 code over active letters
        self.letter_code_list = [None]*len(keyboard_layout)
        letter_code = 2
        for i in range(len(keyboard_layout)):
            if keyboard_layout[i] is True and i != next_key_idx and i != space_key_idx:
                self.letter_code_list[i] = letter_code
                letter_code += 1


    def read_sensor(self):
        """This function is used to display button presses in the GUI.
        It iterates over each sensor and detects whether it has been pressed
        """
        pressed = [False] * 10 # init all buttons with state False (not pressed)
        button_trigger_time = [0] * 10
        button_longpress_time = [0] * 10
        ignore_counter = 0

        while not self.event.is_set():
            data = self.queue.get()
            coordinate = data.split(',')
            print(coordinate)

            # Ignore the 10 first iterations due to noise
            if ignore_counter < 10:
                ignore_counter += 1
            else:
                try:
                    # Iterate over keyboard keys
                    for i in range(10):
                        # Skip all deactivated keys
                        if self.keyboard_layout[i] is False:
                            continue

                        sensor = int(coordinate[i + 5]) # the indexes before are from imu and spectacles
                        
                        # Initial trigger of button press
                        # if pressed[i] is False and sensor >= ((100 - self.keyboard_trigger_sensitivity[i]) + self.keyboard_pressure[i]) * 10:
                        if pressed[i] is False and sensor >= (100 - self.keyboard_trigger_sensitivity[i]) * 10:
                            # trigger left or right vibration motor
                            if i < 5:
                                self.write_queue.put(b'2')
                            else:
                                self.write_queue.put(b'1')
                            # trigger action for click of T8 buttons in openGui.py
                            button_trigger_time[i] = time.time()
                            button_longpress_time[i] = button_trigger_time[i] + self.long_press_duration
                            if i != self.next_key_idx and i != self.space_key_idx:
                                self.ui.updateLetterCaseList(0)
                                # self.ui.buttons[i].click()
                                self.ui.clicked(str(self.letter_code_list[i]))
                            
                            # animate button down in GUI
                            # self.ui.buttons[i].setDown(True)
                            pressed[i] = True
                        
                        # Hold button longer than long press duration
                        # elif pressed[i] is True and sensor > ((self.keyboard_release_sensitivity / 100.) * (100 - self.keyboard_trigger_sensitivity[i]) + self.keyboard_pressure[i]) * 10:
                        elif pressed[i] is True and sensor > (self.keyboard_release_sensitivity / 100.) * (100 - self.keyboard_trigger_sensitivity[i]) * 10:
                            # trigger backspace when long pressing next button
                            if i == self.next_key_idx:  # next button
                                if time.time() >= button_longpress_time[i]:
                                    self.ui.backspaceClicked() # trigger backspace click
                                    button_longpress_time[i] += self.retrigger_duration
                                    # self.ui.button_backspace.setDown(True)
                                # animate button release in GUI after 100 ms
                                # if time.time() >= button_longpress_time[i] - self.retrigger_duration + 0.2:
                                #     self.ui.button_backspace.setDown(False)
                            # trigger enter when long pressing space button
                            elif i == self.space_key_idx:  # space button
                                if time.time() >= button_longpress_time[i]:
                                    self.ui.enterClicked() # trigger enter click
                                    button_longpress_time[i] += self.retrigger_duration
                            # Capitalize letters when long pressing
                            else: # all letter buttons
                                if time.time() >= button_longpress_time[i]:
                                    self.ui.updateLetterCaseList(1)
                                    button_longpress_time[i] += 9999    # letter buttons shall only be triggered once
                                    self.ui.generateText()
                                
                        # Release button before long press duration is reached
                        # elif pressed[i] is True and sensor <= ((self.keyboard_release_sensitivity / 100.) * (100 - self.keyboard_trigger_sensitivity[i]) + self.keyboard_pressure[i]) * 10:
                        elif pressed[i] is True and sensor <= (self.keyboard_release_sensitivity / 100.) * (100 - self.keyboard_trigger_sensitivity[i]) * 10:
                            if i == self.next_key_idx:  # next button and space button
                                if time.time() - button_trigger_time[i] < self.long_press_duration:
                                    self.ui.nextClicked()
                            elif i == self.space_key_idx:  # next button and space button
                                if time.time() - button_trigger_time[i] < self.long_press_duration:
                                    self.ui.spaceClicked()

                            pressed[i] = False
                            # animate button release in GUI
                            # self.ui.buttons[i].setDown(False)

                except Exception as e:
                    logging.warning("Exception: {}".format(str(e)))
