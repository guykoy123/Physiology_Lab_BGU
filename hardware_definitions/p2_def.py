from devices import *

board = Breakout_1_2()
speaker = Audio_board(board.port_4) # Instantiate audio board.
pump = Digital_output(pin = board.BNC_2)
wheel = Digital_output(pin = board.BNC_1)