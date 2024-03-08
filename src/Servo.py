import pyb
import time

# Initializing pin A10
pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)

# Timer channel 1
TIM1 = pyb.Timer(1, freq=50)
ch3 = TIM1.channel(3, pyb.Timer.PWM, pin=pinA10)

# Function to set duty cycle (0 to 100)
def set_duty_cycle(duty_cycle):
    ch3.pulse_width_percent(duty_cycle)

if __name__ == "__main__":
    while True:     
        set_duty_cycle(.75) 
        time.sleep(2)
        print('1')
        set_duty_cycle(5)  
        time.sleep(2)
        print('2')
        set_duty_cycle(8.75) 
        time.sleep(2)
        print('3')
        set_duty_cycle(5)  
        time.sleep(3) 

# duty cycle of 5 is 0 degrees