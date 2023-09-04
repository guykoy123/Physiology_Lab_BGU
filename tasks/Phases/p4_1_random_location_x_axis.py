"""
phase 4.1: mouse is tested on ability to distinguish between positions of triggers
process:
    1. start brain recording
    2. pick correct location for experiment
    3. play start beep
    4. start wheel after randomized time
    5. move trigger into whisking position after random time (location is randomly picked from list)
    6. if correct location and mouse licked - dispense water
    7. move trigger out of whisking position
    8. stop recording
"""

from pyControl.utility import *
from devices import *

board = Breakout_1_2()

# button = Digital_input(pin=board.port_1.DIO_B, rising_event='button_press',debounce=100,pull="down") 
wheel = Digital_output(pin = board.port_1.DIO_A)
port_exp = Port_expander(port = board.port_3)
speaker = Audio_board(board.port_4) # Instantiate audio board.
lickometer = Lickometer(port_exp.port_1,debounce=20)
motor_z = Stepper_motor(port = board.port_2)
motor_y = Stepper_motor(port = board.port_5)
motor_x = Stepper_motor(port = board.port_6)

pump = Digital_output(pin = board.BNC_2)

sync_output = Rsync(pin=board.BNC_1,mean_IPI=1500,event_name="pulse") #needs to be a digital input on the intan system
recording_trigger = Digital_output(pin = board.DAC_1) #needs to be a digital input on the intan system




#public variables
# v.custom_variables_dialog ="custom_variables_dialog"
v.volume = 50 #speaker volume
v.frequency = 2000 #start tone frequency
v.wheel_delay = 900 #delay from start of trial to start of wheel turn
v.delay_offset = 10 #percetage of offset from original value to randomize values
v.pump_duration=300*ms #pump duration for button press
v.trigger_delay = 500*ms
v.motor_speed = 1500
v.motor_delay = 4000
v.delay_in_position=3000 #amount of time trigger will stay in position before moving out
v.area_for_trigger_to_move_out=[2000,3000] #values between them the trigger will move to wait outside of mouse feeling range

#value of z and y to be close to mouse
v.z_value=4800 
v.y_value=4000
v.x_value=2000
#x values around the mouse that will be randomly set
v.positions = [1800,1900,2000,2150]
v.correct_position=-1 #if -1 pick random from list. else means the lab worker preset a position

#private variables
v.finished_startup___ = False
v.pump_bool___=False

v.motor_z_pos___=0
v.motor_y_pos___=0
v.motor_x_pos___=0
v.in_correct_position_flag___=False
v.motors_stationary___=True
v.motors_ready___=True
states = ['startup','main_loop','update_motors']
initial_state = 'startup'
events = ['speaker_off','start_walking','pump_off','pump_on','pulse','move_in','move_out'
          ,'lick_1','lick_1_off','incorrect_position']


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
    if event== 'entry':
        if(not v.finished_startup___):
            #setup the trial
            #pick random correct position for experiment
            if v.correct_position==-1:
                v.correct_position=choice(v.positions) #pick random correct location
            else:
                if v.correct_position not in v.positions: #if lab worker picked location out of list stop framework
                    print("Error: location out of list")
                    stop_framework()
            print("correct position for this experiment: " + str(v.correct_position))
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
    if (event=='start_walking'):
        wheel.on()
        v.finished_startup___=True
        
        goto_state('main_loop')




def main_loop(event):

    #move trigger into position
    if event=="move_in":   
        v.motors_stationary___=False
        #move each motor while saving the longest amount of moving one of the motors need to do to calculate how much time to wait
        move = move_motor_into_position('z',v.z_value) 
        move = max(move,move_motor_into_position('y',v.y_value))
        x_position = choice(v.positions) #pick random position on x axis
        if x_position == v.correct_position:
            v.in_correct_position_flag___=True
            print("moved into correct position - " + str(x_position))
        else:
            print("moved into incorrect position - " + str(x_position))
        move = max(move,move_motor_into_position('x',x_position))
        v.motors_ready___=False
        timed_goto_state("update_motors",move*0.9/v.motor_speed*second) #wait for motors to finish setting trigger in position
        
    elif event =="move_out": #move out of position to waiting spot
        if v.motors_stationary___ and not v.motors_ready___:
            v.in_correct_position_flag___=False
            v.motors_stationary___=False
            move = move_motor_into_position('y',randint(v.area_for_trigger_to_move_out[0],v.area_for_trigger_to_move_out[1]))
            
            timed_goto_state("main_loop",move/v.motor_speed*second)
            v.motors_ready___=True
            v.motors_stationary___=True

        

def update_motors(event):
    if event=='entry':
        v.motors_stationary___=True
        set_timer('incorrect_position',v.delay_in_position) 
    elif event=="lick_1": #if mouse licks correctly disarm the incorrect position event, turn pump on and go back to main loop
        if v.finished_startup___ and v.motors_stationary___ and v.in_correct_position_flag___:
            disarm_timer('incorrect_position')
            publish_event("pump_on")
            goto_state('main_loop')
    elif event=='incorrect_position': #if picked random position that's no the correct one move back to waiting
        set_timer('move_out',50)
        goto_state('main_loop')

def all_states(event):
    if(event=='pump_on'):
        if(not v.pump_bool___):
            pump.on()
            v.pump_bool___=True
            set_timer('pump_off',v.pump_duration) #turn off pump after set duration
            
        
    if(event=='pump_off'):
        pump.off()
        v.pump_bool___=False
        goto_state('main_loop')
        set_timer("move_out",50)

    if (event=='speaker_off'):
        speaker.off()

    #trigger moves in when okay after a random time
    elif v.motors_stationary___ and v.motors_ready___ and v.finished_startup___:
        v.motors_ready___=False
        v.motors_stationary___=False
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