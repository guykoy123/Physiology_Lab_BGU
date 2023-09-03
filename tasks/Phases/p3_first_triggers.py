"""
phase 3: mouse learns to react to triggers
process:
    1. start brain recording
    2. plat start beep
    3. start wheel after randomized time
    4. move trigger into whisking position after random time
    5. lab worker pushes button to dispense water
    5. move trigger out of whisking position
    7. stop recording
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
v.frequency = 2000 #start tone frequency
v.wheel_delay = 900 #delay from start of trial to start of wheel turn
v.delay_offset = 10 #percetage of offset from original value to randomize values
v.pump_duration=300*ms #pump duration for button press
v.trigger_delay = 500*ms
v.motor_speed = 1500
v.motor_delay = 4000
#private variables
v.finished_startup___ = False
v.pump_bool___=False

v.motor_z_pos___=0
v.motor_y_pos___=0
v.motor_x_pos___=0

v.motors_stationary___=True
v.motors_ready___=True
states = ['startup','main_loop','update_motors']
initial_state = 'startup'
events = ['speaker_off','start_walking','pump_off','button_press','pulse','move_in','move_out'
          ,'lick_1','lick_1_off','stationary']


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
            return_home()
            #turn on speaker and beep for start
            speaker.set_volume(v.volume)
            speaker.sine(v.frequency)
            #randomize the duration before experiment begins
            set_timer('start_walking',v.wheel_delay * get_rand_offset())
            set_timer('speaker_off',800)
            # set_timer('move_in', v.motor_delay*rand_offset)



def main_loop(event):
    if event=="move_in":   
        v.motors_stationary___=False
        move = move_motor_into_position('z',4800) 
        move = max(move,move_motor_into_position('y',4000))
        move = max(move,move_motor_into_position('x',2000))
        v.motors_ready___=False
        timed_goto_state("update_motors",move/v.motor_speed*second)
        
    elif event =="move_out":
        if v.motors_stationary___:
            v.motors_stationary___=False
            move = move_motor_into_position('y',randint(2000,3000))
            timed_goto_state("update_motors",move/v.motor_speed*second)
            v.motors_ready___=True
        else:
            set_timer("move_out",50)

def update_motors(event):
    if event=='entry':
        v.motors_stationary___=True
    elif event!='exit':
        goto_state('main_loop')

def all_states(event):
    if(event=='button_press'): #on event of button press and the pump is not active give water
        if(not v.pump_bool___):
            pump.on()
            v.pump_bool___=True
            set_timer('pump_off',v.pump_duration) #turn off pump after set duration
            set_timer("move_out",50)
        
    if(event=='pump_off'):
        pump.off()
        v.pump_bool___=False

    if (event=='speaker_off'):
        speaker.off()
    if(not v.finished_startup___):
        #setup the trial
        recording_trigger.on()
        print("triggered recording")
    elif v.motors_stationary___ and v.motors_ready___ and v.finished_startup___:
        v.motors_ready___=False
        v.motors_stationry=False
        set_timer('move_in',v.motor_delay*get_rand_offset())
        

def run_end():
    #make sure all devices are off
    return_home()
    speaker.off()
    pump.off()
    wheel.off()
    recording_trigger.off()
    print("stopped recording")
    print_variables()