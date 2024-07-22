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
wheel = Digital_output(pin = board.DAC_2)
sync_output = Rsync(pin=board.BNC_1,event_name="pulse",pulse_dur=300) #needs to be a digital input on the intan system
recording_trigger = Digital_output(pin = board.DAC_1) #needs to be a digital input on the intan system
port_exp = Port_expander(port = board.port_3)
motor1 = Stepper_motor(port = port_exp.port_1)

#public variables
v.volume = 50 #speaker volume
v.frequency = 2000 #start tone frequency
v.delay = 900 #delay from start of trial to start of wheel turn
v.delay_offset = 10 #percetage of offset from original value to randomize values
v.pump_duration=300*ms #pump duration for button press


#private variables
v.finished_startup___ = False
v.pump_bool___=False

states = ['forward','backward']
initial_state = 'forward'
events = ['speaker_off','start_walking','pump_off','button_press','pulse']

def forward(event):  
    motor1.forward(step_rate=100)
    timed_goto_state("backward",1000)
def backward(event):
    motor1.backward(step_rate=100)
    timed_goto_state("forward",1000)


# def variable_validation():
#     """
#     runs validations on all public variables of the task
#     """
#     valid_flag=True
    
#     if not isinstance(v.number_of_trials,int) or v.number_of_trials<-1:
#         valid_flag=False
#         print("number_of_trials has to be an integer larger or equal to -1")
#     if not isinstance(v.beep_volume,int) or v.beep_volume>100 or v.beep_volume<1:
#         valid_flag=False
#         print("beep_volume has to be an integer between 1 and 127")
#     if not isinstance(v.start_beep_frequency,int) or v.start_beep_frequency>6000 or v.start_beep_frequency<1:
#         valid_flag=False
#         print("start_beep_frequency has to be an integer between 1 and 6000 [Hz]")
#     if not isinstance(v.water_beep_frequency,int) or v.water_beep_frequency>6000 or v.water_beep_frequency<1:
#         valid_flag=False
#         print("water_beep_frequency has to be an integer between 1 and 6000 [Hz]")
#     if not isinstance(v.delay_to_start_wheel ,int) or v.delay_to_start_wheel <0:
#         valid_flag=False
#         print("delay_to_start wheel has to be an integer larger or equal to 0")
#     if not isinstance(v.wheel_delay_offset ,int) or v.wheel_delay_offset <0:
#         valid_flag=False
#         print("wheel_delay_offset has to be an integer larger or equal to 0")
#     if not isinstance(v.pump_duration ,int) or v.pump_duration <0:
#         valid_flag=False
#         print("wheel_delay_offset has to be an integer larger or equal to 0")
#     if not isinstance(v.stimulus_time_window ,int) or v.stimulus_time_window <0:
#         valid_flag=False
#         print("stimulus_time_window has to be an integer larger or equal to 0")
#     if not isinstance(v.stimulus_motor_speed ,int) or v.stimulus_motor_speed >1500 or v.stimulus_motor_speed <1:
#         valid_flag=False
#         print("stimulus_motor_speed has to be an integer between 1 and 1500")
#     if not isinstance(v.inter_trial_interval ,int) or v.inter_trial_interval <0:
#         valid_flag=False
#         print("inter_trial_interval has to be an integer larger or equal to 0")
#     if not isinstance(v.correct_stimulus_x_value, int) or v.correct_stimulus_x_value>4800 or v.correct_stimulus_x_value<0:
#         valid_flag=False
#         print("correct_stimulus_x_value has to be an integer between 0 and 4800")
#     if not isinstance(v.correct_stimulus_y_value, int) or v.correct_stimulus_y_value>4800 or v.correct_stimulus_y_value<0:
#         valid_flag=False
#         print("correct_stimulus_y_value has to be an integer between 0 and 4800")
#     if not isinstance(v.correct_stimulus_z_value, int) or v.correct_stimulus_z_value>4800 or v.correct_stimulus_z_value<0:
#         valid_flag=False
#         print("correct_stimulus_z_value has to be an integer between 0 and 4800")
    
#     #check stimulus offset lists
#     catch_trial_position_flag=False #check that catch trial position does not align with other positions
#     if len( v.x_stimulus_offset)== len( v.y_stimulus_offset) and len( v.y_stimulus_offset)==len( v.z_stimulus_offset):
#         for  i in range(v.x_stimulus_offset):
#             #check that all offset values are integers and when summing with correct value it stays within allowed range
#             x=v.x_stimulus_offset[i] + v.correct_stimulus_x_value
#             if x<0 or x>4800 or  isinstance(v.x_stimulus_offset,int):
#                 valid_flag=False
#                 break
#             elif x==v.catch_trial_x_position:
#                 catch_trial_position_flag=True
#             y=v.y_stimulus_offset[i] + v.correct_stimulus_y_value
#             if y<0 or y>4800 or  isinstance(v.y_stimulus_offset,int):
#                 valid_flag=False
#                 break
#             elif y==v.catch_trial_y_position:
#                 catch_trial_position_flag=True
#             z=v.z_stimulus_offset[i] + v.correct_stimulus_z_value
#             if z<0 or z>4800 or  isinstance(v.z_stimulus_offset,int):
#                 valid_flag=False
#                 break
#             elif z==v.catch_trial_z_position:
#                 catch_trial_position_flag=True
#         if not valid_flag:
#             print("x/y/z_stimulus_offset + correct_stimulus_x/y/z_value has to be and integer withing allowed range (0-4800)")
#     else:
#         valid_flag=False
#         print("x/y/z_stimulus_offset lists have to be the same length")
    
