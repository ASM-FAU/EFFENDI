import threading
import pyautogui
import time
import math
from ctypes import windll#, Structure, c_long, byref   


pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0 # remove delay
baudrate = 115200


# class POINT(Structure):
#     _fields_ = [("x", c_long), ("y", c_long)]   


class MouseControl(threading.Thread):
    # Pulling the actual position of the mouse

    def __init__(self, name, desktop, gui, min_sensor_value_x, max_sensor_value_x, min_sensor_value_y, max_sensor_value_y, mouse_click_sensitivity_f, mouse_click_sensitivity_p, mouse_release_sensitivity_f, mouse_release_sensitivity_p, mouse_cursor_sensitivity, scroll_up_trigger, scroll_down_trigger, scroll_release_sensitivity, scroll_speed, right_click_duration, recenter_mouse_duration, tolerated_mouse_movement, trigger_mouse_down, mouse_acceleration, event, queue, write_queue, prox_mode):
        threading.Thread.__init__(self)
        self.name = name
        self.desktop = desktop
        self.queue = queue
        self.write_queue = write_queue
        self.event = event
        self.min_sensor_value_x = min_sensor_value_x
        self.max_sensor_value_x = max_sensor_value_x
        self.min_sensor_value_y = min_sensor_value_y
        self.max_sensor_value_y = max_sensor_value_y
        self.mouse_click_sensitivity_f = mouse_click_sensitivity_f
        self.mouse_click_sensitivity_p = mouse_click_sensitivity_p
        self.mouse_release_sensitivity_f = mouse_release_sensitivity_f
        self.mouse_release_sensitivity_p = mouse_release_sensitivity_p
        self.mouse_cursor_sensitivity = mouse_cursor_sensitivity
        self.scroll_up_trigger = scroll_up_trigger
        self.scroll_down_trigger = scroll_down_trigger
        self.scroll_release_sensitivity = scroll_release_sensitivity
        self.scroll_speed = scroll_speed
        self.right_click_duration = right_click_duration
        self.recenter_mouse_duration = recenter_mouse_duration
        self.tolerated_mouse_movement = tolerated_mouse_movement
        self.trigger_mouse_down = trigger_mouse_down
        self.mouse_acceleration = mouse_acceleration
        self.prox_mode = prox_mode
        # self.disable_mouse = disable_mouse

        # Detect screen size and resolution
        self.screen_width, self.screen_height = pyautogui.size()
        # Recenter
        self.recenter_x_pixels = 0
        self.recenter_y_pixels = 0
        self.recenter_x_phi = 0
        self.recenter_y_phi = 0

        if self.desktop is True:
            self.effendi_window_id = gui.ui.effendi_window_id
            print('EFFENDI Window ID: {}'.format(self.effendi_window_id))
            self.focused_window = windll.user32.GetForegroundWindow()

    # def getMousePosition(self):
    #     pos = win32api.GetCursorPos()
    #     return pos[0], pos[1]

    # def getMousePosition(self):
    #     pos = POINT()
    #     windll.user32.GetCursorPos(byref(pos))
    #     return pos.x, pos.y


    # According to X, Y values setting the mouse position
    def moveMouse(self, x, y):
        windll.user32.SetCursorPos(x, y)


    def translate_x(self, sensor_x):
        """Move horizontal mouse cursor position according to new sensor values

        Args:
            sensor_x (float): Horizontal position in degrees

        Returns:
            float: Updated horizontal cursor position in pixels
        """
        out_val = 0
        if self.mouse_acceleration is True:
            in_range = float(abs(self.max_sensor_value_x - self.min_sensor_value_x))    # 2*phi_ges
            # in_val = float(sensor_x - self.min_sensor_value_x) - (in_range / 2.)             # phi= -phi_ges to +phi_ges
            in_val = float(sensor_x - self.min_sensor_value_x + self.recenter_x_phi) - (in_range / 2.)             # phi= -phi_ges to +phi_ges
            out_val = (math.tan(math.radians(float(in_val))) / math.tan(math.radians(in_range / 2.))) * float(self.screen_width / 2.) + float(self.screen_width / 2.)
            print(math.tan(math.radians(float(in_val))))
            #TODO recenter does not work here yet, center must be maintained since tan is not linear
        else:
            in_range = float(abs(self.max_sensor_value_x - self.min_sensor_value_x))
            in_val = sensor_x - self.min_sensor_value_x / ((self.mouse_cursor_sensitivity / 100) * 2)
            out_val = (float(in_val) / in_range) * float(self.screen_width) * ((self.mouse_cursor_sensitivity / 100) * 2)
            out_val += self.recenter_x_pixels
        return out_val


    def translate_y(self, sensor_y):
        """Move vertical mouse cursor position according to new sensor values

        Args:
            sensor_y (float): Vertical position in degrees

        Returns:
            float: Updated vertical cursor position in pixels
        """
        out_val = 0
        if self.mouse_acceleration is True:
            in_range = float(abs(self.max_sensor_value_y - self.min_sensor_value_y))    # 2*phi_ges
            # in_val = float(sensor_y - self.min_sensor_value_y) - (in_range / 2.)             # phi= -phi_ges to +phi_ges
            in_val = float(sensor_y - self.min_sensor_value_y + self.recenter_y_phi) - (in_range / 2.)             # phi= -phi_ges to +phi_ges
            out_val = (math.tan(math.radians(float(in_val))) / math.tan(math.radians(in_range / 2.))) * float(self.screen_height / 2) + float(self.screen_height / 2)
        else:
            in_range = float(abs(self.max_sensor_value_y - self.min_sensor_value_y))
            in_val = sensor_y - self.max_sensor_value_y / ((self.mouse_cursor_sensitivity / 100) * 2)
            out_val = (float(in_val) / in_range) * float(self.screen_height) * ((self.mouse_cursor_sensitivity / 100) * 2)
            out_val += self.recenter_y_pixels
        return out_val


    def recenterMouse(self, sensor_x, sensor_y, horizontal, vertical):
        """Computes a value to recenter the mouse by o´pixels or degrees in translate function. Depends on whether mouse acceleration is on or off.

        Args:
            sensor_x (float): Horizontal position in degrees
            sensor_y (float): Vertical position in degrees
            horizontal (int): Horizontal position in pixels
            vertical (int): Vertical position in pixels
        """
        if self.mouse_acceleration is True:
            self.recenter_x_phi = self.min_sensor_value_x + float(abs(self.max_sensor_value_x - self.min_sensor_value_x) / 2.) - sensor_x   # degrees
            self.recenter_y_phi = self.min_sensor_value_y + float(abs(self.max_sensor_value_y - self.min_sensor_value_y) / 2.) - sensor_y
        else:
            self.recenter_x_pixels = int(self.screen_width / 2 - horizontal + self.recenter_x_pixels) # pixels
            self.recenter_y_pixels = int(self.screen_height / 2 - vertical + self.recenter_y_pixels)


    def run(self):
        """This method runs a loop to update cursor position and trigger mouse clicks
        """
        system_startup = True
        ignore_counter = 0
        mouseDown = False
        dragDrop = False
        rightClicked = False
        recentered = False
        scrolling = False
        mouse_down_time = False

        horizontal = 0
        vertical = 0
        horizontal_prev = 0
        vertical_prev = 0

        # print(self.event.is_set())

        while not self.event.is_set():
            newValue = self.queue.get()

            # Split the value that comes from serial port ','
            coordinate = newValue.split(',')
            # print(coordinate)

            # The X and Y coordinate of the sensor
            # If you do want to pass a string representation of a float to an int, you can convert to a float first, then to an integer
            try:
                sensor_x = float(coordinate[0])
                sensor_y = float(coordinate[1])

                horizontal = int(self.translate_x(sensor_x))
                vertical = int(self.translate_y(sensor_y))

                # Recenter mouse at startup
                if system_startup is True and ignore_counter > 10:
                    self.recenterMouse(sensor_x, sensor_y, horizontal, vertical)
                    system_startup = False
                elif system_startup is True and ignore_counter <=10:
                    ignore_counter += 1

                # Set mouse position to new calculated position
                # if self.disable_mouse is False:
                self.moveMouse(horizontal, vertical)
                # print("x: {}, y: {}".format(horizontal, vertical))

            except Exception as e: 
                print(e)
                print("Could not read sensor this time.")

            # Scroll function
            try:
                scroll = float(coordinate[2])
            except:
                scroll = 0
                print("FSR Value scroll: invalid value")

            # Trigger Scrolling up
            if scroll < self.scroll_up_trigger and not scrolling:
                scrolling = True
                pyautogui.scroll(self.scroll_speed)
            # Trigger Scrolling down
            elif scroll > self.scroll_down_trigger and not scrolling:
                scrolling = True
                pyautogui.scroll(-self.scroll_speed)
            # Keep scrolling up
            elif scrolling is True and scroll < self.scroll_release_sensitivity/100 * self.scroll_up_trigger:
                pyautogui.scroll(self.scroll_speed)
            # Keep scrolling down
            elif scrolling is True and scroll > self.scroll_release_sensitivity/100 * self.scroll_down_trigger:
                pyautogui.scroll(-self.scroll_speed)
            # Release scrolling up
            elif scrolling is True and scroll > self.scroll_release_sensitivity/100 * self.scroll_up_trigger:
                scrolling = False
            # Release scrolling down
            elif scrolling is True and scroll < self.scroll_release_sensitivity/100 * self.scroll_down_trigger:
                scrolling = False

            # Click function
            if self.prox_mode is False:
                try:
                    # computes average of both FSR from spectacles
                    currentValue1 = int(coordinate[3])
                    currentValue2 = int(coordinate[4])
                    currentValue = int((currentValue2 + currentValue1) / 2)
                except:
                    currentValue = 0
                    print("FSR Value: invalid value")

                # Mouse pressed
                if currentValue > (100. - self.mouse_click_sensitivity_f) * 10. and not mouseDown and not rightClicked:
                    mouseDown = True
                    mouse_down_time = time.time()
                    # for tolerance drag and drop
                    horizontal_prev = horizontal
                    vertical_prev = vertical

                    pyautogui.mouseDown()
                    self.write_queue.put(b'1')
                    self.write_queue.put(b'2')
                    if self.desktop is True:
                        if windll.user32.GetForegroundWindow() != self.effendi_window_id and windll.user32.GetForegroundWindow() != 0:
                            self.focused_window = windll.user32.GetForegroundWindow()
                        windll.user32.SetForegroundWindow(self.focused_window)
                        # print(self.focused_window)

                # Mouse released
                elif currentValue < (self.mouse_release_sensitivity_f / 100.) * (100. - self.mouse_click_sensitivity_f) * 10. and mouseDown:
                    mouse_down_time = False
                    mouseDown = False
                    dragDrop = False
                    recentered = False

                    if not rightClicked:
                        if self.trigger_mouse_down is True:
                            pyautogui.mouseUp(horizontal_prev, vertical_prev)
                        else:
                            pyautogui.mouseUp()
                    else:
                        rightClicked = False
                        
                # Right click and recenter
                if mouseDown and not dragDrop:
                    # Drag and drop
                    if not dragDrop and (abs(horizontal - horizontal_prev) > ((self.tolerated_mouse_movement / 100.) * self.screen_height) or abs(vertical - vertical_prev) > ((self.tolerated_mouse_movement / 100.) * self.screen_height)):
                        dragDrop = True
                    # right click
                    if time.time() - mouse_down_time > self.right_click_duration and not rightClicked and not dragDrop:
                        pyautogui.rightClick()
                        rightClicked = True
                    # recenter mouse
                    elif time.time() - mouse_down_time > self.recenter_mouse_duration and not recentered:
                        self.recenterMouse(sensor_x, sensor_y, horizontal, vertical)
                        recentered = True

            elif self.prox_mode is True:
                try:
                    currentValue = int(coordinate[15])
                except:
                    currentValue = 0
                    print("FSR Value: invalid value")

                # Mouse pressed
                if currentValue > self.mouse_click_sensitivity_p and not mouseDown and not rightClicked:
                    mouseDown = True
                    mouse_down_time = time.time()
                    # for tolerance drag and drop
                    horizontal_prev = horizontal
                    vertical_prev = vertical

                    pyautogui.mouseDown()
                    self.write_queue.put(b'1')
                    self.write_queue.put(b'2')
                    if self.desktop is True:
                        if windll.user32.GetForegroundWindow() != self.effendi_window_id and windll.user32.GetForegroundWindow() != 0:
                            self.focused_window = windll.user32.GetForegroundWindow()
                        windll.user32.SetForegroundWindow(self.focused_window)
                        # print(self.focused_window)

                # Mouse released
                elif currentValue < self.mouse_release_sensitivity_p and mouseDown:
                    mouse_down_time = False
                    mouseDown = False
                    dragDrop = False
                    recentered = False

                    if not rightClicked:
                        if self.trigger_mouse_down is True:
                            pyautogui.mouseUp(horizontal_prev, vertical_prev)
                        else:
                            pyautogui.mouseUp()
                    else:
                        rightClicked = False
                        
                # Right click and recenter
                if mouseDown and not dragDrop:
                    # Drag and drop
                    if not dragDrop and (abs(horizontal - horizontal_prev) > ((self.tolerated_mouse_movement / 100.) * self.screen_height) or abs(vertical - vertical_prev) > ((self.tolerated_mouse_movement / 100.) * self.screen_height)):
                        dragDrop = True
                    # right click
                    if time.time() - mouse_down_time > self.right_click_duration and not rightClicked and not dragDrop:
                        pyautogui.rightClick()
                        rightClicked = True
                    # recenter mouse
                    elif time.time() - mouse_down_time > self.recenter_mouse_duration and not recentered:
                        self.recenterMouse(sensor_x, sensor_y, horizontal, vertical)
                        recentered = True
