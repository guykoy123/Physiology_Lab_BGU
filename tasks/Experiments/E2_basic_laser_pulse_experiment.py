"""
basic paradigm to test the effect of the laser pulses on the brain of the mouse.

1. start brain recording
2. play trial start beep
3. wait some time
4. pulse laser based on preset variables (by sending a digital high to turn on)
5. give water
6. wait some time and go back to stage 2



laser variables:

- number of pulses
- pulse duration
- inter pulse interval
"""

from devices import *
from pyControl.utility import *

board = Breakout_1_2()
port_exp = Port_expander(port = board.port_3)
laser=Digital_output(pin = port_exp.port_2.DIO_B)
speaker = Audio_board(board.port_4) # Instantiate audio board.
pump = Digital_output(pin = board.BNC_2)

sync_output = Rsync(pin=board.BNC_1,mean_IPI=1500,event_name="pulse") #needs to be a digital input on the intan system
recording_trigger = Digital_output(pin = port_exp.port_2.DIO_A) #needs to be a digital input on the intan system

#public variables
v.number_of_trials=-1 #amount of trials to run for this task, if -1 run until manually stopped
v.beep_volume = 50 #speaker volume
v.start_beep_frequency = 2000 #start tone start_frequency
v.pump_duration=75*ms #pump duration for button press
v.delay_to_start_pulses=300 #delay from start of trial until laser pulses start
v.time_between_trials=5000 

v.number_of_pulses=1
v.pulse_duration=1 #in milliseconds
v.inter_pulse_interval=1 #time between consecutive pulses


#private variables
v.finished_startup___ = False
v.pump_bool___=False #pump on/off
v.trial_counter___=0
v.pulse_counter___=0
states = ['start_trial','main_loop']
initial_state = 'start_trial'
events = ['speaker_off','pump_off','pump_on','pulse','laser_on','laser_off',
          'start_trial_event','end_trial','end_experiment']


def run_start():  
    recording_trigger.on()
    #TODO: add laser variables validation


def start_trial(event):  
    if(not v.finished_startup___ and event=='start_trial_event'): #first trial will only start if worker has triggered the event manually, meaning the camera is recording
        print("trial #"+str(v.trial_counter___))
        #setup the trial
        #turn on speaker and beep for start
        speaker.set_volume(v.beep_volume)
        speaker.sine(v.start_beep_frequency)

        set_timer('speaker_off',800)
        v.finished_startup___=True
        set_timer('laser_on',v.delay_to_start_pulses)
        goto_state('main_loop')
        

def main_loop(event):
    #cycle through laser pulses using events and timers
    if(event=='laser_on'):
        if v.pulse_counter___<v.number_of_pulses: #pulse laser
            laser.on()
            set_timer('laser_off',v.pulse_duration)
            v.pulse_counter___+=1
        else:#finished pulsing, reset counter and give water
            v.pulse_counter___=0
            publish_event('pump_on')
    if event=='laser_off':
        laser.off()
        set_timer('laser_on',v.inter_pulse_interval)
    if(event=='pump_on'): #give water and set timer for stop event
        if(not v.pump_bool___):
            pump.on()
            v.pump_bool___=True
            set_timer('pump_off',v.pump_duration) #turn off pump after set duration
    if(event=='pump_off'): #stop pump and set timer for next pump on
        pump.off()
        v.pump_bool___=False
        publish_event('end_trial')
        goto_state('start_trial')

def all_states(event):
    if (event=='speaker_off'):
        speaker.off()

    if (event=='end_trial'):
        #make sure all devices are off
        speaker.off()
        pump.off()
        laser.off()

        # print_variables()
        v.trial_counter___+=1

        #reset flags
        v.finished_startup___=False

        #if amount of trials is reached, end task
        #if amount of trials set to -1, will never stop automatically
        if v.trial_counter___!=v.number_of_trials:
            set_timer('start_trial_event',v.time_between_trials)
            goto_state('start_trial')
        else:
            stop_framework()


def run_end():
    #make sure all devices are off
    recording_trigger.off()
    speaker.off()
    pump.off()
    laser.off()
    print_variables()