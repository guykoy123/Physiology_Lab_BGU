from pyControl.utility import *
from devices import *

# States and events.
states = ["state_a"]
events = []

initial_state = "state_a"

# Variables
v.positions = [0, 1, 2, 3, 4]
v.position_probability_list = [0.2, 0.2, 0.2, 0.2, 0.2]

v.var_a = False
v.var_b = "hello"
v.var_c = 1.0


# Custom controls dialog declaration
v.custom_controls_dialog = "validation_gui"  # advanced example dialog that is loaded from a .py file


# State behaviour functions.
def state_a(event):
    if event == "entry":
        pass
