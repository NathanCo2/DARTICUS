"""!
@file encoder_reader.py

This program demonstrates the development of a class called Encoder to measure
the movement of a motor using an optical encoder. This code was tested an ran
with the Motor Driver class developed in Lab 1 to examine if the code was running
correctly. 

@author Jessica Perez, Jacquelyn Banh, and Nathan Chapman
@date   2024-02-06 Original program, based on example from above listed source
@copyright (c) 2024 by Jessica Perez, Jacquelyn Banh, and Nathan Chapman and released under the GNU Public Licenes V3
"""

import pyb
import time
from motor_driver import MotorDriver

class Encoder:
    """! 
    This class implements a Encoder for an ME405 kit. 
    """

    def __init__ (self, ch1pin, ch2pin, timer):
        """! 
        Creates an encoder object that can be used to measure
        the position of a motor
        @param ch1pin: Pin for reading encoder channel 1
        @param ch2pin: Pin for reading encoder channel 2
        @param timer: Timer object for reading encoder
        """
        #print ("Creating an encoder reader")
        self.timer = timer
        self.en1 = timer.channel(1, pyb.Timer.ENC_AB, pin=ch1pin) #sets up ch 1 for encoder counting mode on ch1pin
        self.en2 = timer.channel(2, pyb.Timer.ENC_AB, pin=ch2pin) #sets up ch 2 for encoder counting mode on ch2pin
        self.timer.counter(0)
        self.previous = self.timer.counter()
        self.deltatot = 0
        self.AR = int(0xFFFF + 1) # calculates half the auto reload value for 16 bit number
        
    def read(self):
        """!
        This method returns the current position of the
        motor using the encoder
        """
        #print("Counter = ", self.timer.counter());
        #Accounts from overflow and underflow
        self.current = self.timer.counter()# stores current time value
        self.delta = self.current - self.previous # calculates the delta based on current time and previous time
        #print(f"delta {self.delta}")
        #print("Delta = ", self.delta);# print the delta
        if self.delta > self.AR/2: # check underflow (if delta is greater then auto reload value)
            self.delta -= self.AR # offset to correct underflow (if so, then will offset by subtracting AR from delta)
        elif self.delta < -self.AR/2: # check overflow (if delta is less then auto reload value)
            self.delta += self.AR # offset to correct overflow (if so, then will offset by add AR from delta)
        self.deltatot += self.delta# summing all delta from previous calculates (to determine position overtime)
        #print("Delta = ", self.delta);# prints the delta
        #print("Delta Total = ", self.deltatot);# prints total delta
        self.previous = self.current # stores previous time into current for next read
        #print(self.timer.counter())
        #return self.timer.counter()
        return self.deltatot
    
    def zero(self):
        """!
        This method sets the encoder count to zero at the
        current position of the motor
        """
        self.timer.counter(0)
        #print ("Encoder count reset to zero")

# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program           
if __name__ == "__main__":    # set up timer 4 for encoder 1
    TIM4 = pyb.Timer(4, prescaler=1, period=0xFFFF) # Timer 4, no prescalar, frequency 100kHz
    # set up timer 8 for encoder 2
    TIM8 = pyb.Timer(8, prescaler=1, period=0xFFFF) # Timer 8, no prescalar, frequency 100kHz
    # Define pin assignments for encoder 1
    pinb6 = pyb.Pin(pyb.Pin.board.PB6)
    pinb7 = pyb.Pin(pyb.Pin.board.PB7)
    #Define pin assignments for encoder 2
    pinc6 = pyb.Pin(pyb.Pin.board.PC6)
    pinc7 = pyb.Pin(pyb.Pin.board.PC7)
    # Create first encoder object
    Tom = Encoder(pinb6, pinb7, TIM4)
    Jerry = Encoder(pinc6, pinc7, TIM8)

    # setup motor
    TIM3 = pyb.Timer(3, freq=2000) # Timer 3, frequency 2000Hz
    # Define pin assignments for motor 1
    pina10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    pinb4= pyb.Pin(pyb.Pin.board.PB4)
    pinb5 = pyb.Pin(pyb.Pin.board.PB5)

    # Create motor drivers
    moe = MotorDriver(pina10, pinb4, pinb5, TIM3)
    while True:
        moe.set_duty_cycle (-50)#Reverse at 50% duty cycle
        #read encoder 20times for 20 seconds
        time.sleep(0.01)
        Jerry.read()
    #change to different duty cycle
        #moe.set_duty_cycle (50)
        #read encoder 20 times for 20 sec
        #time.sleep(0.01)
        #Tom.read()
