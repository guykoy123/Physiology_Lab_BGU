"""
phase 3: mouse is taught  to distinguish between two different materials
process:
    1. start brain recording
    2. play start beep
    3. start wheel after randomized time
    4. move stimulus into whisking position after random time (location is randomly picked from two options)
    5. if correct material dispense water
    6. move stimulus out of whisking position
    7. end trial
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
recording_trigger = Digital_output(pin = port_exp.port_2.DIO_A) #needs to be a digital input on the intan system




#public variables
v.amount_of_trials=-1 #amount of trials to run for this task, if -1 run until manually stopped
v.beep_volume = 50 #speaker volume
v.start_beep_frequency = 2000 #start tone start_frequency
v.water_beep_frequency = 4000 #tone for start of water window
v.delay_to_start_wheel = 300 #delay from start of trial to start of wheel turn
v.wheel_delay_offset = 10 #percentage of offset from original value to randomize values
v.pump_duration=75*ms #pump duration for button press
v.stimulus_time_window = 3000*ms #how long the stimulus stays in place
v.stimulus_motor_speed = 1500

v.time_between_trials=5000 

v.percentage_of_reference_material=0.5  


#position in whisking area
v.stimulus_x_value=2000
v.stimulus_y_value=4000
v.stimulus_z_value=4800

#limits to move out of whisking area
v.stimulus_x_outer_bounds=(800,1200)
v.stimulus_y_outer_bounds=(2000,3000)
v.stimulus_z_outer_bounds=(3000,3500)

#z values around the mouse that will be randomly set
#first position is the reference material (correct material)
v.material_positions = [4800,4000]
v.correct_position___=0

#private variables
v.finished_startup___ = False
v.pump_bool___=False

v.trial_counter___=0
v.correct_material_counter___=0
v.correct_licks_counter___=0
v.licked_this_window___=False

v.motor_z_pos___=0
v.motor_y_pos___=0
v.motor_x_pos___=0
v.in_correct_position_flag___=False
v.motors_stationary___=True
v.motors_ready___=True

states = ['start_trial','main_loop','update_motors']
initial_state = 'start_trial'
events = ['speaker_off','start_walking','pump_off','pump_on','pulse','move_in','moved_in','move_out'
          ,'lick_1','lick_1_off','incorrect_position',
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

def run_start():  
    recording_trigger.on()
    print("starting recording!!!!!!!!!!!!!!!!!")


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
        set_timer("move_in",300)

def main_loop(event):

    #move stimulus into position
    if event=="move_in":   
        v.motors_stationary___=False
        #move each motor while saving the longest amount of moving one of the motors need to do to calculate how much time to wait
        random_value = random() #pick random material based on preset ratio
        if random_value<=v.percentage_of_reference_material:
            z_position = v.material_positions[0] 
            v.in_correct_position_flag___=True
            print("moved into correct position - " + str(z_position))
            v.correct_material_counter___+=1
        else:
            z_position=v.material_positions[1]
            print("moved into incorrect position - " + str(z_position))
        moving_time = move_motor_into_position('z',z_position) 
        #calls the function that move along axis, the function returns the ETA
        #takes the max of all axes ETA for the next event
        moving_time = max(moving_time,move_motor_into_position('y',v.stimulus_y_value))
        moving_time = max(moving_time,move_motor_into_position('x',v.stimulus_x_value))
        v.motors_ready___=False
        set_timer("moved_in",moving_time*0.9/v.stimulus_motor_speed*second) #wait for motors to finish setting stimulus in position
        
    elif event =="move_out": #move out of position to waiting spot
        if v.motors_stationary___ and not v.motors_ready___:
            v.in_correct_position_flag___=False
            v.motors_stationary___=False
            #calls the function that move along axis, the function returns the ETA
            #takes the max of all axes ETA for the next event
            moving_time = move_motor_into_position('y',randint(v.stimulus_y_outer_bounds[0],v.stimulus_y_outer_bounds[1]))
            moving_time = max(moving_time,move_motor_into_position('x',randint(v.stimulus_x_outer_bounds[0],v.stimulus_x_outer_bounds[1])))
            moving_time = max(moving_time,move_motor_into_position('z',randint(v.stimulus_z_outer_bounds[0],v.stimulus_z_outer_bounds[1])))
            set_timer("end_trial",moving_time/v.stimulus_motor_speed*second)
            v.motors_ready___=True
            v.motors_stationary___=True
    
    if event=='lick_1' and v.motors_stationary___ and not v.motors_ready___ and v.in_correct_position_flag___ and not v.licked_this_window___:
        v.correct_licks_counter___+=1
        v.licked_this_window___=True



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

    if (event=='start_walking'):
        wheel.on()
        v.finished_startup___=True

    elif event=='moved_in': #runs when stimulus moved into place
        v.motors_stationary___=True
        speaker.sine(v.water_beep_frequency)
        set_timer('speaker_off',500)
        if v.in_correct_position_flag___:
            set_timer('pump_on',1000)
        set_timer('move_out',v.stimulus_time_window)
        goto_state('main_loop')
    
    if (event=='end_trial'):
        #make sure all devices are off
        speaker.off()
        pump.off()
        wheel.off()

        # print_variables()
        v.trial_counter___+=1

        #reset flags
        v.finished_startup___=False
        v.motors_stationary___=True
        v.motors_ready___=True
        v.licked_this_window___=False
        #if amount of trials is reached, end task
        #if amount of trials set to -1, will never stop automatically
        if v.trial_counter___!=v.amount_of_trials:
            set_timer('start_trial_event',v.time_between_trials)
            goto_state('start_trial')
        else:
            stop_framework()
    if (event=='end_experiment'):
        stop_framework()

        

def run_end():
    print('total {} trials. reference material was presented {} times. mouse licked correctly {} times'.format(v.trial_counter___,v.correct_material_counter___,v.correct_licks_counter___))
    #make sure all devices are off
    return_home()
    speaker.off()
    pump.off()
    wheel.off()
    recording_trigger.off()
    print("stopped recording")
    print_variables()