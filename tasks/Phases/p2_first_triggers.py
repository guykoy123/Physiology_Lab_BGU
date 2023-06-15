"""
phase 2: mouse learns to react to triggers
(divided into two parts 2.1 and 2.2)
process:
    1. start brain recording
    2. plat start beep
    3. start wheel after randomized time
    4. move trigger into whisking position after random time
    5. move trigger out of whisking position
    6. mouse receives water if responded to trigger
        6.1 in part 2.1 recieve water right after lick
        6.2 in part 2.2 recieve water only after trigger
    7. stop recording
"""

from pyControl.utility import *
from hardware_definitions.p2_def import *



#public variables
v.volume = 50 #speaker volume
v.frequency = 2000 #start tone frequency
v.delay = 900 #delay from start of trial to start of wheel turn
v.delay_offset = 10 #percetage of offset from original value to randomize values
v.pump_duration=300*ms #pump duration for button press


#private variables
v.finished_startup___ = False
v.pump_bool___=False

states = ['startup','main_loop']
initial_state = 'startup'
events = ['speaker_off','start_walking','pump_off','pulse']

def startup(event):  
    if (event=='start_walking'):
        wheel.on()
        v.finished_startup___=True
        goto_state('main_loop')

    else:
        if(not v.finished_startup___):
            
            #setup the trial
            #turn on speaker and beep for start
            speaker.set_volume(v.volume)
            speaker.sine(v.frequency)
            #randomize the duration before experiment begins
            rand_offset = randint(0,v.delay_offset)/100 + 1
            set_timer('start_walking',v.delay * rand_offset)
            set_timer('speaker_off',800)
            


def main_loop(event):
    if(event=='button_press'): #on event of button press and the pump is not active give water
        if(not v.pump_bool___):
            pump.on()
            v.pump_bool___=True
            set_timer('pump_off',v.pump_duration) #turn off pump after set duration
    if(event=='pump_off'):
        pump.off()
        v.pump_bool___=False

        
def all_states(event):
    if (event=='speaker_off'):
        speaker.off()

def run_end():
    #make sure all devices are off
    speaker.off()
    pump.off()
    wheel.off()
    print_variables()