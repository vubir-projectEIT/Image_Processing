""" IMPORTS """

import time

import numpy as np
from serial import Serial
from serial.tools import list_ports
import re


""" CLASS """

class Controller:

    # Controller constants
    __PWM_MIN = 0
    __PWM_MAX = 511
    __LOGS_OFF = b"loff\r\n"
    __LOGS_ON = b"lon\r\n"
    __PRINTING_ON = b"hon\r\n"
    __PRINTING_OFF = b"hoff\r\n"

    # Dict of open ports
    __open_ports = {}

    # Override in order to control Serial object referencing
    def __new__(cls, port=None):

        # Get all available port names
        port_names = [e.name for e in list_ports.comports() if e.description.startswith("USB Serial Port")]

        if port is None:
            raise ConnectionError(f"port was not defined, available={port_names}")
            return None
        elif not (isinstance(port, str)):
            raise TypeError(f"expected {str}, got {type(port)}")
        elif port not in port_names:
            raise ConnectionError(f"port '{port}' not found in {port_names}")

        # Check if this port is managed by another object
        if port in cls.__open_ports.keys():
            obj = cls.__open_ports[port]
        else:
            obj = super().__new__(cls)
            obj.__serial = Serial(port, 115200, timeout=1)
            cls.__open_ports[port] = obj

        return obj

    # Sets fan speed pwm in range [0:100] percent
    def set_pwm(self, value: int):

        # Check input
        if not isinstance(value, (int, float)):
            raise TypeError(f"expected [{int}, {float}], got {type(value)}")

        # Format pwm into message for controller
        m = self.__format_message(value)

        # Send with response
        if self.__serial.is_open:
            self.__serial.write(m)
            response = self.__serial.readline().decode('utf-8')
        else:
            response = f"'{m}' failed to  send, port closed"

        # Return result
        return response

    # Toggle print
    def toggle_printing(self, enabled: bool):

        # Check input
        if not isinstance(enabled, bool):
            raise TypeError(f"expected {bool}, got {type(enabled)}")

        # Ensure port is open
        if not self.__serial.is_open:
            return

        elif enabled:
            self.__serial.write(Controller.__PRINTING_ON)
        else:
            self.__serial.write(Controller.__PRINTING_OFF)

        # Get response
        # s = self.__serial.readline().decode("utf-8")
        # print(f"toggle_printing={enabled}: response={s}")

    def toggle_logging(self, enabled: bool):

        if not isinstance(enabled, bool):
            raise TypeError(f"expected {type(bool)}, got {type(enabled)}")

        if not self.__serial.is_open:
            return

        if enabled:
            self.__serial.write(Controller.__PRINTING_ON)
        else:
            self.__serial.write(Controller.__PRINTING_OFF)

        # Get response
        s = self.__serial.readline().decode("utf-8")
        print(f"toggle_logging={enabled}: response={s}")

    # Retrieves height of ping ball from ping pong controller
    def get_ball_height(self, block_timeout=True):

        # Block until receipt
        while not len(r := self.__serial.readline()) and block_timeout:
            time.sleep(0.03)

        # Decode as string
        s = r.decode("utf-8")

        # Search using re
        p = r"[Hh]+[eight: ]*[0-9A-f]{4}"
        match = re.match(p, s)
        if match is not None:
            h = match[0][-4:]
            h = int(h, 16)
            return h
        else:
            return f"get_ball_height: response={s if len(s) else '<NULL>'}"


    # Format pwm into controller message
    @staticmethod
    def __format_message(pwm: int):

        # Clamp pwm between 0-100%
        if pwm < 0:
            pwm = 0
        elif pwm > 100:
            pwm = 100

        # Scale percent pwm
        pwm_range = Controller.__PWM_MAX - Controller.__PWM_MIN
        pwm = round(pwm_range * pwm * 0.01)

        return f"D{pwm:04x}\r\n".encode('utf-8')


    def __del__(self):
        if self.__serial.is_open:
            self.__serial.close()

        # Remove self from open controllers
        Controller.__open_ports.pop(self, None)


""" MAIN """

if __name__ == "__main__":

    # Instantiate the python controller
    c = Controller("COM5")

    # This will update available height data at 33Hz
    c.toggle_printing(True)

    while True:

        # Get the current ball height
        value = c.get_ball_height()
        print(f"Ball height is: {value}mm")

        # This is where you should do something intelligent with the height data
        pwm = 50 * np.sin(2 * np.pi * (1/3) * time.monotonic()) + 10  # Synthetic output

        # Send a new pwm value to the controller
        c.set_pwm(pwm)
