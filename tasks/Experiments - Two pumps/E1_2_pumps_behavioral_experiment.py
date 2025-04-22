"""
Can be used for the experiment but also for teaching the mouse the different stimuli
Mouse will be shown two simuli,
For simulai A will have to lick 1
For simulai B will have to lick 2

"""

from pyControl.utility import *
from devices import *
# from hardware_definitions.full_hardware_definition import *


board = Breakout_1_2()

# button = Digital_input(pin=board.port_1.DIO_B, rising_event='button_press',debounce=100,pull="down") 
wheel = Digital_output(pin = board.port_1.DIO_A)
port_exp = Port_expander(port = board.port_3)
speaker = Audio_board(board.port_4) # Instantiate audio board.
lickometer = Lickometer(port_exp.port_1,debounce=20)
motor_z = Stepper_motor(port = board.port_2)
motor_y = Stepper_motor(port = board.port_5)
motor_x = Stepper_motor(port = board.port_6)
laser=Digital_output(pin = port_exp.port_2.DIO_B)

pump_1 = Digital_output(pin = board.BNC_2)
pump_2 = Digital_output(pin = port_exp.port_3.DIO_B)

sync_output = Rsync(pin=board.BNC_1,mean_IPI=1500,event_name="pulse") #needs to be a digital input on the intan system
recording_trigger = Digital_output(pin = port_exp.port_2.DIO_A) #needs to be a digital input on the intan system

trial_pulse=Digital_output(port_exp.port_3.DIO_A) #a pulse will be sent at the start of each trial to signal to an external system


# Custom controls dialog declaration
v.custom_controls_dialog = "E1_2_pumps_validation_gui"  # advanced example dialog that is loaded from a .py file



#public variables
v.number_of_trials=-1 #amount of trials to run for this task, if -1 run until manually stopped
v.beep_volume = 50 #speaker volume
v.start_beep_frequency = 2000 #start tone start_frequency
v.water_beep_frequency = 4000 #tone for start of water window
v.delay_to_start_wheel = 300 #delay from start of trial to start of wheel turn
v.wheel_delay_offset = 10 #percentage of offset from original value to randomize values
v.pump_duration=75*ms #pump duration for button press
v.stimulus_time_window = 3000*ms #how long the stimulus stays in place
v.stimulus_motor_speed = 1500

#laser variables
v.laser_on=False #laser switch
v.laser_delay_from_start=200 #delay from the start of the trial to start pulsing the laser
v.laser_number_of_pulses=5
v.laser_pulse_duration=5
v.laser_inter_pulse_interval=10
v.laser_pulse_counter___=0

v.inter_trial_interval=5000 

# position A in whisking area
v.stimulus_A_x_value=2000
v.stimulus_A_y_value=4000
v.stimulus_A_z_value=4800

#position B in whisking area
v.stimulus_B_x_value=2000
v.stimulus_B_y_value=4000
v.stimulus_B_z_value=4500

v.probability_of_pos_A=0.5 #rest is for position B 

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


#time to add to inter_trial_interval to punish mouse for wrong lick
v.punishment_period=2000
v.punishment_for_incorrect_timing=False
v.punishment_for_incorrect_stimulus=False
v.add_punishment___=False

#private variables
v.finished_startup___ = False
v.pump_1_bool___=False #pump on/off
v.pump_2_bool___=False #pump on/off

v.trial_counter___=0
v.correct_lick_counter___=0 #in how many trials the mouse licked correctly
v.correct_stimulus_counter___=0 #in how many trials the stimulus was placed in the correct position
v.licked_this_window___=False #flag if mouse has licked in allowed window of time for current trial

#current stimulus position
v.motor_z_pos___=0
v.motor_y_pos___=0
v.motor_x_pos___=0

v.in_pos_A___=False
v.in_pos_B___=False

v.motors_stationary___=True
v.motors_ready___=True

