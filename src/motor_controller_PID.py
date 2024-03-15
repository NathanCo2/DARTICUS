"""!
@file motor_controller.py

This program develops a Motor Controller class that performs closed loop PID control.
This requires the Motor Driver and Encoder class
This program demonstrates the development of a class called MotorController to that
perform closed-loop proportional control. This code was tested an ranwith the Motor
Driver class and Encoder class developed in the previous labs to examine if the code
was running correctly. 

@author Jessica Perez, Jacquelyn Banh, and Nathan Chapman
@date   2024-03-5
"""

import pyb
import utime
import cqueue

class MotorController:
    """! 
    This class implements the Motor Controller for an ME405 kit. 
    """

    def __init__ (self, Pgain, Igain, Dgain, setpoint, setdutycycle_f, getactual_f, timequeue, valqueue):
        """! 
        Creates an encoder object that can be used to measure
        the position of a motor
        @param Pgain = Kp, percent duty cycle/encoder count
        @param Igain = Ki
        @param Dgain = Kd
        @param setpoint = desired angle of motor
        @param setdutycycle_f = function to set duty cycle output
        @param getactual_f = function to read actual value
        @param timequeue = queue to put time values for graphing
        @param valqueue = queue to put position values for graphing
        """
        self.setpoint = setpoint
        self.Pgain = Pgain
        self.Igain = Igain
        self.Dgain = Dgain
        self.actual = 0
        self.err = 0
        self.setdutycycle = setdutycycle_f
        self.getactual = getactual_f
        self.timequeue = timequeue # queue for time
        self.valqueue = valqueue # queue for values
        self.esum = 0 #error sum to be used for I control
        self.lasterr = 0 # error
        self.newt = 0
        self.oldt = 0
        
    def run(self):
        """!
        This method will run one pass of the control algorithm
        """
        self.newt = utime.ticks_ms()
        self.dt = utime.ticks_diff(self.newt, self.oldt)/1000
#         print(f'time difference {self.dt}')
        #self.dt = 30/1000
        self.actual = self.getactual() # call read encoder function and get delta total
#         print(f'actual encoder position {self.actual}')
        self.err = self.setpoint - self.actual
        #print(f'err {self.err}')
        self.esum += self.err
        self.diff = self.err - self.lasterr
        self.PWM = self.err*self.Pgain + self.esum*self.dt*self.Igain + self.diff*self.Dgain/self.dt
        # self.PWM = max(min(self.PWM, 100), -100) #This line of code suckss
        #print(f'PWM {self.PWM}')
        self.setdutycycle(self.PWM)
        self.lasterr = self.err
        self.timequeue.put(utime.ticks_ms()) # puts time in queue
        self.valqueue.put(self.actual) # puts PWM in queue
        self.oldt = self.newt
        
        
    def set_setpoint(self,setpoint):
        """!
        This method sets up the setpoint for proportional control
        @param setpoint = desired angle of motor
        """
        self.setpoint = setpoint
        
    def set_Kp(self,Pgain):
        """!
        This method sets up the gain for proportional control
        @param gain = Kp, percent duty cycle/encoder count
        """
        self.Pgain = Pgain
        
    def set_Ki(self, Igain):
        """!
        This method sets up the gain for Integral control
        @param gain = Ki
        """
        self.Igain = Igain    
        
    def controller_response(self):
        """!
        This method will print the results obtained of the step
        response and print when the step response is done running
        """  
        self.time = []
        self.val = []
        while self.timequeue.any():#Checks if anything is the Queue and emptying it
            self.time.append(self.timequeue.get()) #Gets single value from queue
            self.val.append(self.valqueue.get())
        self.firsttime = self.time[0]
        self.time_offset = [t - self.firsttime for t in self.time]
        for i in range(len(self.time_offset)):
            print(f"{self.time_offset[i]}, {self.val[i]}")

# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program           
if __name__ == "__main__":

    from motor_driver import MotorDriver
    from encoder_reader import Encoder
    
    # Initialize motor drivers and encoders
    length = 200
    time1 = cqueue.FloatQueue(length)
    val1 = cqueue.FloatQueue(length)
    time2 = cqueue.FloatQueue(length)
    val2 = cqueue.FloatQueue(length)
    
    # one full rotation is 32653.44 for top tier
    angle1 = -180
    convert1 = 47.2
    setpoint1 = 0 #12500
    KP1 = 0.9
    KI1 = 0
    KD1 = 0
    
    angle2 = -20
    convert2 = 4100/90 # test code for 227 gearbox with only small inertia
    setpoint2 = 0 #convert2*angle2
    KP2 = 0.3
    KI2 = 0.001
    KD2 = 0.001
    
    # Set up timer 4 for encoder 1
    TIM4 = pyb.Timer(4, prescaler=1, period=0xFFFF) # Timer 4, no prescalar, frequency 100kHz
    # Define pin assignments for encoder 1
    pinb6 = pyb.Pin(pyb.Pin.board.PB6)
    pinb7 = pyb.Pin(pyb.Pin.board.PB7)
    # Create encoder object
    Encoder1 = Encoder(pinb6, pinb7, TIM4)
    Encoder1.zero()
    # setup motor
    TIM3 = pyb.Timer(3, freq=2000) # Timer 3, frequency 2000Hz
    # Define pin assignments for motor 1
    pina10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    pinb4 = pyb.Pin(pyb.Pin.board.PB4)
    pinb5 = pyb.Pin(pyb.Pin.board.PB5)
    # Create motor driver
    Motor1 = MotorDriver(pina10, pinb4, pinb5, TIM3)
    # Create motor controller 1
    Control1 = MotorController(KP1, KI1, KD1, setpoint1, Motor1.set_duty_cycle, Encoder1.read, time1, val1)
    
    # set up timer 8 for encoder 2
    TIM8 = pyb.Timer(8, prescaler=1, period=0xFFFF) # Timer 8, no prescalar, frequency 100kHz
    #Define pin assignments for encoder 2
    pinc6 = pyb.Pin(pyb.Pin.board.PC6)
    pinc7 = pyb.Pin(pyb.Pin.board.PC7)
    # Create encoder object
    Encoder2 = Encoder(pinc6, pinc7, TIM8)
    Encoder2.zero()
    # setup motor 2
    TIM5 = pyb.Timer(5, freq=2000) # Timer 5, frequency 2000Hz
    # Define pin assignments for motor 2
    pinc1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    pina0 = pyb.Pin(pyb.Pin.board.PA0)
    pina1 = pyb.Pin(pyb.Pin.board.PA1)    
    # Create motor driver 2
    Motor2 = MotorDriver(pinc1, pina0, pina1, TIM5)
    # create motor controller 2
    Control2 = MotorController(KP2, KI2, KD2, setpoint2, Motor2.set_duty_cycle, Encoder2.read, time2, val2)
    while True:
        try:
            
            angle2 = float(input('Angle: '))
            setpoint2 = convert2*angle2
#             Control2.controller_response()
#             setpoint2 = float(input('Setpoint2: '))
            Control2.set_setpoint(setpoint2)
            for i in range(length):
#                 Control1.run()
                Control2.run()
                utime.sleep_ms(20)
#             break
        except KeyboardInterrupt:
            break
        
    print("Control 1 response")
    print(f"KP: {KP1}, KI: {KI1}, KD: {KD1}")
#     Control1.controller_response()
    print(f'setpoint1: {setpoint1}')
    
    print("Control 2 response")
    print(f"KP: {KP2}, KI: {KI2}, KD: {KD2}")
    Control2.controller_response()
    Motor1.set_duty_cycle(0)
    Motor2.set_duty_cycle(0)
    print("done")
