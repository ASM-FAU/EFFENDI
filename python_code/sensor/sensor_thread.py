import threading
import serial


class SensorReader(threading.Thread):

    def __init__(self, name, port, event, mouse_queue, gui_queue, write_queue, desktop):
        threading.Thread.__init__(self)
        self.name = name
        self.event = event
        self.mouse_queue = mouse_queue
        self.gui_queue = gui_queue
        self.write_queue = write_queue
        self.desktop = desktop
        self.baudrate = 115200
        self.port = port
        self.connected = False
        self.arduino = serial.Serial(self.port, self.baudrate)
        self.write_to_arduino(b'G') # make LED turn Green

    def write_to_arduino(self, data):
        try:
            if not self.connected:
                self.arduino.readline()
                self.connected = True
            self.arduino.write(data)
        except:
            print("Connection failed!")
            pass

    def run(self):
        ignore_counter = 0
        pressed = []
        for i in range(10):
            pressed.append(False)
        while not self.event.is_set():

            if not self.write_queue.empty():
                self.write_to_arduino(self.write_queue.get())

            try:
                data = self.arduino.readline()
            except Exception as e:
                print("Could not read sensor data, due to: {}".format(str(e)))
                return

            # Ignore first xx data samples from sensors and then stream data (only for desktop application)
            if self.desktop is True and ignore_counter < 1050:
                ignore_counter += 1
            else:
                newData = data.decode("ISO-8859-1")
                newData = newData[:-2]
                self.mouse_queue.put(newData)
                self.gui_queue.put(newData)