#     #check that position probabilities line up with number of positions
#     # and that the sum is 1
#     if len(v.position_probability_list)-1!= len(v.y_stimulus_offset):
#         valid_flag=False
#         print("position_probability_list need to be of length 1 + length of x_stimulus_offset list")
#     if sum(v.position_probability_list)!=1:
#         print("position_probability_list does not sum up to 1")
#         valid_flag=False
    
#     #check that catch trial stimulus position is withing allowed range
#     if not isinstance(v.catch_trial_x_position ,int) or v.catch_trial_x_position >4800 or v.catch_trial_x_position <0:
#         valid_flag=False
#         print("catch_trial_x_position has to be an integer between 0 and 4800")
#     if not isinstance(v.catch_trial_y_position ,int) or v.catch_trial_y_position >4800 or v.catch_trial_y_position <0:
#         valid_flag=False
#         print("catch_trial_y_position has to be an integer between 0 and 4800")
#     if not isinstance(v.catch_trial_z_position ,int) or v.catch_trial_z_position >4800 or v.catch_trial_z_position <0:
#         valid_flag=False
#         print("catch_trial_z_position has to be an integer between 0 and 4800")
    
#     #check that catch trial positions are valid
#     if catch_trial_position_flag:
#         valid_flag=False
#         print("catch_trial_x/y/z_position can't line up with other positions")

#     if not isinstance(v.probability_of_catch_trial,(int,float)) or v.probability_of_catch_trial<0 or  v.probability_of_catch_trial>1:
#         valid_flag=False
#         print("probability_of_catch_trial has to be a number between 0 and 1")
    
#     #check stimulus outer bounds
#     #check tuples of length 2
#     if not isinstance(v.stimulus_x_outer_bounds,tuple) or len(v.stimulus_x_outer_bounds)!=2:
#         valid_flag=False
#         print("stimulus_x_outer_bounds has to be a tuple of length 2")
#     if not isinstance(v.stimulus_y_outer_bounds,tuple) or len(v.stimulus_y_outer_bounds)!=2:
#         valid_flag=False
#         print("stimulus_y_outer_bounds has to be a tuple of length 2")
#     if not isinstance(v.stimulus_z_outer_bounds,tuple) or len(v.stimulus_z_outer_bounds)!=2:
#         valid_flag=False
#         print("stimulus_z_outer_bounds has to be a tuple of length 2")
    
#     #check values of tuples are valid
#     if not isinstance(v.stimulus_x_outer_bounds[0],int) or not isinstance(v.stimulus_x_outer_bounds[1],int) or v.stimulus_x_outer_bounds[0]<0 or v.stimulus_x_outer_bounds[0]>v.stimulus_x_outer_bounds[1] or v.stimulus_x_outer_bounds[1]>4800:
#         valid_flag=False
#         print("stimulus_x_outer_bounds has to be 2 integer values 0<first values<second value<4800")
#     if not isinstance(v.stimulus_y_outer_bounds[0],int) or not isinstance(v.stimulus_y_outer_bounds[1],int) or v.stimulus_y_outer_bounds[0]<0 or v.stimulus_y_outer_bounds[0]>v.stimulus_y_outer_bounds[1] or v.stimulus_y_outer_bounds[1]>4800:
#         valid_flag=False
#         print("stimulus_y_outer_bounds has to be 2 integer values 0<first values<second value<4800")
#     if not isinstance(v.stimulus_z_outer_bounds[0],int) or not isinstance(v.stimulus_z_outer_bounds[1],int) or v.stimulus_z_outer_bounds[0]<0 or v.stimulus_z_outer_bounds[0]>v.stimulus_z_outer_bounds[1] or v.stimulus_z_outer_bounds[1]>4800:
#         valid_flag=False
#         print("stimulus_z_outer_bounds has to be 2 integer values 0<first values<second value<4800")
    
#     #check validity of punishment variables
#     if not isinstance(v.punishment_period,int) or v.punishment_period<0:
#         valid_flag=False
#         print("punishment_period has to be an integer larger or equal to 0")
#     if not isinstance(v.punishment_for_incorrect_timing,bool):
#         valid_flag=False
#         print("punishment_for_incorrect_timing has to be a boolean value")
#     if not isinstance(v.punishment_for_incorrect_stimulus,bool):
#         valid_flag=False
#         print("punishment_for_incorrect_stimulus has to be a boolean value")

#     if  not valid_flag:
#         stop_framework()
