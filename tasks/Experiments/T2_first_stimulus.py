"""
phase 2: mouse learns to react to stimuli
process:
    1. beep for start if trial
    2. after time start moving wheel
    3. move stimulus into place (make the position changeable variable)
    4. move stimulus out after set duration (also variable)
    5. play beep to signal water (different frequency from the start)
    6. give water after set duration from wheel start (also variable)
    7. stop wheel
    8. end trial start inter_trial_interval timer until going back to stage 1
"""

from pyControl.utility import *
from devices import *

board = Breakout_1_2()

button = Digital_input(pin=board.port_1.DIO_B, rising_event='button_press',debounce=100,pull="down") 
wheel = Digital_output(pin = board.port_1.DIO_A)
port_exp = Port_expander(port = board.port_3)
speaker = Audio_board(board.port_4) # Instantiate audio board.
# lickometer = Lickometer(port_exp.port_1) #no need for lickometer in this experiment
motor_z = Stepper_motor(port = board.port_2)
motor_y = Stepper_motor(port = board.port_5)
motor_x = Stepper_motor(port = board.port_6)

pump = Digital_output(pin = board.BNC_2)

sync_output = Rsync(pin=board.BNC_1,mean_IPI=1500,event_name="pulse") #needs to be a digital input on the intan system
recording_trigger = Digital_output(pin = board.DAC_1) #needs to be a digital input on the intan system




#public variables
v.number_of_trials=-1 #amount of trials to run for this task, if -1 run until manually stopped
v.beep_volume = 50 #speaker volume
v.start_beep_frequency = 2000 #start tone start_frequency
v.water_beep_frequency = 4000 #tone for start of water window
v.delay_to_start_wheel = 300 #delay from start of trial to start of wheel turn
v.delay_for_water_after_trial_start=100 #time to wait before giving water after wheel stops
v.wheel_delay_offset = 10 #percentage of offset from original value to randomize values
v.pump_duration=75*ms #pump duration for button press
v.stimulus_time_window = 3000*ms #how long the stimulus stays in place
v.stimulus_motor_speed = 1500
v.trial_duration=4000
v.stimulus_delay_from_start_of_trial=300 #the amount of time to wait before stimulus moves into whisking position from trial start
v.inter_trial_interval=5000 

#position in whisking area
v.stimulus_x_value=2000
v.stimulus_y_value=4000
v.stimulus_z_value=4800

#limits to move out of whisking area
v.stimulus_x_outer_bounds=(800,1200)
v.stimulus_y_outer_bounds=(2000,3000)
v.stimulus_z_outer_bounds=(3000,3500)

#private variables
v.finished_startup___ = False
v.pump_bool___=False
v.trial_counter___=0

v.motor_z_pos___=0
v.motor_y_pos___=0
v.motor_x_pos___=0

v.motors_stationary___=True
v.motors_ready___=True

# Custom controls dialog declaration
v.custom_controls_dialog = "T2_validation_gui"  # advanced example dialog that is loaded from a .py file


states = ['start_trial','main_loop','update_motors']
initial_state = 'start_trial'
events = ['speaker_off','start_walking','pump_on','pump_off',
          'button_press','pulse','move_in','move_out','moved_in'
          ,'lick_1','lick_1_off',
          'start_trial_event','end_trial','end_experiment']
    
    
def return_home():
    if v.motor_z_pos___>0:
        motor_z.forward(v.stimulus_motor_speed,v.motor_z_pos___)
        v.motor_z_pos___=0
    if v.motor_y_pos___>0:
        motor_y.forward(v.stimulus_motor_speed,v.motor_y_pos___)
        v.motor_y_pos___=0
    if v.motor_x_pos___>0:
        motor_x.forward(v.stimulus_motor_speed,v.motor_x_pos___)
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
            motor_x.backward(v.stimulus_motor_speed,move)
            v.motor_x_pos___+=move
        elif move>-4800 and move<0:
            motor_x.forward(v.stimulus_motor_speed,move*(-1))
            v.motor_x_pos___+=move

    elif motor=='y':
        move = position-v.motor_y_pos___
        if move>0 and move<=4800:
            motor_y.backward(v.stimulus_motor_speed,move)
            v.motor_y_pos___+=move
        elif move>=-4800 and move<0:
            motor_y.forward(v.stimulus_motor_speed,move*(-1))
            v.motor_y_pos___+=move

    elif motor=='z':
        move = position-v.motor_z_pos___
        if move>0 and move<=4800:
            motor_z.backward(v.stimulus_motor_speed,move)
            v.motor_z_pos___+=move
        elif move>=-4800 and move<0:
            motor_z.forward(v.stimulus_motor_speed,move*(-1))
            v.motor_z_pos___+=move
    return move

def get_rand_offset():
    return randint(0,v.wheel_delay_offset)/100 + 1

def start_trial(event):  
    try:
        if(not v.finished_startup___ and (event=='start_trial_event' or v.trial_counter___==0)):
            print("trial #"+str(v.trial_counter___))
            #setup the trial
            #turn on speaker and beep for start
            speaker.set_volume(v.beep_volume)
            speaker.sine(v.start_beep_frequency)
            #randomize the duration before experiment begins
            rand_offset = randint(0,v.wheel_delay_offset)/100 + 1
            set_timer('start_walking',v.delay_to_start_wheel * rand_offset)
            set_timer('pump_on',v.delay_for_water_after_trial_start)
            set_timer('speaker_off',800)
            v.finished_startup___=True
            goto_state('main_loop')
            set_timer("move_in",v.stimulus_delay_from_start_of_trial)
            set_timer('end_trial',v.trial_duration)
    except Exception as e:
        print(e)
        stop_framework()




def main_loop(event):
    try:
        if event=="move_in":   
            v.motors_stationary___=False
            #calls the function that move along axis, the function returns the ETA
            #takes the max of all axes ETA for the next event
            moving_time = move_motor_into_position('z',v.stimulus_z_value) 
            moving_time = max(moving_time,move_motor_into_position('y',v.stimulus_y_value))
            moving_time = max(moving_time,move_motor_into_position('x',v.stimulus_x_value))
            v.motors_ready___=False
            set_timer("moved_in",moving_time/v.stimulus_motor_speed*second)
            
        elif event =="move_out":
            if v.motors_stationary___:
                v.motors_stationary___=False
                #calls the function that move along axis, the function returns the ETA
                #takes the max of all axes ETA for the next event
                moving_time = move_motor_into_position('y',randint(v.stimulus_y_outer_bounds[0],v.stimulus_y_outer_bounds[1]))
                moving_time = max(moving_time,move_motor_into_position('x',randint(v.stimulus_x_outer_bounds[0],v.stimulus_x_outer_bounds[1])))
                moving_time = max(moving_time,move_motor_into_position('z',randint(v.stimulus_z_outer_bounds[0],v.stimulus_z_outer_bounds[1])))
                set_timer("end_trial",moving_time/v.stimulus_motor_speed*second)
                v.motors_ready___=True
            else:
                set_timer("move_out",50)
    except Exception as e:
        print(e)
        stop_framework()

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

    elif event=='moved_in': #runs when stimulus moved into place
        v.motors_stationary___=True
        speaker.sine(v.water_beep_frequency)
        set_timer('speaker_off',500)
        set_timer('move_out',v.stimulus_time_window)
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
        #if amount of trials is reached, end task
        #if amount of trials set to -1, will never stop automatically
        if v.trial_counter___!=v.number_of_trials:
            set_timer('start_trial_event',v.inter_trial_interval)
            goto_state('start_trial')
        else:
            stop_framework()
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