"""
phase 2: mouse learns to react to triggers
process:
    1. start brain recording
    2. plat start beep
    3. start wheel after randomized time
    4. move trigger into whisking position after random time
    5. play sound to notify of licking window
    6. give water
    7. move trigger out of whisking position
    8. end trial
"""

from pyControl.utility import *
from devices import *

board = Breakout_1_2()

button = Digital_input(pin=board.port_1.DIO_B, rising_event='button_press',debounce=100,pull="down") 
wheel = Digital_output(pin = board.port_1.DIO_A)
port_exp = Port_expander(port = board.port_3)
speaker = Audio_board(board.port_4) # Instantiate audio board.
lickometer = Lickometer(port_exp.port_1)
motor_z = Stepper_motor(port = board.port_2)
motor_y = Stepper_motor(port = board.port_5)
motor_x = Stepper_motor(port = board.port_6)

pump = Digital_output(pin = board.BNC_2)

sync_output = Rsync(pin=board.BNC_1,mean_IPI=1500,event_name="pulse") #needs to be a digital input on the intan system
recording_trigger = Digital_output(pin = board.DAC_1) #needs to be a digital input on the intan system




#public variables
v.volume = 50 #speaker volume
v.start_frequency = 2000 #start tone start_frequency
v.water_frequency = 4000 #tone for start of water window
v.wheel_delay = 600 #delay from start of trial to start of wheel turn
v.delay_offset = 10 #percetage of offset from original value to randomize values
v.pump_duration=300*ms #pump duration for button press
v.trigger_window = 2000*ms #how long the trigger stays in place
v.motor_speed = 1500
v.motor_delay = 4000

v.time_between_trials=5000 
#private variables
v.finished_startup___ = False
v.pump_bool___=False
v.trial_counter___=0

v.motor_z_pos___=0
v.motor_y_pos___=0
v.motor_x_pos___=0

v.motors_stationary___=True
v.motors_ready___=True

states = ['start_trial','main_loop','update_motors']
initial_state = 'start_trial'
events = ['speaker_off','start_walking','pump_on','pump_off',
          'button_press','pulse','move_in','move_out','moved_in'
          ,'lick_1','lick_1_off',
          'start_trial_event','end_trial','end_experiment']


def return_home():
    if v.motor_z_pos___>0:
        motor_z.forward(v.motor_speed,v.motor_z_pos___)
        v.motor_z_pos___=0
    if v.motor_y_pos___>0:
        motor_y.forward(v.motor_speed,v.motor_y_pos___)
        v.motor_y_pos___=0
    if v.motor_x_pos___>0:
        motor_x.forward(v.motor_speed,v.motor_x_pos___)
        v.motor_x_pos___=0

    print("motors homed")

def move_motor_into_position(motor, position):
    """
    moves desired motor into position
    and updates position in variables
    in: 
        motor (string) contains motor axis (x,y,z)
        position (int) desired position in steps
    out:
        move (int) how many steps the motor need to move
    """
    move=0
    if motor=='x':
        move = position-v.motor_x_pos___
        if move>0 and move<=4800:
            motor_x.backward(v.motor_speed,move)
            v.motor_x_pos___+=move
        elif move>-4800 and move<0:
            motor_x.forward(v.motor_speed,move*(-1))
            v.motor_x_pos___+=move

    elif motor=='y':
        move = position-v.motor_y_pos___
        if move>0 and move<=4800:
            motor_y.backward(v.motor_speed,move)
            v.motor_y_pos___+=move
        elif move>=-4800 and move<0:
            motor_y.forward(v.motor_speed,move*(-1))
            v.motor_y_pos___+=move

    elif motor=='z':
        move = position-v.motor_z_pos___
        if move>0 and move<=4800:
            motor_z.backward(v.motor_speed,move)
            v.motor_z_pos___+=move
        elif move>=-4800 and move<0:
            motor_z.forward(v.motor_speed,move*(-1))
            v.motor_z_pos___+=move
    return move

def get_rand_offset():
    return randint(0,v.delay_offset)/100 + 1

def start_trial(event):  
    if(not v.finished_startup___ and (event=='start_trial_event' or v.trial_counter___==0)):
        print("trial #"+str(v.trial_counter___))
        #setup the trial
        #turn on speaker and beep for start
        speaker.set_volume(v.volume)
        speaker.sine(v.start_frequency)
        #randomize the duration before experiment begins
        rand_offset = randint(0,v.delay_offset)/100 + 1
        set_timer('start_walking',v.wheel_delay * rand_offset)
        set_timer('speaker_off',800)
        v.finished_startup___=True
        goto_state('main_loop')
        set_timer("move_in",300)




def main_loop(event):
    if event=="move_in":   
        v.motors_stationary___=False
        move = move_motor_into_position('z',4800) 
        move = max(move,move_motor_into_position('y',4000))
        move = max(move,move_motor_into_position('x',2000))
        v.motors_ready___=False
        set_timer("moved_in",move/v.motor_speed*second)
        
    elif event =="move_out":
        if v.motors_stationary___:
            v.motors_stationary___=False
            move = move_motor_into_position('y',randint(2000,3000))
            set_timer("end_trial",move/v.motor_speed*second)
            v.motors_ready___=True
        else:
            set_timer("move_out",50)

def all_states(event):
    if(event=='pump_on'):
        if(not v.pump_bool___):

            pump.on()
            v.pump_bool___=True
            set_timer('pump_off',v.pump_duration) #turn off pump after set duration

        
    if(event=='pump_off'):
        pump.off()
        v.pump_bool___=False

    if (event=='speaker_off'):
        speaker.off()
    if(not v.finished_startup___):
        #setup the trial
        recording_trigger.on()
        print("triggered recording")
    if (event=='start_walking'):
        wheel.on()
        v.finished_startup___=True

    elif event=='moved_in': #runs when trigger moved into place
        v.motors_stationary___=True
        speaker.sine(v.water_frequency)
        set_timer('speaker_off',500)
        set_timer('pump_on',800)
        set_timer('move_out',v.trigger_window)
        goto_state('main_loop')
    
    if (event=='end_trial'):
        #make sure all devices are off
        speaker.off()
        pump.off()
        wheel.off()

        print_variables()
        v.trial_counter___+=1

        #reset flags
        v.finished_startup___=False
        v.motors_stationary___=True
        v.motors_ready___=True

        set_timer('start_trial_event',v.time_between_trials)
        goto_state('start_trial')
    if (event=='end_experiment'):
        stop_framework()

def run_end():
    #make sure all devices are off
    return_home()
    speaker.off()
    pump.off()
    wheel.off()
    recording_trigger.off()
    print("stopped recording")
    print_variables()