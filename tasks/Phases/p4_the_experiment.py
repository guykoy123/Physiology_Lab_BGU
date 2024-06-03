"""
In the experiment mouse will be shown stimuli in different positions preset before the start. will receive water for licking at correct one, punishment for incorrect one.

important variables:

- correct stimulus position - (x,y,z)
- catch trial stimulus position - (x,y,z)
- catch trial probability
- offset from correct position lists, per axis, that hold position offset of additional positions
- position probability list - holds probability to choose each of the possible position (including correct position)


1. check validity of preset positions and probabilities for the experiment
2. start brain recording
3. lab worker confirms camera has been turned on
4. begin trials (until trial counter reaches preset amount, or indefinitely)
   1. start trial - beep for start
   2. move wheel after some time
   3. pick between regular trial or catch trial (based on probability variable)
      1. catch trial - move stimulus into catch trial position (preset before experiment start)
      2. regular trial - pick position from possible position list based on probability list corresponding to each position. Then move the stimulus into chosen position
   4. beep for licking period
      1. lick on correct stimulus - give water
      2. lick on incorrect stimulus - don't give water, add punishment period to inter trial interval
   5. move trigger out
   6. stop wheel
   7. stop trial
   8. start inter trial interval, when it ends go back to stage 'a' - start trial
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

#"correct" position in whisking area
v.correct_stimulus_x_value=2000
v.correct_stimulus_y_value=4000
v.correct_stimulus_z_value=4800

#offset from correct position lists, one for each axis
v.x_stimulus_offset=[]
v.y_stimulus_offset=[]
v.z_stimulus_offset=[]

#position probability list. first one is the correct position, the rest are corresponding to their order in the offset list
v.position_probability_list=[]
v.position_CDF_list___=[] #Cumulative distribution function for the probabilities

#catch trial position - absolute value
v.catch_trial_x_position = 0
v.catch_trial_y_position = 0
v.catch_trial_z_position = 0

#how many of total trials will be catch trials
v.probability_of_catch_trial=0.05

#limits to move out of whisking area
v.stimulus_x_outer_bounds=(800,1200)
v.stimulus_y_outer_bounds=(2000,3000)
v.stimulus_z_outer_bounds=(3000,3500)


#time to add to time_between_trials to punish mouse for wrong lick
v.punishment_period=2000
v.punishment_for_incorrect_timing=False
v.punishment_for_incorrect_stimulus=False
v.add_punishment___=False

#private variables
v.finished_startup___ = False
v.pump_bool___=False #pump on/off

v.trial_counter___=0
v.correct_lick_counter___=0 #in how many trials the mouse licked correctly
v.correct_position_counter___=0 #in how many trials the stimulus was placed in the correct position
v.licked_this_window___=False #flag if mouse has licked in allowed window of time for current trial

#current stimulus position
v.motor_z_pos___=0
v.motor_y_pos___=0
v.motor_x_pos___=0
v.in_correct_position_flag___=False
v.motors_stationary___=True
v.motors_ready___=True
states = ['start_trial','main_loop','update_motors']
initial_state = 'start_trial'
events = ['speaker_off','start_walking','pump_off','pump_on','pulse','move_in','move_out'
          ,'lick_1','lick_1_off','exit_position',
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
    #TODO: add position and probability validation
    #calculate Cumulative distribution function for position probabilities
    for i in range(len(v.position_probability_list)):
        v.position_CDF_list___.append(sum(v.position_probability_list[0:i+1]))
    print("CDF: " + str(v.position_CDF_list___))
    print("starting recording")

def start_trial(event):  
    if(not v.finished_startup___ and event=='start_trial_event'): #first trial will only start if worker has triggered the event manually, meaning the camera is recording
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
    if (event=='start_walking'):
        wheel.on()
        v.finished_startup___=True
        
        goto_state('main_loop')




def main_loop(event):
    """
    event=="move_in"
        pick stimulus target position, set x/y/z_position to desired value
        run move_motor_into_position for each axis while setting the wait time to the max
    event =="move_out"
        move stimulus out of position to the waiting spot
    """
    #move stimulus into position
    if event=="move_in":   
        v.motors_stationary___=False
        random_value=random()
        if random_value<=v.probability_of_catch_trial:   #pick regular trial or catch trial:
            z_position = v.catch_trial_z_position
            x_position = v.catch_trial_x_position
            y_position = v.catch_trial_y_position
            print("catch trial")

        else:
            #generate value between 0 and 1 to pick a desired position (using the CDF)
            #set x/y/z_position to desired value
            #move motor into position
            random_value = random() #pick random material based on preset ratio
            print("random value: "+str(random_value))
            for i in range(len(v.position_CDF_list___)):
                if v.position_CDF_list___[i]>=random_value:
                    print("moving to position "+ str(i) + "(0 - correct position)")
                    if i==0:
                        x_position = v.correct_stimulus_x_value
                        y_position = v.correct_stimulus_y_value
                        z_position = v.correct_stimulus_z_value
                    x_position = v.x_stimulus_offset[i-1]+v.correct_stimulus_x_value
                    y_position = v.y_stimulus_offset[i-1]+v.correct_stimulus_y_value
                    z_position = v.z_stimulus_offset[i-1]+v.correct_stimulus_z_value
                    break

        
        moving_time = move_motor_into_position('z',z_position) 
        #calls the function that move along axis, the function returns the ETA
        #takes the max of all axes ETA for the next event
        moving_time = max(moving_time,move_motor_into_position('y',y_position))
        moving_time = max(moving_time,move_motor_into_position('x',x_position))
        v.motors_ready___=False
        timed_goto_state("update_motors",moving_time*0.9/v.stimulus_motor_speed*second) #wait for motors to finish setting stimulus in position
        
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

        

def update_motors(event):
    if event=='entry':
        v.motors_stationary___=True
        speaker.sine(v.water_beep_frequency)
        set_timer('speaker_off',500)
        set_timer('exit_position',v.stimulus_time_window) 
    elif event=='exit_position': #if picked random position that's no the correct one move back to waiting
        set_timer('move_out',50)
        goto_state('main_loop')

def all_states(event):

    if event=="lick_1": #if mouse licks correctly disarm the incorrect position event, turn pump on and go back to main loop
        if v.finished_startup___ and v.motors_stationary___ and v.in_correct_position_flag___ and not v.licked_this_window___ and not v.motors_ready___:
            v.licked_this_window___=True
            v.correct_lick_counter___+=1
            publish_event("pump_on")
        #if mouse licks for incorrect stimulus set punishment flag to True
        elif v.punishment_for_incorrect_stimulus and v.finished_startup___ and v.motors_stationary___ and not v.licked_this_window___ and not v.motors_ready___:
            v.add_punishment___=True
        elif v.punishment_for_incorrect_timing and not v.licked_this_window___:
            v.add_punishment___=True
            
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
            set_timer('start_trial_event',v.time_between_trials + v.add_punishment___*v.punishment_period)
            if v.add_punishment___:
                print("adding punishment period")
            v.add_punishment___=False
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
    if v.correct_position_counter___!=0:
        print("success rate: " +str(v.correct_lick_counter___/v.correct_position_counter___*100)+"%")