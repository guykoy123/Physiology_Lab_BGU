try:
    from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
    from source.gui.custom_controls_dialog import Text_var,Spin_var,Slider_var,Checkbox_var
    from source.gui.settings import get_setting
except AttributeError as e:
    print(e)
try:

    TITLE = "T1 controls validation"
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

            self.number_of_trials=Text_var(init_var_dict=init_vars,label="<b>Number of trials:</b><br>(-1 run trials indefinitely)",varname="number_of_trials",text_width=INPUT_WIDTH )
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
            self.water_beep_frequency=Spin_var(init_vars,"Water beep frequency[Hz]:",1,10000,1,"water_beep_frequency")
            self.water_beep_frequency.add_to_grid(controls_layout,row)
            self.water_beep_frequency.setBoard(board)
            row+=1


            controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
            row += 1
            controls_layout.addWidget(QtWidgets.QLabel("<b>Trial structure:</b> <br>(all delays are calculated from start of trial)"), row, 0, 1, 4)
            row += 1

            #wheel timing
            self.delay_to_start_wheel=Spin_var(init_var_dict=init_vars,label="Delay to start wheel:",spin_min=1,spin_max=100000,step=1,varname="delay_to_start_wheel")
            self.delay_to_start_wheel.add_to_grid(controls_layout,row)
            self.delay_to_start_wheel.setBoard(board)
            row+=1

            self.wheel_delay_offset=Spin_var(init_var_dict=init_vars,label="Wheel delay offset:",spin_min=1,spin_max=100,step=1,varname="wheel_delay_offset")
            self.wheel_delay_offset.add_to_grid(controls_layout,row)
            self.wheel_delay_offset.setBoard(board)
            row+=1


            ##### water timing #####
            self.delay_for_water_after_trial_start=Spin_var(init_var_dict=init_vars,label="Delay to give water:",spin_min=1,spin_max=100000,step=1,varname="delay_for_water_after_trial_start")
            self.delay_for_water_after_trial_start.add_to_grid(controls_layout,row)
            self.delay_for_water_after_trial_start.setBoard(board)
            row+=1

            self.pump_duration=Spin_var(init_vars,"Pump duration:",1,500,1,"pump_duration")
            self.pump_duration.add_to_grid(controls_layout,row)
            self.pump_duration.setBoard(board)
            row+=1

            ##### stimulus timing #####
            self.stimulus_time_window=Spin_var(init_vars,"Stimulus time window:<br>(duration of stimulus in whisking range)",1,10000,1,"stimulus_time_window")
            self.stimulus_time_window.add_to_grid(controls_layout,row)
            self.stimulus_time_window.setBoard(board)
            row+=1

            self.stimulus_delay_from_start=Spin_var(init_vars,"Stimulus delay from start:",1,20000,1,"stimulus_delay_from_start_of_trial")
            self.stimulus_delay_from_start.add_to_grid(controls_layout,row)
            self.stimulus_delay_from_start.setBoard(board)
            row+=1

            ##### trial timing #####
            self.trial_duration=Spin_var(init_var_dict=init_vars,label="Trial duration:",spin_min=1,spin_max=100000,step=1,varname="trial_duration")
            self.trial_duration.add_to_grid(controls_layout,row)
            self.trial_duration.setBoard(board)
            row+=1
            
            self.inter_trial_interval=Spin_var(init_var_dict=init_vars,label="Inter trial interval:",spin_min=1,spin_max=100000,step=1,varname="inter_trial_interval")
            self.inter_trial_interval.add_to_grid(controls_layout,row)
            self.inter_trial_interval.setBoard(board)
            row+=1
            

            controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
            row += 1
            controls_layout.addWidget(QtWidgets.QLabel("<b>Stimulus positioning:</b>"), row, 0, 1, 4)
            row += 1

            ##### correct stimulus variables #####
            self.stimulus_x_value=Spin_var(init_var_dict=init_vars,label="Stimulus X coordinate:",spin_min=1,spin_max=4800,step=1,varname="stimulus_x_value")
            self.stimulus_x_value.add_to_grid(controls_layout,row)
            self.stimulus_x_value.setBoard(board)
            row+=1

            self.stimulus_y_value=Spin_var(init_var_dict=init_vars,label="Stimulus Y coordinate:",spin_min=1,spin_max=4800,step=1,varname="stimulus_y_value")
            self.stimulus_y_value.add_to_grid(controls_layout,row)
            self.stimulus_y_value.setBoard(board)
            row+=1

            self.stimulus_z_value=Spin_var(init_var_dict=init_vars,label="Stimulus Z coordinate:",spin_min=1,spin_max=4800,step=1,varname="stimulus_z_value")
            self.stimulus_z_value.add_to_grid(controls_layout,row)
            self.stimulus_z_value.setBoard(board)
            row+=1
            
            ##### outer bounds variables #####
            controls_layout.addWidget(QtWidgets.QLabel("Outer bounds are the area where the stimulus moves to after being in whisking range<br>(waiting between trials) <br> The stimulus X/Y/Z coordinates can't be inside the bounds.<br> Written in format (start_position,end_position)"), row, 0, 1, 4)
            row += 1

            self.stimulus_x_outer_bounds = Text_var(init_vars, "Stimulus X outer bounds:", "stimulus_x_outer_bounds", text_width=INPUT_WIDTH)
            self.stimulus_x_outer_bounds.add_to_grid(controls_layout, row)
            self.stimulus_x_outer_bounds.setBoard(board)
            row += 1

            self.stimulus_y_outer_bounds = Text_var(init_vars, "Stimulus Y outer bounds:", "stimulus_y_outer_bounds", text_width=INPUT_WIDTH)
            self.stimulus_y_outer_bounds.add_to_grid(controls_layout, row)
            self.stimulus_y_outer_bounds.setBoard(board)
            row += 1

            self.stimulus_z_outer_bounds = Text_var(init_vars, "Stimulus Z outer bounds:", "stimulus_z_outer_bounds", text_width=INPUT_WIDTH)
            self.stimulus_z_outer_bounds.add_to_grid(controls_layout, row)
            self.stimulus_z_outer_bounds.setBoard(board)
            row += 1


            self.create_validators()



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


        def create_validators(self):
            def position_validator():
                """
                check that correct stimulus position does not fall in the outer bounds range
                """
                #pull correct position values
                stimulus_x_value=eval(self.stimulus_x_value.spn.text())
                stimulus_y_value=eval(self.stimulus_y_value.spn.text())
                stimulus_z_value=eval(self.stimulus_z_value.spn.text())

                #pull outer bounds values (automatically parses into tuple type)
                stimulus_x_outer_bounds=eval(self.stimulus_x_outer_bounds.line_edit.text())
                stimulus_y_outer_bounds=eval(self.stimulus_y_outer_bounds.line_edit.text())
                stimulus_z_outer_bounds=eval(self.stimulus_z_outer_bounds.line_edit.text())

                #validate bounds are withing legal values (0-4800)
                if stimulus_x_outer_bounds[0]<0 or stimulus_x_outer_bounds[1]>4800 or type(stimulus_x_outer_bounds[0])!=int or type(stimulus_x_outer_bounds[1])!=int or stimulus_x_outer_bounds[1]<stimulus_x_outer_bounds[0]:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("Stimulus outer bounds have to be integers withing range 0-4800.<br>Start position must be less then or equal to end position")
                    msg.exec()
                    return
                if stimulus_y_outer_bounds[0]<0 or stimulus_y_outer_bounds[1]>4800 or type(stimulus_y_outer_bounds[0])!=int or type(stimulus_y_outer_bounds[1])!=int or stimulus_y_outer_bounds[1]<stimulus_y_outer_bounds[0]:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("Stimulus outer bounds have to be integers withing range 0-4800.<br>Start position must be less then or equal to end position")
                    msg.exec()
                    return
                if stimulus_z_outer_bounds[0]<0 or stimulus_z_outer_bounds[1]>4800 or type(stimulus_z_outer_bounds[0])!=int or type(stimulus_z_outer_bounds[1])!=int or stimulus_z_outer_bounds[1]<stimulus_z_outer_bounds[0]:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("Stimulus outer bounds have to be integers withing range 0-4800.<br>Start position must be less then or equal to end position")
                    msg.exec()
                    return
                
                #validate correct position is outside the outer bounds
                if stimulus_x_outer_bounds[0]<=stimulus_x_value and stimulus_x_outer_bounds[1]>=stimulus_x_value:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("stimulus correct position can't be withing the outer bounds range")
                    msg.exec()
                    return
                if stimulus_y_outer_bounds[0]<=stimulus_y_value and stimulus_y_outer_bounds[1]>=stimulus_y_value:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("stimulus correct position can't be withing the outer bounds range")
                    msg.exec()
                    return
                if stimulus_z_outer_bounds[0]<=stimulus_z_value and stimulus_z_outer_bounds[1]>=stimulus_z_value:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("stimulus correct position can't be withing the outer bounds range")
                    msg.exec()
                    return

                self.stimulus_x_value.set()
                self.stimulus_y_value.set()
                self.stimulus_z_value.set()

                self.stimulus_x_outer_bounds.set()
                self.stimulus_y_outer_bounds.set()
                self.stimulus_z_outer_bounds.set()



            def sound_validator():
                """
                check that start beep and water beep are different from each other
                """
                start_beep_freq=eval(self.start_beep_frequency.spn.text())
                water_beep_freq=eval(self.water_beep_frequency.spn.text())

                if abs(start_beep_freq-water_beep_freq)<100:
                    msg=QtWidgets.QMessageBox()
                    msg.setText("Start and water frequencies have to be at least 100Hz apart")
                    msg.exec()
                    return
                
                #save variable values because they are valid
                self.start_beep_frequency.set()
                self.water_beep_frequency.set()


            def trial_timing_validator():
                """
                check that wheel delay does not take longer then the length of the trial
                check that water delay and pump duration do not take longer then the length of the trial
                """
                #pull variable values
                trial_duration = eval(self.trial_duration.spn.text())
                delay_to_start_wheel=eval(self.delay_to_start_wheel.spn.text())
                delay_for_water=eval(self.delay_for_water_after_trial_start.spn.text())
                pump_duration=eval(self.pump_duration.spn.text())

                #validate the wheel spinning plus delay fit in duration
                if delay_to_start_wheel>trial_duration:
                    msg=QtWidgets.QMessageBox()
                    msg.setText("Delay to start wheel must be <= of trial duration")
                    msg.exec()
                    return
                
                if delay_for_water+pump_duration>trial_duration:
                    msg=QtWidgets.QMessageBox()
                    msg.setText("Delay for water + pump duration must be <= of trial duration")
                    msg.exec()
                    return
                
                #save variable values because they are valid
                self.delay_to_start_wheel.set()
                self.trial_duration.set()
                self.delay_for_water_after_trial_start.set()
                self.pump_duration.set()
            
            ##### trial structure and timing variables #####
            self.trial_duration.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.trial_duration.set_btn.clicked.connect(trial_timing_validator)

            self.delay_to_start_wheel.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.delay_to_start_wheel.set_btn.clicked.connect(trial_timing_validator)

            self.delay_for_water_after_trial_start.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.delay_for_water_after_trial_start.set_btn.clicked.connect(trial_timing_validator)

            self.pump_duration.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.pump_duration.set_btn.clicked.connect(trial_timing_validator)

            ##### sound variables #####
            self.start_beep_frequency.set_btn.clicked.disconnect()
            self.start_beep_frequency.set_btn.clicked.connect(sound_validator)

            self.start_beep_frequency.set_btn.clicked.disconnect()
            self.start_beep_frequency.set_btn.clicked.connect(sound_validator)

            ##### stimulus position variables #####
            self.stimulus_x_value.set_btn.clicked.disconnect()
            self.stimulus_x_value.set_btn.clicked.connect(position_validator)

            self.stimulus_y_value.set_btn.clicked.disconnect()
            self.stimulus_y_value.set_btn.clicked.connect(position_validator)

            self.stimulus_z_value.set_btn.clicked.disconnect()
            self.stimulus_z_value.set_btn.clicked.connect(position_validator)
            # connect the validator to the line edit and set button
            self.stimulus_x_outer_bounds.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.stimulus_x_outer_bounds.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.stimulus_x_outer_bounds.line_edit.returnPressed.connect(position_validator)
            self.stimulus_x_outer_bounds.set_btn.clicked.connect(position_validator)

            self.stimulus_y_outer_bounds.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.stimulus_y_outer_bounds.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.stimulus_y_outer_bounds.line_edit.returnPressed.connect(position_validator)
            self.stimulus_y_outer_bounds.set_btn.clicked.connect(position_validator)

            self.stimulus_z_outer_bounds.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.stimulus_z_outer_bounds.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.stimulus_z_outer_bounds.line_edit.returnPressed.connect(position_validator)
            self.stimulus_z_outer_bounds.set_btn.clicked.connect(position_validator)

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