from devices import *

board = Breakout_1_2()
speaker = Audio_board(board.port_4) # Instantiate audio board.
 # Instantiate lickometer. used as water button in p1
lickometer = Lickometer(port=board.port_2,debounce=100,rising_event_A='press', falling_event_A='press_off')
pump = Digital_output(pin = board.BNC_2)
wheel = Digital_output(pin = board.BNC_1)