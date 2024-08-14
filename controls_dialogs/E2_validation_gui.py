try:
    from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
    from source.gui.custom_controls_dialog import Text_var,Spin_var,Slider_var,Checkbox_var
    from source.gui.settings import get_setting
except AttributeError as e:
    print(e)
try:

    TITLE = "E2 controls validation"
    INPUT_WIDTH = 200


    # Custom Variable dialog
    class Custom_controls_dialog(QtWidgets.QDialog):
        # Dialog for setting and getting task variables.
        def __init__(self, parent, board):
            super(QtWidgets.QDialog, self).__init__(parent)
            self.setWindowTitle(TITLE)
            self.layout = QtWidgets.QVBoxLayout(self)
            self.controls_grid = Controls_grid(self, board)
            self.layout.addWidget(self.controls_grid)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(self.layout)


    class Controls_grid(QtWidgets.QWidget):
        def __init__(self, parent, board):
            super(QtWidgets.QWidget, self).__init__(parent)
            variables = board.sm_info.variables
            self.grid_layout = QtWidgets.QGridLayout()
            initial_variables_dict = {v_name: v_value_str for (v_name, v_value_str) in sorted(variables.items())}
            self.controls_gui = Controls_gui(self, self.grid_layout, board, initial_variables_dict)
            self.setLayout(self.grid_layout)


    class Controls_gui(QtWidgets.QWidget):
        def __init__(self, parent, grid_layout, board, init_vars):
            super(QtWidgets.QWidget, self).__init__(parent)
            self.board = board

            # create widgets
            widget = QtWidgets.QWidget()
            controls_layout = QtWidgets.QGridLayout()
            row = 0

            self.number_of_trials=Text_var(init_var_dict=init_vars,label="<b>Number of trials:</b> (-1 run trials indefinitely)",varname="number_of_trials",text_width=INPUT_WIDTH )
            self.number_of_trials.add_to_grid(controls_layout,row)
            self.number_of_trials.setBoard(board)
            row+=1


            controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
            row += 1
            controls_layout.addWidget(QtWidgets.QLabel("<b>Sound controls:</b>"), row, 0, 1, 4)
            row += 1
            self.beep_volume=Spin_var(init_vars,"Beep Volume:",1,127,1,"beep_volume")
            self.beep_volume.add_to_grid(controls_layout,row)
            self.beep_volume.setBoard(board)
            row+=1
            self.start_beep_frequency=Spin_var(init_vars,"Start beep frequency[Hz]:",1,10000,1,"start_beep_frequency")
            self.start_beep_frequency.add_to_grid(controls_layout,row)
            self.start_beep_frequency.setBoard(board)
            row+=1


            ##### Laser controls #####
            controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
            row += 1
            controls_layout.addWidget(QtWidgets.QLabel("<b>Laser controls:</b>"), row, 0, 1, 4)
            row += 1
            self.laser_delay_from_start=Spin_var(init_var_dict=init_vars,label="Laser delay from start:",spin_min=1,spin_max=100000,step=1,varname="laser_delay_from_start")
            self.laser_delay_from_start.add_to_grid(controls_layout,row)
            self.laser_delay_from_start.setBoard(board)
            row+=1

            self.laser_number_of_pulses=Spin_var(init_var_dict=init_vars,label="Number of pulses:",spin_min=1,spin_max=1000,step=1,varname="laser_number_of_pulses")
            self.laser_number_of_pulses.add_to_grid(controls_layout,row)
            self.laser_number_of_pulses.setBoard(board)
            row+=1

            self.laser_pulse_duration=Spin_var(init_var_dict=init_vars,label="Pulse duration:",spin_min=1,spin_max=1000,step=1,varname="laser_pulse_duration")
            self.laser_pulse_duration.add_to_grid(controls_layout,row)
            self.laser_pulse_duration.setBoard(board)
            row+=1
            
            self.laser_inter_pulse_interval=Spin_var(init_var_dict=init_vars,label="Inter pulse interval:",spin_min=1,spin_max=1000,step=1,varname="laser_inter_pulse_interval")
            self.laser_inter_pulse_interval.add_to_grid(controls_layout,row)
            self.laser_inter_pulse_interval.setBoard(board)
            row+=1

            controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
            row += 1
            controls_layout.addWidget(QtWidgets.QLabel("<b>Trial structure:</b> <br>(all delays are calculated from start of trial)"), row, 0, 1, 4)
            row += 1

            self.pump_duration=Spin_var(init_vars,"Pump duration:",1,500,1,"pump_duration")
            self.pump_duration.add_to_grid(controls_layout,row)
            self.pump_duration.setBoard(board)
            row+=1
            
            self.time_between_trials=Spin_var(init_var_dict=init_vars,label="Time between trials:",spin_min=1,spin_max=100000,step=1,varname="time_between_trials")
            self.time_between_trials.add_to_grid(controls_layout,row)
            self.time_between_trials.setBoard(board)
            row+=1


            ##### events #####
            controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
            row += 1
            controls_layout.addWidget(QtWidgets.QLabel("<b>Events:</b><br>trigger start_trial_event to begin trials after making sure camera and intan systems are working properly."), row, 0, 1, 4)
            row += 1
            self.create_events_trigger_groupbox()
            controls_layout.addWidget(self.events_groupbox, row, 0, 1, 4)
            row += 1  

            # separator
            controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
            row += 1

            #if you want to add notes uncomment the following 3 lines
            self.create_notes_groupbox()
            controls_layout.addWidget(self.notes_groupbox, row, 0, 1, 4)
            row += 1

            controls_layout.setRowStretch(row, 1)
            widget.setLayout(controls_layout)
            grid_layout.addWidget(widget, 0, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

            # add close shortcut
            self.close_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self)
            self.close_shortcut.activated.connect(self.close)


    



        def create_events_trigger_groupbox(self):
            # Events groupbox.
            self.events_groupbox = QtWidgets.QGroupBox("Event trigger")
            self.eventsbox_layout = QtWidgets.QHBoxLayout(self.events_groupbox)
            self.trigger_event_lbl = QtWidgets.QLabel("Event:")
            self.event_select_combo = QtWidgets.QComboBox()
            self.event_select_combo.addItems(self.board.sm_info.events)
            self.trigger_event_button = QtWidgets.QPushButton("Trigger")
            self.trigger_event_button.clicked.connect(self.trigger_event)
            self.trigger_event_button.setDefault(False)
            self.trigger_event_button.setAutoDefault(False)
            self.eventsbox_layout.addWidget(self.trigger_event_lbl)
            self.eventsbox_layout.addWidget(self.event_select_combo)
            self.eventsbox_layout.addWidget(self.trigger_event_button)
            self.eventsbox_layout.addStretch(1)

        def create_notes_groupbox(self):
            # Notes groupbox
            self.notes_groupbox = QtWidgets.QGroupBox("Add note to log")
            self.notesbox_layout = QtWidgets.QGridLayout(self.notes_groupbox)
            self.notes_textbox = QtWidgets.QTextEdit()
            self.notes_textbox.setFixedHeight(get_setting("GUI", "log_font_size") * 4)
            self.notes_textbox.setFont(QtGui.QFont("Courier New", get_setting("GUI", "log_font_size")))
            self.note_button = QtWidgets.QPushButton("Add note")
            self.note_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            self.note_button.clicked.connect(self.add_note)
            self.notesbox_layout.addWidget(self.notes_textbox, 0, 0, 1, 2)
            self.notesbox_layout.addWidget(self.note_button, 1, 1)
            self.notesbox_layout.setColumnStretch(0, 1)

        def trigger_event(self):
            if self.board.framework_running:
                self.board.trigger_event(self.event_select_combo.currentText())

        def add_note(self):
            note_text = self.notes_textbox.toPlainText()
            self.notes_textbox.clear()
            self.board.data_logger.print_message(note_text, source="u")
except AttributeError as e:
    print(e)