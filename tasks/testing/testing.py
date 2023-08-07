"""
phase 1 of the experiment
mouse learns to whisk
process:
1. beep to notify start of trial
2. wheel starts to move
3. lab workers checks if the mouse is whisking
4. if mouse is whisking lab worker presses the button to give water to the mouse
"""
from pyControl.utility import *
from devices import *

board = Breakout_1_2()
speaker = Audio_board(board.port_4) # Instantiate audio board.
button = Digital_input(pin=board.port_5.DIO_B, rising_event='button_press',debounce=100,pull="down") 
pump = Digital_output(pin = board.BNC_2)
wheel = Digital_output(pin = board.DAC_2)
sync_output = Rsync(pin=board.BNC_1,event_name="pulse",pulse_dur=300) #needs to be a digital input on the intan system
recording_trigger = Digital_output(pin = board.DAC_1) #needs to be a digital input on the intan system
port_exp = Port_expander(port = board.port_3)
motor1 = Stepper_motor(port = port_exp.port_1)

#public variables
v.volume = 50 #speaker volume
v.frequency = 2000 #start tone frequency
v.delay = 900 #delay from start of trial to start of wheel turn
v.delay_offset = 10 #percetage of offset from original value to randomize values
v.pump_duration=300*ms #pump duration for button press


#private variables
v.finished_startup___ = False
v.pump_bool___=False

states = ['forward','backward']
initial_state = 'forward'
events = ['speaker_off','start_walking','pump_off','button_press','pulse']

def forward(event):  
    motor1.forward(step_rate=100)
    timed_goto_state("backward",1000)
def backward(event):
    motor1.backward(step_rate=100)
    timed_goto_state("forward",1000)