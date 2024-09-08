try:
    from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
    from source.gui.custom_controls_dialog import Text_var,Spin_var,Slider_var,Checkbox_var
    from source.gui.settings import get_setting
except AttributeError as e:
    print(e)
try:

    TITLE = "T2 controls validation"
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


            ##### sound variables #####
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
            controls_layout.addWidget(QtWidgets.QLabel("<b>Trial structure [ms]:</b> <br>(all delays are calculated from start of trial)<br>When setting value be sure to consider at least 3 seconds of time for stimulus to move."), row, 0, 1, 4)
            row += 1

            ##### wheel timing #####
            self.delay_to_start_wheel=Spin_var(init_var_dict=init_vars,label="Delay to start wheel:",spin_min=1,spin_max=100000,step=1,varname="delay_to_start_wheel")
            self.delay_to_start_wheel.add_to_grid(controls_layout,row)
            self.delay_to_start_wheel.setBoard(board)
            row+=1

            self.wheel_delay_offset=Spin_var(init_var_dict=init_vars,label="Wheel delay offset[%]:",spin_min=1,spin_max=100,step=1,varname="wheel_delay_offset")
            self.wheel_delay_offset.add_to_grid(controls_layout,row)
            self.wheel_delay_offset.setBoard(board)
            row+=1

            self.wheel_spin_duration=Spin_var(init_var_dict=init_vars,label="Wheel spin duration:",spin_min=1,spin_max=100000,step=1,varname="wheel_spin_duration")
            self.wheel_spin_duration.add_to_grid(controls_layout,row)
            self.wheel_spin_duration.setBoard(board)
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

            ##### stimulus variables #####
            controls_layout.addWidget(QtWidgets.QLabel("<br>Positions list contains the coordinates for the correlated axis.<br>Format: [integer,integer,...]"), row, 0, 1, 4)
            row += 1
            
            self.x_stimulus_position = Text_var(init_vars, "Stimulus X position list:", "x_stimulus_position", text_width=INPUT_WIDTH)
            self.x_stimulus_position.add_to_grid(controls_layout, row)
            self.x_stimulus_position.setBoard(board)
            row += 1

            self.y_stimulus_position = Text_var(init_vars, "Stimulus Y position list:", "y_stimulus_position", text_width=INPUT_WIDTH)
            self.y_stimulus_position.add_to_grid(controls_layout, row)
            self.y_stimulus_position.setBoard(board)
            row += 1

            self.z_stimulus_position = Text_var(init_vars, "Stimulus Z position list:", "z_stimulus_position", text_width=INPUT_WIDTH)
            self.z_stimulus_position.add_to_grid(controls_layout, row)
            self.z_stimulus_position.setBoard(board)
            row += 1

            ##### Probability list #####
            controls_layout.addWidget(QtWidgets.QLabel("<br>The probability list gives probabilities of a certain position being used in a trial.<br>(in order of position list)<br>Total probabilities have to sum up to 1.<br>Format: [float,float,...]"), row, 0, 1, 4)
            row += 1

            self.position_probability_list = Text_var(init_vars, "Position probability list:", "position_probability_list", text_width=INPUT_WIDTH)
            self.position_probability_list.add_to_grid(controls_layout, row)
            self.position_probability_list.setBoard(board)
            row += 1

            
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

                #pull position list values
                x_stimulus_position=eval(self.x_stimulus_position.line_edit.text())
                y_stimulus_position=eval(self.y_stimulus_position.line_edit.text())
                z_stimulus_position=eval(self.z_stimulus_position.line_edit.text())

                #pull outer bounds values (automatically parses into tuple type)
                stimulus_x_outer_bounds=eval(self.stimulus_x_outer_bounds.line_edit.text())
                stimulus_y_outer_bounds=eval(self.stimulus_y_outer_bounds.line_edit.text())
                stimulus_z_outer_bounds=eval(self.stimulus_z_outer_bounds.line_edit.text())

                #check that position lists are of the same length
                if not len(x_stimulus_position)==len(y_stimulus_position)==len(z_stimulus_position):
                    msg = QtWidgets.QMessageBox()
                    msg.setText("Position lists have to be of the same length")
                    msg.exec()
                    #set values because user might be in the process of inputting values
                    self.x_stimulus_position.set()
                    self.y_stimulus_position.set()
                    self.z_stimulus_position.set()
                    return
                


                #validate bounds are withing legal values (0-1700)
                if stimulus_x_outer_bounds[0]<0 or stimulus_x_outer_bounds[1]>1700 or type(stimulus_x_outer_bounds[0])!=int or type(stimulus_x_outer_bounds[1])!=int or stimulus_x_outer_bounds[1]<stimulus_x_outer_bounds[0]:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("Stimulus outer bounds have to be integers withing range 0-1700.<br>Start position must be less then or equal to end position")
                    msg.exec()
                    return
                if stimulus_y_outer_bounds[0]<0 or stimulus_y_outer_bounds[1]>1700 or type(stimulus_y_outer_bounds[0])!=int or type(stimulus_y_outer_bounds[1])!=int or stimulus_y_outer_bounds[1]<stimulus_y_outer_bounds[0]:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("Stimulus outer bounds have to be integers withing range 0-1700.<br>Start position must be less then or equal to end position")
                    msg.exec()
                    return
                if stimulus_z_outer_bounds[0]<0 or stimulus_z_outer_bounds[1]>1700 or type(stimulus_z_outer_bounds[0])!=int or type(stimulus_z_outer_bounds[1])!=int or stimulus_z_outer_bounds[1]<stimulus_z_outer_bounds[0]:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("Stimulus outer bounds have to be integers withing range 0-1700.<br>Start position must be less then or equal to end position")
                    msg.exec()
                    return
                
                #get minimum values for each axis (from all positions)
                #while also checking that offset+correct_position is withing legal bounds of the axis
                x_min=1700
                for i in range(len(x_stimulus_position)):
                    new_val=x_stimulus_position[i]
                    x_min=min(x_min,new_val)
                    if new_val<0 or new_val>1700:
                        msg = QtWidgets.QMessageBox()
                        msg.setText("Position value value must be within 0-1700 range.<br>Found problem in x position list in position " + str(i))
                        msg.exec()
                        return
                y_min=1700
                for i in range(len(y_stimulus_position)):
                    new_val=y_stimulus_position[i]
                    y_min=min(y_min,new_val)
                    if new_val<0 or new_val>1700:
                        msg = QtWidgets.QMessageBox()
                        msg.setText("Position value value must be within 0-1700 range.<br>Found problem in y position list in position " + str(i))
                        msg.exec()
                        return
                z_min=1700
                for i in range(len(z_stimulus_position)):
                    new_val=z_stimulus_position[i]
                    z_min=min(z_min,new_val)
                    if new_val<0 or new_val>1700:
                        msg = QtWidgets.QMessageBox()
                        msg.setText("Position value value must be within 0-1700 range.<br>Found problem in z position list in position " + str(i))
                        msg.exec()
                        return

                #validate positions are outside the outer bounds
                if stimulus_x_outer_bounds[1]>x_min:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("stimulus positions can't be withing the outer bounds range")
                    msg.exec()
                    return
                if stimulus_y_outer_bounds[1]>y_min:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("stimulus positions can't be withing the outer bounds range")
                    msg.exec()
                    return
                if stimulus_z_outer_bounds[1]>z_min:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("stimulus positions can't be withing the outer bounds range")
                    msg.exec()
                    return

                self.stimulus_x_outer_bounds.set()
                self.stimulus_y_outer_bounds.set()
                self.stimulus_z_outer_bounds.set()

                self.x_stimulus_position.set()
                self.y_stimulus_position.set()
                self.z_stimulus_position.set()




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
                check that wheel delay does not take longer than the length of the trial
                check that water delay and pump duration do not take longer than the length of the trial
                """
                #pull variable values
                trial_duration = eval(self.trial_duration.spn.text())
                delay_to_start_wheel=eval(self.delay_to_start_wheel.spn.text())
                delay_for_water=eval(self.delay_for_water_after_trial_start.spn.text())
                pump_duration=eval(self.pump_duration.spn.text())
                wheel_spin_duration = eval(self.wheel_spin_duration.spn.text())
                stimulus_delay_from_start = eval(self.stimulus_delay_from_start.spn.text())
                stimulus_time_window = eval(self.stimulus_time_window.spn.text())

                #validate the wheel spinning plus delay fit in duration
                if delay_to_start_wheel+wheel_spin_duration>trial_duration:
                    msg=QtWidgets.QMessageBox()
                    msg.setText("Delay to start wheel + wheel spin duration must be <= of trial duration")
                    msg.exec()
                    return
                
                if delay_for_water+pump_duration>trial_duration:
                    msg=QtWidgets.QMessageBox()
                    msg.setText("Delay for water + pump duration must be <= of trial duration")
                    msg.exec()
                    return
                
                if stimulus_delay_from_start+stimulus_time_window+3000 > trial_duration:
                    msg=QtWidgets.QMessageBox()
                    msg.setText("stimulus delay + stimulus time window + 3sec must be <= of trial duration")
                    msg.exec()
                    return
                
                #save variable values because they are valid
                self.delay_to_start_wheel.set()
                self.trial_duration.set()
                self.delay_for_water_after_trial_start.set()
                self.pump_duration.set()
                self.stimulus_delay_from_start.set()
                self.stimulus_time_window.set()

            def probability_validator():
                """
                checks probabilities sum to 1 and that every position has a corresponding probability
                """
                #pull probability list
                position_probability_list=eval(self.position_probability_list.line_edit.text())

                #run through values making sure the're floats that sum to 1
                sum=0
                for i in range(len(position_probability_list)):
                    if position_probability_list[i]<=1 and (type(position_probability_list[i])==float or type(position_probability_list[i])==int) :
                        sum+=position_probability_list[i]
                    else:
                        msg=QtWidgets.QMessageBox()
                        msg.setText("Probabilities have to be numbers less than or equal to 1 and in float format.<br>Problem with number in position "+str(i))
                        msg.exec()
                        return
                if sum!=1:
                    msg=QtWidgets.QMessageBox()
                    msg.setText("Probabilities have to sum to 1")
                    msg.exec()
                    return
                if len(position_probability_list) != len(eval(self.x_stimulus_position.line_edit.text())):
                    msg=QtWidgets.QMessageBox()
                    msg.setText("Length of probabilities list has to match number of positions.")
                    msg.exec()
                    return
                
                self.position_probability_list.set()


            ##### trial structure and timing variables #####
            self.trial_duration.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.trial_duration.set_btn.clicked.connect(trial_timing_validator)

            self.delay_to_start_wheel.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.delay_to_start_wheel.set_btn.clicked.connect(trial_timing_validator)

            self.delay_for_water_after_trial_start.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.delay_for_water_after_trial_start.set_btn.clicked.connect(trial_timing_validator)

            self.pump_duration.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.pump_duration.set_btn.clicked.connect(trial_timing_validator)
            
            self.stimulus_delay_from_start.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.stimulus_delay_from_start.set_btn.clicked.connect(trial_timing_validator)

            self.stimulus_time_window.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.stimulus_time_window.set_btn.clicked.connect(trial_timing_validator)


            ##### sound variables #####
            self.start_beep_frequency.set_btn.clicked.disconnect()
            self.start_beep_frequency.set_btn.clicked.connect(sound_validator)

            self.start_beep_frequency.set_btn.clicked.disconnect()
            self.start_beep_frequency.set_btn.clicked.connect(sound_validator)

            ##### stimulus position variables #####
            self.x_stimulus_position.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.x_stimulus_position.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.x_stimulus_position.line_edit.returnPressed.connect(position_validator)
            self.x_stimulus_position.set_btn.clicked.connect(position_validator)

            self.y_stimulus_position.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.y_stimulus_position.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.y_stimulus_position.line_edit.returnPressed.connect(position_validator)
            self.y_stimulus_position.set_btn.clicked.connect(position_validator)

            self.z_stimulus_position.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.z_stimulus_position.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.z_stimulus_position.line_edit.returnPressed.connect(position_validator)
            self.z_stimulus_position.set_btn.clicked.connect(position_validator)

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

            
            ##### probability list #####
            self.position_probability_list.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.position_probability_list.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.position_probability_list.line_edit.returnPressed.connect(probability_validator)
            self.position_probability_list.set_btn.clicked.connect(probability_validator)

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