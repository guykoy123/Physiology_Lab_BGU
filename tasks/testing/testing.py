from pyControl.utility import *
from devices import *
#import hardware_definitions.test_def as hw

board = Breakout_1_2()
speaker = Audio_board(board.port_4) # Instantiate audio board.
lickometer = Lickometer(port=board.port_2,debounce=100) # Instantiate lickometer.
    #ground needs to connect to conducting floor, LCK1 connects to water nossle
    #make sure in final setup there is not interference that trigger fake positives

pump = Digital_output(pin = board.BNC_2)
blue_LED = Digital_output('B4')


v.volume = 50
v.frequency = 2000
v.delay = 1000
v.finished_startup___ = False


states = ['startup','main_loop']
initial_state = 'startup'
events =['start_walking','lick_1','lick_1_off']

def run_start():
    print_variables()

def startup(event):  
    if (event=='start_walking'):
        speaker.off()
        print("starting walking motor")
        v.finished_startup___=True
        goto_state('main_loop')
    else:
        if(not v.finished_startup___):
            speaker.set_volume(v.volume)
            speaker.sine(v.frequency)
            set_timer('start_walking',v.delay)



def main_loop(event):
    if(event == 'lick_1'):
        blue_LED.on()
        print("licked")
        pump.on()
    elif(event == 'lick_1_off'):
        blue_LED.off()
        pump.off()





def run_end():
    print_variables()