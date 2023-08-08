"""
phase 1 of the experiment
mouse learns to whisk
process:
1. beep to notify start of trial
2. wheel starts to move
3. give water periodically
4. lab worker stop experiment when needed
"""
from pyControl.utility import *
from devices import *

board = Breakout_1_2()
wheel = Digital_output(pin = board.port_1.DIO_A)
speaker = Audio_board(board.port_4) # Instantiate audio board.
pump = Digital_output(pin = board.BNC_2)


#public variables
v.volume = 50 #speaker volume
v.frequency = 2000 #start tone frequency
v.delay = 900 #delay from start of trial to start of wheel turn
v.delay_offset = 10 #percetage of offset from original value to randomize values

v.pump_duration=300*ms #pump duration for button press
v.pump_wait_period = 4500 #time between giving water

#private variables
v.finished_startup___ = False
v.pump_bool___=False

states = ['main_loop']
initial_state = 'main_loop'
events = ['speaker_off','start_walking','pump_off','pump_on']

def run_start():  
    #setup the trial
    #turn on speaker and beep for start
    speaker.set_volume(v.volume)
    speaker.sine(v.frequency)
    #randomize the duration before experiment begins
    rand_offset = randint(0,v.delay_offset)/100 + 1
    set_timer('start_walking',v.delay * rand_offset)
    set_timer('speaker_off',800)
    set_timer('pump_on',1000)


def main_loop(event):
    if(event=='pump_on'): #give water and set timer for stop event
        if(not v.pump_bool___):
            pump.on()
            v.pump_bool___=True
            set_timer('pump_off',v.pump_duration) #turn off pump after set duration
    if(event=='pump_off'): #stop pump and set timer for next pump on
        pump.off()
        v.pump_bool___=False
        set_timer('pump_on', v.pump_wait_period)
        
def all_states(event):
    if (event=='speaker_off'):
        speaker.off()

    if (event=='start_walking'):
        wheel.on()
        v.finished_startup___=True

def run_end():
    #make sure all devices are off
    speaker.off()
    pump.off()
    wheel.off()
    print_variables()