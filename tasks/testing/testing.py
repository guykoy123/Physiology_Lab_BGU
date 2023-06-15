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
wheel = Digital_output(pin = board.BNC_1)
sync_output = Rsync(pin=board.DAC_2, mean_IPI=1000,event_name="pulse") #needs to be a digital input on the intan system
recording_trigger = Digital_output(pin = board.DAC_1) #needs to be a digital input on the intan system


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
events = ['speaker_off','start_walking','pump_off','button_press','pulse']

def startup(event):  
    if (event=='start_walking'):
        wheel.on()
        v.finished_startup___=True
        goto_state('main_loop')

    else:
        if(not v.finished_startup___):
            #setup the trial
            recording_trigger.on()
            print("triggered recording")
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
    if(not v.finished_startup___):
        #setup the trial
        recording_trigger.on()
        print("triggered recording")

def run_end():
    #make sure all devices are off
    speaker.off()
    pump.off()
    wheel.off()
    recording_trigger.off()
    print("stopped recording")
    print_variables()