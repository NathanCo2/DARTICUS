import pyb
import time

# Initializing pin A0
pinA1 = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)

# Timer channel 2
TIM2 = pyb.Timer(2, freq=50)
ch2 = TIM2.channel(2, pyb.Timer.PWM, pin=pinA1)

# Function to set duty cycle (0 to 100)
def set_duty_cycle(duty_cycle):
    ch2.pulse_width_percent(duty_cycle)

if __name__ == "__main__":
    while True:
        set_duty_cycle(1)  
        time.sleep(.5)      
        set_duty_cycle(6) 
        time.sleep(.5)      	

