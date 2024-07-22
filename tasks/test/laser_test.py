from pyControl.utility import *
from devices import *

board = Breakout_1_2()
port_exp = Port_expander(port = board.port_3)
laser=Digital_output(pin = port_exp.port_2.DIO_B)

v.number_of_pulses=1
v.pulse_duration=10
v.inter_pulse_interval=100
v.started___=False
states = ['main_loop']
initial_state = 'main_loop'
events=['turn_on','turn_off']
def main_loop(event):
    if not v.started___:
        v.started___=True
        publish_event('turn_on')
    if event=='turn_on':
        laser.on()
        v.number_of_pulses-=1
        set_timer('turn_off',v.pulse_duration)
    elif event=='turn_off':
        laser.off()
        if v.number_of_pulses>0:
            set_timer('turn_on',v.inter_pulse_interval)        
        else:
            stop_framework()