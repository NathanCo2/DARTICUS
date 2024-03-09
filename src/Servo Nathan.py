import pyb
import time

# Initializing pin A10
pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)

# Timer channel 1
TIM1 = pyb.Timer(1, freq=50)
ch3 = TIM1.channel(3, pyb.Timer.PWM, pin=pinA10)

# Function to set duty cycle (0 to 100)
def set_duty_cycle(duty_cycle):
    ch3.pulse_width(duty_cycle)

# Define servo parameters 1501 MG
# servo_min = 800  # Minimum pulse width for the servo (in microseconds)
# servo_max = 2200  # Maximum pulse width for the servo (in microseconds)

# Define servo parameters MG 966R
servo_min = 1000  # Minimum pulse width for the servo (in microseconds)
servo_max = 2000  # Maximum pulse width for the servo (in microseconds)

def set_angle(angle):
    # Convert the angle to pulse width
    pulse_width = int((angle / 180) * (servo_max - servo_min) + servo_min)
    print(pulse_width)
    # Set the pulse width
    set_duty_cycle(pulse_width) # duty in ms

if __name__ == "__main__":
    
    while True:     
        # Move the servo to 0 degrees
        set_angle(0)
        time.sleep(2)  # Wait for 1 second
        # Move the servo to 90 degrees
        set_angle(180)
        time.sleep(2)  # Wait for 1 second
        # Move the servo to 180 degrees
        set_angle(0)
        time.sleep(2)  # Wait for 1 second

# duty cycle of 5 is 0 degrees
