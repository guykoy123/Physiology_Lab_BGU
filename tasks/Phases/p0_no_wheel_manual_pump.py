"""
phase 0 of the experiment
mouse gets used to the enviroment
process:
1. beep to notify start of trial
2. give water every button press
3. lab worker stops experiment when needed
"""
from pyControl.utility import *
from devices import *

board = Breakout_1_2()
speaker = Audio_board(board.port_4) # Instantiate audio board.
pump = Digital_output(pin = board.BNC_2)
button = Digital_input(pin=board.port_1.DIO_B, rising_event='pump_on',debounce=100,pull="down") 

#public variables
v.beep_volume = 50 #speaker volume
v.start_beep_frequency = 2000 #start tone frequency

v.pump_wait_period = 4500 #time between giving water
v.pump_duration=75*ms #pump duration for button press


#private variables
v.finished_startup___ = False
v.pump_bool___=False

states = ['main_loop']
initial_state = 'main_loop'
events = ['speaker_off','pump_on','pump_off']

def run_start():  
    #setup the trial
    #turn on speaker and beep for start
    speaker.set_volume(v.volume)
    speaker.sine(v.frequency)
    set_timer('speaker_off',800)


def main_loop(event):
    if(event=='pump_on'): #give water and set timer for stop event
        if(not v.pump_bool___):
            pump.on()
            v.pump_bool___=True
            set_timer('pump_off',v.pump_duration) #turn off pump after set duration
    if(event=='pump_off'): #stop pump and set timer for next pump on
        pump.off()
        v.pump_bool___=False


        
def all_states(event):
    if (event=='speaker_off'):
        speaker.off()


def run_end():
    #make sure all devices are off
    speaker.off()
    pump.off()
    print_variables()