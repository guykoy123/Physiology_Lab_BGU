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
v.time_to_stop_wheel=500 #time after giving water before the wheel stops moving
v.time_between_trials=5000 
# v.pump_wait_period = 4500 #time between giving water

#private variables
v.finished_startup___ = False
v.pump_bool___=False
v.trial_counter___=0
states = ['start_trial','main_loop']
initial_state = 'start_trial'
events = ['speaker_off','start_walking','pump_off','pump_on','start_trial_event','end_trial','end_experiment']

def start_trial(event):  
    if(not v.finished_startup___ and (event=='start_trial_event' or v.trial_counter___==0)):
        print("starting trial #"+str(v.trial_counter___))
        #setup the trial
        #turn on speaker and beep for start
        speaker.set_volume(v.volume)
        speaker.sine(v.frequency)
        #randomize the duration before experiment begins
        rand_offset = randint(0,v.delay_offset)/100 + 1
        set_timer('start_walking',v.delay * rand_offset)
        set_timer('speaker_off',800)
        v.finished_startup___=True
        goto_state('main_loop')



def main_loop(event):
    if(event=='pump_on'): #give water and set timer for stop event
        if(not v.pump_bool___):
            pump.on()
            v.pump_bool___=True
            set_timer('pump_off',v.pump_duration) #turn off pump after set duration
    if(event=='pump_off'): #stop pump and set timer for next pump on
        pump.off()
        v.pump_bool___=False
        set_timer('end_trial',v.time_to_stop_wheel)
        
def all_states(event):
    if (event=='speaker_off'):
        speaker.off()

    if (event=='start_walking'):
        wheel.on()
        v.finished_startup___=True
        set_timer('pump_on',1000)
    if (event=='end_trial'):
        #make sure all devices are off
        speaker.off()
        pump.off()
        wheel.off()
        print_variables()
        v.trial_counter___+=1
        v.finished_startup___=False
        set_timer('start_trial_event',v.time_between_trials)
        goto_state('start_trial')
    if (event=='end_experiment'):
        stop_framework()
