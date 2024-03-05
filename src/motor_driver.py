"""!
@file motor_driver.py
Run real or simulated dynamic response tests and plot the results. This program
demonstrates a way to make a simple GUI with a plot in it. It uses Tkinter, an
old-fashioned and ugly but useful GUI library which is included in Python by
default.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Jessica Perez, Jacquelyn Banh, and Nathan Chapman
@date   2024-01-30 Original program, based on example from above listed source
@copyright (c) 2024 by Jessica Perez, Jacquelyn Banh, and Nathan Chapman and released under the GNU Public Licenes V3
"""

import pyb
import time

class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin: Pin for enabling the motor driver
        @param in1pin: Pin for controlling direction 1
        @param in2pin: Pin for controlling direction 2
        @param timer: Timer object for generating PWM signals
        """
        #print ("Creating a motor driver")
        self.en_pin = en_pin
        self.timer = timer
        self.ch1 = timer.channel(1, pyb.Timer.PWM, pin=in1pin) #sets up ch 1 for PWM mode on in1pin
        self.ch2 = timer.channel(2, pyb.Timer.PWM, pin=in2pin) #sets up ch 2 for PWM mode on in2pin
        self.en_pin.low()
        

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        #print (f"Setting duty cycle to {level}")
        self.en_pin.high() #enable motors
        if level > 0:
            # Moves the motor forward
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(level)
        elif level < 0:
            # Moves the motor reverse
            self.ch1.pulse_width_percent(-level)
            self.ch2.pulse_width_percent(0)
        else:
            #Braking/Stops the motor
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0)
        
 
# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program       
if __name__ == "__main__":
    # set up timer 3 and 5
    TIM3 = pyb.Timer(3, freq=2000) # Timer 3, frequency 2000Hz
    TIM5 = pyb.Timer(5, freq=2000) # Timer 5, frequency 2000Hz
    # Define pin assignments for motor 1
    ENA = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    IN1A = pyb.Pin(pyb.Pin.board.PB4)
    IN2A = pyb.Pin(pyb.Pin.board.PB5)
    # Define pin assignments for motor 2
    ENB = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    IN1B = pyb.Pin(pyb.Pin.board.PA0)
    IN2B = pyb.Pin(pyb.Pin.board.PA1)

    # Create motor drivers
    eenie = MotorDriver(ENA, IN1A, IN2A, TIM3)
    moe = MotorDriver(ENB, IN1B, IN2B, TIM5)
    while True:
        moe.set_duty_cycle (50)				#Forward at 50% duty cycle
        eenie.set_duty_cycle (-50)	
        time.sleep(2)						#Sleeps for 2 seconds
        moe.set_duty_cycle (-50)			#Reverse at 50% duty cycle
        eenie.set_duty_cycle (50)	
        time.sleep(2)						#Sleeps for 2 seconds
        moe.set_duty_cycle (0)				#Stops the duty cycle
        eenie.set_duty_cycle (0)	
        time.sleep(2)						#Sleeps for 2 seconds
        
   