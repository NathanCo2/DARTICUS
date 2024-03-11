"""!
@file servo_driver.py
Creates a driver to run a servo using angle input

@author Nathan Chapman
@date   2024-03-08
"""

import pyb
import time

class ServoDriver:
    """! 
    This class implements a servo driver 
    """

    def __init__ (self, pwm, servo_min, servo_max, angle_range):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param ch: channel setup with timer at 50hz
        @param servo_min: minimum servo pulse width in microseconds
        @param servo_max: maximum servo pulse width in microseconds
        @param angle_range: servos physical angle range
        """
        self.pwm = pwm
        self.servo_min = servo_min
        self.servo_max = servo_max
        self.angle_range = angle_range
        self.pulse_width_range = servo_max - servo_min  # Range of pulse widths in µs
        
    def set_angle(self, angle):
        """!
        Sets angle of servo based on servo parameters
        @param angle: desired physical angle of motor
        """
        # Calculate the pulse width for the given angle
        self.pulse_width = int(((angle / self.angle_range) * self.pulse_width_range + self.servo_min) *3.2)
        self.pwm.pulse_width(self.pulse_width)
        print(f'Driving angle at {self.pulse_width} microsec pulse')

        
 
# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program       
if __name__ == "__main__":
    # Define pin assigments for example servo
    # setup PWM pin
    pinB0 = pyb.Pin.board.PB0
    # Timer channel 1
    TIM3 = pyb.Timer(3, freq=50) # 50hz is standard for servos
    ch3 = TIM3.channel(3,pyb.Timer.PWM, pin=pinB0)
    
#     # Define servo parameters 1501 MG
#     servo_min = 800  # Minimum pulse width for the servo (in microseconds)
#     servo_max = 2200  # Maximum pulse width for the servo (in microseconds)
#     angle_range = 165
    
#     # Define servo parameters MG 966R
#     servo_min = 1000  # Minimum pulse width for the servo (in microseconds)
#     servo_max = 2000  # Maximum pulse width for the servo (in microseconds)
#     angle_range = 120 # angle range 0 to value
#     
    # Define servo parameters MG 966R
    servo_min = 500  # Minimum pulse width for the servo (in microseconds)
    servo_max = 2500  # Maximum pulse width for the servo (in microseconds)
    angle_range = 180
    
    # Create servo driver
    serpo = ServoDriver(ch3,servo_min,servo_max,angle_range)
    serpo.set_angle(119)
    time.sleep(1)
    try:
        while True:
            if input('fire?'):
                serpo.set_angle(60)
                time.sleep(3)
                break
    except KeyboardInterrupt:
        serpo.set_angle(120)
        time.sleep(1)
    serpo.set_angle(120)
#     while True:
#         time.sleep(2)
#         serpo.set_angle(60)
#         time.sleep(2)
#         serpo.set_angle(120)
        
        
        
