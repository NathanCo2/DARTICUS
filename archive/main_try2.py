import gc
import pyb
import time
import cqueue
import cotask
import task_share
from motor_driver import MotorDriver
from encoder_reader import Encoder
from motor_controller_4 import MotorController
from servo_driver import ServoDriver


def Aim(shares, shares2):
    my_share, my_queue = shares
    pivot_done, setpoint = shares2
    
    check = pivot_done.get()
    if check == 1:
        counter = 0
        while True:
            counter += 1
            my_share.put(counter)
            yield 

def Fire(shares):
    the_share, the_queue = shares
    
    while True:
        print(f"Share1: {the_share.get()} ")
        value = the_share.get()
        if value == 1:
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

            time.sleep(2)
            serpo.set_angle(60)
            time.sleep(2)
            serpo.set_angle(120)
            time.sleep(2)
            serpo.set_angle(60)
            time.sleep(2)
            serpo.set_angle(120)
            time.sleep(2)
            
        else:
            yield
        
    
def Pivot(shares2):
    pivot_done, setpoint = shares2
    
    if wait == True:
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
        Deitch = MotorController(gain, setpoint, Tom.set_duty_cycle, Jerry.read, time1, val1)
        for i in range(200):
            Deitch.run()
            yield
        print("done 1")
        Tom.set_duty_cycle(0)
        
        # once done set flag and wait
        # Initialize Values
        counter = 0
        while True:
            counter += 1
            pivot_done.put(counter)
            yield
    else:
        yield

def task4_fun(shares2):
    the_share2, the_queue2 = shares2
    counter = 0

#     while True:
#         print(f"Share2: {the_share2.get()}", end='')
#         #while not the_queue2.empty():
#         #    print(f"{the_queue2.get()} ", end='')
#         print('')
#         yield 0

if __name__ == "__main__":
    #Initalize values:
    waiting = True
    
    # Create variables to pass to tasks. queues are for printing data, gain and setpoint are input
    time1 = cqueue.FloatQueue(200)
    val1 = cqueue.FloatQueue(200)
    
    print("FIRING DARTICUS!!! \n"
          "Press Ctrl-C to stop and show diagnostics.")

    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    share1 = task_share.Share('h', thread_protect=False, name="Share 1")

    task1 = cotask.Task(Aim, name="Aim", priority=1, period=100,
                        profile=True, trace=False, shares=(share0, share1, Q0))
    task2 = cotask.Task(Fire, name="Fire", priority=2, period=100,
                        profile=True, trace=False, shares=(share0, share1))
    task3 = cotask.Task(Pivot, name="Pivot", priority=4, period=200,
                        profile=True, trace=False, shares=(share1, share0))
    task4 = cotask.Task(task4_fun, name="Task 4", priority=3, period=200,
                        profile=True, trace=False, shares=(share1, share0))

    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)

    gc.collect()

    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    print('\n' + str(cotask.task_list))
    print(task_share.show_all())

