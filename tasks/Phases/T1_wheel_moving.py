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
v.amount_of_trials=-1 #amount of trials to run for this task, if -1 run until manually stopped
v.beep_volume = 50 #speaker volume
v.start_beep_frequency = 2000 #start tone frequency
v.delay_to_start_wheel = 300 #delay from start of trial to start of wheel turn
v.wheel_delay_offset = 10 #percentage of offset from original value to randomize values

v.pump_duration=75*ms #pump duration for button press
v.time_of_wheel_spinning=2000 #time after giving water before the wheel stops moving
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
        print("trial #"+str(v.trial_counter___))
        #setup the trial
        #turn on speaker and beep for start
        speaker.set_volume(v.beep_volume)
        speaker.sine(v.start_beep_frequency)
        #randomize the duration before experiment begins
        rand_offset = randint(0,v.wheel_delay_offset)/100 + 1
        set_timer('start_walking',v.delay_to_start_wheel * rand_offset)
        
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
        
        
def all_states(event):
    if (event=='speaker_off'):
        speaker.off()

    if (event=='start_walking'):
        wheel.on()
        v.finished_startup___=True
        set_timer('pump_on',1000)
        set_timer('end_trial',v.time_of_wheel_spinning)
    if (event=='end_trial'):
        #make sure all devices are off
        speaker.off()
        pump.off()
        wheel.off()
        print_variables()
        v.trial_counter___+=1
        v.finished_startup___=False

        #if amount of trials is reached, end task
        #if amount of trials set to -1, will never stop automatically
        if v.trial_counter___!=v.amount_of_trials:
            set_timer('start_trial_event',v.time_between_trials)
            goto_state('start_trial')
        else:
            stop_framework()
    if (event=='end_experiment'):
        stop_framework()