states = ['start_trial','main_loop','update_motors']
initial_state = 'start_trial'
events = ['speaker_off','start_walking','pump_1_off','pump_1_on','pulse','move_in','move_out'
          ,'lick_1','lick_1_off','lick_2','lick_2_off','exit_position','laser_on','laser_off',
          'start_trial_event','end_trial','end_experiment' ,'stop_trial_pulse',
          'pump_2_on','pump_2_off']


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

def get_rand_offset(): #returns a random number of time to be added to delay
    return randint(0,v.wheel_delay_offset)/100 + 1


def run_start():  
    recording_trigger.on()

    print("starting recording")

def start_trial(event):  
    if(not v.finished_startup___ and event=='start_trial_event'): #first trial will only start if worker has triggered the event manually, meaning the camera is recording
        print("trial #"+str(v.trial_counter___))
        print("laser on: " +str(v.laser_on))
        #setup the trial
        #turn on speaker and beep for start
        speaker.set_volume(v.beep_volume)
        speaker.sine(v.start_beep_frequency)

        #randomize the duration before experiment begins
        rand_offset = randint(0,v.wheel_delay_offset)/100 + 1
        set_timer('start_walking',v.delay_to_start_wheel * rand_offset)
        set_timer('speaker_off',800)

        v.finished_startup___=True

        trial_pulse.on()
        set_timer("stop_trial_pulse",5)

        goto_state('main_loop')
        if v.laser_on:
            set_timer("laser_on",v.laser_delay_from_start)
        set_timer("move_in",300)

        # #calculate Cumulative distribution function for position probabilities
        # if not len(v.position_CDF_list___)>0:
        #     for i in range(len(v.position_probability_list)):
        #         v.position_CDF_list___.append(sum(v.position_probability_list[0:i+1]))
        #     print("CDF: " + str(v.position_CDF_list___))
        

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
            #generate value between 0 and 1 to pick a desired position 
            #set x/y/z_position to desired value
            #move motor into position
            random_value = random() #pick random material based on preset ratio
            print("random value: "+str(random_value))
            if random_value<=v.probability_of_pos_A:
                x_position = v.stimulus_A_x_value
                y_position = v.stimulus_A_y_value
                z_position = v.stimulus_A_z_value
                v.in_pos_A___=True
                print("moving into position A")
            else:
                x_position = v.stimulus_B_x_value
                y_position = v.stimulus_B_y_value
                z_position = v.stimulus_B_z_value
                v.in_pos_B___=True
                print("moving into position B")
        
        moving_time = move_motor_into_position('z',z_position) 
        #calls the function that move along axis, the function returns the ETA
        #takes the max of all axes ETA for the next event
        moving_time = max(moving_time,move_motor_into_position('y',y_position))
        moving_time = max(moving_time,move_motor_into_position('x',x_position))
        v.motors_ready___=False
        timed_goto_state("update_motors",moving_time*0.9/v.stimulus_motor_speed*second) #wait for motors to finish setting stimulus in position
        
    elif event =="move_out": #move out of position to waiting spot
        if v.motors_stationary___ and not v.motors_ready___:
            v.in_pos_A___=False
            v.in_pos_B___=False
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
        print("start lick window")
        set_timer('speaker_off',500)
        set_timer('exit_position',v.stimulus_time_window) 
        # print("flag states: ")
        # print("finished startup" + str(v.finished_startup___))
        # print("v.motors.stationary" +str(v.motors_stationary___))
        # print("in_position A" + str(v.in_pos_A___))
        # print("in_position B" + str(v.in_pos_B___))
        # print("licked_this_window" + str(v.licked_this_window___))
        # print("motors ready" + str(v.motors_ready___))
    elif event=='exit_position': #if picked random position that's no the correct one move back to waiting
        set_timer('move_out',50)
        goto_state('main_loop')

