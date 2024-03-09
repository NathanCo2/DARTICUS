"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
from motor_driver import MotorDriver
from encoder_reader import Encoder
from motor_controller_PID import MotorController
from mlx_cam import MLX_Cam
import utime


def Pivot(shares):
    """!
    Task which runs motor attached to tier 1 turntable. Pivots DARTICUS 180*
    Initiliazes then calls run(), setting a GO1 flag when reached
    Parameters in shares
    @param setpoint Defines the desired setpoint (Infrared Camera position)
    @param Pgain Defines the proportional gain of the controller
    """
    # Get references to the gain and setpoint which have been passed to this task
    setpoint, Pgain = shares
    
    # Initialize motor drivers and encoders
    # set up timer 8 for encoder 2
    TIM8 = pyb.Timer(8, prescaler=1, period=0xFFFF) # Timer 8, no prescalar, frequency 100kHz
    #Define pin assignments for encoder 2
    pinc6 = pyb.Pin(pyb.Pin.board.PC6)
    pinc7 = pyb.Pin(pyb.Pin.board.PC7)
    # Create encoder object
    Jerry = Encoder(pinc6, pinc7, TIM8)
    
    # setup motor
    TIM5 = pyb.Timer(5, freq=2000) # Timer 5, frequency 2000Hz
    # Define pin assignments for motor 2
    pinc1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    pina0= pyb.Pin(pyb.Pin.board.PA0)
    pina1 = pyb.Pin(pyb.Pin.board.PA1)    
    # Create motor driver
    Tom = MotorDriver(pinc1, pina0, pina1, TIM5)
    Jerry.zero()
    # Create motor controller
    Deitch = MotorController(gain, setpoint, Tom.set_duty_cycle, Jerry.read)
    #print("start")
    while True:
        Deitch.run()
        if setpoint-100 <= Jerry.read() <= setpoint+100:
            GO1 = True
            break
    Tom.set_duty_cycle(0)
    yield
    
def Aim(shares):
    """!
    Task which runs motor attached to tier 2 turntable to aim blaster at high resolution
    Initializes then calls run(), setting a GO2 flag when reached
    Parameters in shares
    @param setpoint Defines the desired setpoint (Infrared Camera position)
    @param Pgain Defines the proportional gain of the controller
    @param Igain Defines the integral gain of the controller
    @param Dgain Defines the derivative gain of the controller
    """
    # Get references to the gain and setpoint which have been passed to this task
    Pgain, Igain, Dgain, setpoint = shares
    
    # Initialize motor drivers and encoders
    # Set up timer 4 for encoder 1
    TIM4 = pyb.Timer(4, prescaler=1, period=0xFFFF) # Timer 4, no prescalar, frequency 100kHz
    # Define pin assignments for encoder 1
    pinb6 = pyb.Pin(pyb.Pin.board.PB6)
    pinb7 = pyb.Pin(pyb.Pin.board.PB7)
    # Create encoder object
    Jess = Encoder(pinb6, pinb7, TIM4)
    
    # setup motor
    TIM3 = pyb.Timer(3, freq=2000) # Timer 3, frequency 2000Hz
    # Define pin assignments for motor 1
    pina10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    pinb4 = pyb.Pin(pyb.Pin.board.PB4)
    pinb5 = pyb.Pin(pyb.Pin.board.PB5)
    # Create motor driver
    Jackie = MotorDriver(pina10, pinb4, pinb5, TIM3)
    Jess.zero()
    # Create motor controller
    AA = MotorController(Pgain, Igain, Dgain, setpoint, Jackie.set_duty_cycle, Jess.read)
    #print("start")
    
    # one full rotation is 32653.44 for top tier
    convert = 32653.44/360 #converts angle deg to encoder ticks
    while True:
        AA.set_setpoint(convert*setpoint)
        AA.run()
        if setpoint-100 <= Jess.read() <= setpoint+100:
            GO2 = True
        else:
            GO2 = False
        yield
        
def Fire(shares):
    """!
    Task which runs servo when all setpoints are reached. Initializes then waits for go flags
    @param setpoint Defines the desired setpoint of the controller
    @param gain Defines the proportional gain of the controller
    """
    # Get references to the gain and setpoint which have been passed to this task
    #gain, setpoint, time, val = shares
     
    # Initialize servo
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    # Timer channel 1
    TIM1 = pyb.Timer(1, freq=50)
    ch3 = TIM1.channel(3, pyb.Timer.PWM, pin=pinA10)
    
    ch3.pulse_width_percent(.75)
    time.sleep(2)
    ch3.pulse_width_percent(5)
    time.sleep(2)
    ch3.pulse_width_percent(8.75)
    time.sleep(3)
    
    yield


def Track(shares):
    """!
    Task which uses mlx_cam to track target
    Sets setpoint for Aim
    """
    # Initialize I2C bus
    i2c_bus = I2C(1)

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33

    # Create the camera object and set it up in default mode
    camera = MLX_Cam(i2c_bus)
    camera._camera.refresh_rate = 10.0

    # Get image (raw file, nonblocking)
    while True:
        try:
            # Get and image and see how long it takes to grab that image
            # print("Click.", end='')
            # Keep trying to get an image; this could be done in a task, with
            # the task yielding repeatedly until an image is available
            image = None
            while not image:
                image = camera.get_image_nonblocking()
                yield
            # Full image grabbed, yield image
            cam_angle = camera.get_angle(image, limits=(0, 99))
            # will need to translate origin from camera to gun
            angle = cam_angle
            setpoint = angle # need to get this setpoint to AIM task
            yield


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    
    # Initialize values
    
    Pgain1 = 0.1
    Igain1 = 0
    Dgain1 = 0
    angle1 = 180
    setpoint1 = angle1*convert1
    
    Pgain2 = 0.1
    Igain2 = 0
    Dgain2 = 0
    setpoint2 = 0 # This value will be updated by TRACK task
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    task1 = cotask.Task(Pivot, name="Pivot", priority=1, period=100,
                        profile=True, trace=False, shares=(Pgain1, Igain1, Dgain1, setpoint1))
    task2 = cotask.Task(Aim, name="Aim", priority=2, period=100,
                        profile=True, trace=False, shares=(Pgain2, Igain2, Dgain2, setpoint2))
    task3 = cotask.Task(Fire, name="Fire", priority=3, period=100,
                        profile=True, trace=False, shares=(0))
    task4 = cotask.Task(Sight, name="Sight", priority=4, period=100,
                        profile=True, trace=False,)
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break
    