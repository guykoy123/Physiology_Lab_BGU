"""
this task allows control over each motor separately
lab worker will input position in each axis in the variables window and set the new values
then the lab worker must trigger the move event to move the motors to position
return home event will make sure motors move to zero position even if position variable has incorrect data
"""

from pyControl.utility import *
from devices import *

board = Breakout_1_2()
motor_z = Stepper_motor(board.port_2)
motor_y = Stepper_motor(port = board.port_5)
motor_x = Stepper_motor(port = board.port_6)

#public motor position variable, when different from private ones, move the motors
v.motor_z_position=0
v.motor_y_position=0
v.motor_x_position=0

v.motor_z_pos___=0
v.motor_y_pos___=0
v.motor_x_pos___=0

v.motors_stationary___=True

v.motor_speed = 1500

states = ['moved','main']
initial_state='main'
events=['move','wait','return home']

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


def main(event):
    if event=='move':
        if v.motors_stationary___:
            if v.motor_z_position != v.motor_z_pos___:
                wait_time = move_motor_into_position('z',v.motor_z_position)
                v.motors_stationary___=False
                set_timer('wait',wait_time)
            if v.motor_y_position != v.motor_y_pos___:
                wait_time = move_motor_into_position('y',v.motor_y_position)
                v.motors_stationary___=False
                set_timer('wait',wait_time)
            if v.motor_x_position != v.motor_x_pos___:
                print("hit")
                wait_time = move_motor_into_position('x',v.motor_x_position)
                v.motors_stationary___=False
                set_timer('wait',wait_time)
                
    if event=='wait':
        v.motors_stationary___=True
        print("motor in position")

    if event =='return home':
        motor_z.forward(1500,4800)
        motor_y.forward(1500,4800)
        motor_x.forward(1500,4800)
        set_timer('wait',6000*ms)

            