def all_states(event): 
    # mouse only gets one chance to lick correctly. 
    # meaning if he licks first the wrong spout then the right one he will get no water and punishment time will be added
    if event=="lick_1": #if mouse licks pump 1 disarm the incorrect position event, turn pump on and go back to main loop
        # print("flag states: ")
        # print("finished startup" + str(v.finished_startup___))
        # print("v.motors.stationary" +str(v.motors_stationary___))
        # print("in_position A" + str(v.in_pos_A___))
        # print("licked_this_window" + str(v.licked_this_window___))
        # print("motors ready" + str(v.motors_ready___))
        if v.finished_startup___ and v.motors_stationary___ and v.in_pos_A___ and not v.licked_this_window___ and not v.motors_ready___:
            v.licked_this_window___=True
            v.correct_lick_counter___+=1
            publish_event("pump_1_on")
            print("licked correctly for position A")

        #if mouse licks for incorrect stimulus set punishment flag to True
        elif v.punishment_for_incorrect_stimulus and v.finished_startup___ and v.motors_stationary___ and not v.licked_this_window___ and not v.motors_ready___:
            v.add_punishment___=True
        elif v.punishment_for_incorrect_timing and not v.licked_this_window___:
            v.add_punishment___=True

    if event=="lick_2":
        if v.finished_startup___ and v.motors_stationary___ and v.in_pos_B___ and not v.licked_this_window___ and not v.motors_ready___:
            v.licked_this_window___=True
            v.correct_lick_counter___+=1
            publish_event("pump_2_on")
            print("licked correctly for position B")
        
        #if mouse licks for incorrect stimulus set punishment flag to True
        elif v.punishment_for_incorrect_stimulus and v.finished_startup___ and v.motors_stationary___ and not v.licked_this_window___ and not v.motors_ready___:
            v.add_punishment___=True
        elif v.punishment_for_incorrect_timing and not v.licked_this_window___:
            v.add_punishment___=True

    if(event=='pump_1_on'):
        if(not v.pump_1_bool___):
            pump_1.on()
            v.pump_1_bool___=True
            set_timer('pump_1_off',v.pump_duration) #turn off pump after set duration
            
        
    if(event=='pump_1_off'):
        pump_1.off()
        v.pump_1_bool___=False

    if(event=='pump_2_on'):
        if(not v.pump_2_bool___):
            pump_2.on()
            v.pump_2_bool___=True
            set_timer('pump_2_off',v.pump_duration) #turn off pump after set duration
            
        
    if(event=='pump_2_off'):
        pump_2.off()
        v.pump_2_bool___=False

    if event=="laser_on":
        if v.laser_pulse_counter___<v.laser_number_of_pulses:
            v.laser_pulse_counter___+=1
            laser.on()
            set_timer("laser_off",v.laser_pulse_duration)
        else:
            v.laser_pulse_counter___=0

    if event=='laser_off':
        laser.off()
        set_timer("laser_on",v.laser_inter_pulse_interval)

    if (event=='speaker_off'):
        speaker.off()

    if event == 'stop_trial_pulse':
        trial_pulse.off()
        
    if (event=='end_trial'):
        #make sure all devices are off
        speaker.off()
        pump_1.off()
        pump_2.off() 
        wheel.off()
        laser.off()

        # print_variables()
        v.trial_counter___+=1

        #reset flags
        v.finished_startup___=False
        v.motors_stationary___=True
        v.motors_ready___=True
        v.licked_this_window___=False

        #if amount of trials is reached, end task
        #if amount of trials set to -1, will never stop automatically
        if v.trial_counter___!=v.number_of_trials:
            set_timer('start_trial_event',v.inter_trial_interval + v.add_punishment___*v.punishment_period)
            if v.add_punishment___:
                print("adding punishment period")
            v.add_punishment___=False
            goto_state('start_trial')
        else:
            stop_framework()
    if (event=='end_experiment'):
        stop_framework()
        

def run_end():
    print('total {} trials. reference material was presented {} times. mouse licked correctly {} times'.format(v.trial_counter___,v.correct_stimulus_counter___,v.correct_lick_counter___))
    #make sure all devices are off
    return_home()
    speaker.off()
    pump_1.off()
    pump_2.off() 
    wheel.off()
    recording_trigger.off()
    print("stopped recording")
    print_variables()
    if v.correct_stimulus_counter___!=0:
        print("success rate: " +str(v.correct_lick_counter___/v.correct_stimulus_counter___*100)+"%")