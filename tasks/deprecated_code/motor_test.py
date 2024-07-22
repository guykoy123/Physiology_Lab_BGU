from pyControl.utility import *
from devices import *

board = Breakout_1_2()
motor_z = Stepper_motor(board.port_2)
motor_y = Stepper_motor(port = board.port_5)
motor_x = Stepper_motor(port = board.port_6)

states = ['return_home','stop']
initial_state='return_home'
events=['returned_home','test']
def return_home(event):
    motor_z.forward(1500,4800)
    motor_y.forward(1500,4000)
    motor_x.forward(1500,2000)
    timed_goto_state('stop',6000*ms)


def stop(event):
    stop_framework()
