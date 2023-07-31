import logging
import sys
import threading
import time

from PyQt5 import QtWidgets

from gui.openGui import Ui
# from gui.gui_setup import SetupGUI


class Gui:

    def __init__(self, name, event, queue, write_queue, trigger_threshhold, release_threshhold, long_press_duration, retrigger_duration):
        self.name = name
        self.event = event
        self.queue = queue
        self.write_queue = write_queue
        self.trigger_threshhold = trigger_threshhold
        self.release_threshhold = release_threshhold
        self.long_press_duration = long_press_duration
        self.retrigger_duration = retrigger_duration

        self.gui = QtWidgets.QApplication(sys.argv)
        self.ui = Ui()
        self.reading_sensor = threading.Thread(target=self.read_sensor)
        self.reading_sensor.start()


    def read_sensor(self):
        """This function is used to display button presses in the GUI.
        It iterates over each sensor and detects whether it has been pressed

        """
        pressed = [False] * 10 # init all buttons with state False (not pressed)
        button_trigger_time = [0] * 10
        button_longpress_time = [0] * 10

        while not self.event.is_set():
            data = self.queue.get()
            coordinate = data.split(',')

            try:
                for i in range(10):
                    sensor = int(coordinate[i + 5])
                    
                    # Initial trigger of button press
                    if pressed[i] is False and sensor >= self.trigger_threshhold:
                        # trigger left or right vibration motor
                        if i < 5:
                            self.write_queue.put(b'2')
                        else:
                            self.write_queue.put(b'1')
                        # trigger action for click of T8 buttons in openGui.py
                        button_trigger_time[i] = time.time()
                        button_longpress_time[i] = button_trigger_time[i] + self.long_press_duration
                        if i != 4 and i != 5:
                            self.ui.updateLetterCaseList(0)
                            self.ui.buttons[i].click()
                        
                        # animate button down in GUI
                        self.ui.buttons[i].setDown(True)
                        pressed[i] = True
                        # logging.warning("Button {} pressed".format(i + 1))
                    
                    # Hold button longer than long press duration
                    elif pressed[i] is True and sensor > self.release_threshhold:
                        if i == 4:  # next button
                            # trigger backspace when long pressing next button
                            if time.time() >= button_longpress_time[i]:
                                self.ui.button_backspace.click() # trigger backspace click
                                button_longpress_time[i] += self.retrigger_duration
                                self.ui.button_backspace.setDown(True)
                            # animate button release in GUI after 100 ms
                            if time.time() >= button_longpress_time[i] - self.retrigger_duration + 0.2:
                                self.ui.button_backspace.setDown(False)

                        elif i == 5:  # space button
                            # trigger enter when long pressing space button
                            if time.time() >= button_longpress_time[i]:
                                self.ui.button_enter.click() # trigger enter click
                                button_longpress_time[i] += self.retrigger_duration

                        else: # all letter buttons
                            # transform last letter to upper case when long pressing
                            if time.time() >= button_longpress_time[i]:
                                self.ui.updateLetterCaseList(1)
                                button_longpress_time[i] += 9999    # letter buttons shall only be triggered once
                                self.ui.generateText()  
                            
                    # Release button before long press duration is reached
                    elif pressed[i] is True and sensor <= self.release_threshhold:
                        if i == 4 or i == 5:  # next button and space button
                            if time.time() - button_trigger_time[i] < self.long_press_duration:
                                self.ui.buttons[i].click()

                        pressed[i] = False
                        # animate button release in GUI
                        self.ui.buttons[i].setDown(False)

            except Exception as e:
                logging.warning("Exception: {}".format(str(e)))
