import gc
import pyb
import time
import cotask
import task_share
from motor_driver import MotorDriver
from encoder_reader import Encoder
from motor_controller_4 import MotorController
from servo_driver import ServoDriver


def Aim(shares):
    my_share, my_queue = shares
    counter = 0
    while True:
        my_share.put(counter)
        counter += 1
        yield 0

def Fire(shares):
    the_share, the_queue = shares
    
    while True:
        print(f"Share1: {the_share.get()} ", end='')
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
            pass
        
        yield 0

    
def task3_fun(shares2):
    my_share2, my_queue2 = shares2
    counter = 0
#     while True:
#         my_share2.put(counter)
#         #my_queue2.put(counter)
#         counter += 1
#         yield 0

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
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    share1 = task_share.Share('h', thread_protect=False, name="Share 1")

    task1 = cotask.Task(Aim, name="Aim", priority=4, period=100,
                        profile=True, trace=False, shares=(share0, share1))
    task2 = cotask.Task(Fire, name="Fire", priority=2, period=100,
                        profile=True, trace=False, shares=(share0, share1))
    task3 = cotask.Task(task3_fun, name="Task 3", priority=1, period=200,
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

