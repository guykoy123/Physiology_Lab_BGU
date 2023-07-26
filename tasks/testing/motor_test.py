from pyControl.utility import *
from devices import *

board = Breakout_1_2()
motor = Stepper_motor(board.port_4)

states = ['return_home','stop']
initial_state='return_home'
events=['returned_home','test']
def return_home(event):
    motor.forward(1000,4800)
   
    timed_goto_state('stop',6000*ms)


def stop(event):
    stop_framework()
