"""!
@file main.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author Jessica Perez, Jacquelyn Banh, and Nathan Chapman
@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share

from servo_driver import ServoDriver
from motor_driver import MotorDriver
from encoder_reader import Encoder
from motor_controller_PID import MotorController
from mlx_cam import MLX_Cam

import utime
import cqueue
import math

from machine import Pin, I2C
# from mlx90640 import MLX90640
# from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
# from mlx90640.image import ChessPattern, InterleavedPattern


def Pivot(shares):
    """!
    Task which runs motor attached to tier 1 turntable. Pivots DARTICUS 180*
    Initiliazes then calls run(), setting a GO1 flag when reached
    Parameters in shares
    @param setpoint Defines the desired setpoint (Infrared Camera position)
    @param Pgain Defines the proportional gain of the controller
    """
    # Get references to the gain and setpoint which have been passed to this task
    GO1 = shares
    
    Pgain1 = 0.9
    Igain1 = 0
    Dgain1 = 0
    angle1 = 180
    timequeue1 = cqueue.FloatQueue(2)
    valqueue1 = cqueue.FloatQueue(2)
    convert1 = 226.76*3*48/(360) # N1*N2*counts per revolution
    setpoint1 = angle1*convert1
    
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
    AA = MotorController(Pgain1, Igain1, Dgain1, setpoint1, Jackie.set_duty_cycle, Jess.read, timequeue1, valqueue1)
    #print("start")
    
    #print("start")
    while True:
        AA.run()
        if setpoint1-50 <= Jess.read() <= setpoint1+50:
            GO1.put(1) #GO1 = True
            break
    Jackie.set_duty_cycle(0)
    while True: #twiddle them thumbs
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
    bullseye, GO2 = shares
    
    Pgain2 = 0.5
    Igain2 = 0
    Dgain2 = 0
    setpoint2 = 0 # This value will be updated by TRACK task
    timequeue2 = cqueue.FloatQueue(2)
    valqueue2 = cqueue.FloatQueue(2)

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
    Deitch = MotorController(Pgain2, Igain2, Dgain2, setpoint2, Tom.set_duty_cycle, Jerry.read, timequeue2, valqueue2)
    
    
    convert2 = 2750/180 # For testing with just 227 gear drive, 2750 ticks for 180 deg
    target_angle = 0
    GO2flg = False
    while True:
        Deitch.run()
        if bullseye.get()-target_angle != 0:
            target_angle = bullseye.get()
            setpoint2 = -convert2*target_angle
            print(setpoint2)
            Deitch.set_setpoint(setpoint2)
        
        if setpoint2-20 <= Jerry.read() <= setpoint2+20 and setpoint2 != 0:
            if not GO2flg:
                GO2.put(1) #GO2 = True
                GO2flg = True
                print('fire')
        else:
            if GO2flg: #if flag is on and we are out of range, reset GO2
                GO2.put(0)
                GO2flg = False
        yield
        
def Fire(shares):
    """!
    Task which runs servo when all setpoints are reached. Initializes then waits for go flags
    @param setpoint Defines the desired setpoint of the controller
    @param gain Defines the proportional gain of the controller
    """
    # Get references to the gain and setpoint which have been passed to this task
    GO1, GO2 = shares
    
    # Define pin assigments for example servo
    # setup PWM pin
    pinB0 = pyb.Pin.board.PB0
    # Timer channel 1
    TIM3 = pyb.Timer(3, freq=50) # 50hz is standard for servos
    ch3 = TIM3.channel(3,pyb.Timer.PWM, pin=pinB0)
    
    # Define servo parameters MG 966R
    servo_min = 500  # Minimum pulse width for the servo (in microseconds)
    servo_max = 2500  # Maximum pulse width for the servo (in microseconds)
    angle_range = 180
    
    # Create servo driver
    serpo = ServoDriver(ch3,servo_min,servo_max,angle_range)
    serpo.set_angle(120) # home
    yield
    serpo.set_angle(119) # retract servo slightly as first new signal fails
    yield
    while True:
        if GO1.get() and GO2.get(): # if both motors have reached setpoint within tolerance
            serpo.set_angle(60) # FIREEE
            break
    yield
    for i in range(10): # delay reset angle
        yield
    print('Target (should be) eliminated. Thank you for giving me life so I can take theirs')
    serpo.set_angle(120)
    while True:
        yield


def Track(shares):        
    """!
    Task which uses mlx_cam to track target
    Sets setpoint for Aim
    """
    bullseye = shares
    # Initialize I2C bus
    i2c_bus = I2C(1)

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33

    # Create the camera object and set it up in default mode
    camera = MLX_Cam(i2c_bus)
    camera._camera.refresh_rate = 30.0
    last_angle = 0 # init variable for filtering
    
    # Get image (raw file, nonblocking)
    while True:
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
        if abs(cam_angle - last_angle) >= 2.5: # only update if angle has changed by 2 degrees
            angle = math.degrees(math.atan((10 / 18) * math.tan(math.radians(cam_angle))))
            bullseye.put(angle) # gives angle of target to Track
            print(f'Camera angle sent from Track:{angle}')
        last_angle = cam_angle
        yield



# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    
    
    GO1 = task_share.Share('h', thread_protect=False, name="Go 1")
    GO2 = task_share.Share('h', thread_protect=False, name="Go 2")
    bullseye = task_share.Share('f', thread_protect=False, name="bullseye")
    GO1.put(1)
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    
    task1 = cotask.Task(Pivot, name="Pivot", priority=1, period=30,
                        profile=True, trace=False, shares=(GO1))
    task2 = cotask.Task(Aim, name="Aim", priority=4, period=30,
                        profile=True, trace=False, shares=(bullseye, GO2))
    task3 = cotask.Task(Fire, name="Fire", priority=2, period=400,
                        profile=True, trace=False, shares=(GO1, GO2))
    task4 = cotask.Task(Track, name="Track", priority=3, period=100,
                        profile=True, trace=False, shares=(bullseye))
   
#     cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    #print(cotask.task_list)
    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break
        
    # Print a table of task data and a table of shared information data
    #print('\n' + str (cotask.task_list))
    #print(task_share.show_all())
    #print(task1.get_trace())
    #print('')
    
