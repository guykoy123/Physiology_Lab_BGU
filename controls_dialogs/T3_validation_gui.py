try:
    from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
    from source.gui.custom_controls_dialog import Text_var,Spin_var,Slider_var,Checkbox_var
    from source.gui.settings import get_setting
except AttributeError as e:
    print(e)
try:

    TITLE = "T3 controls validation"
    INPUT_WIDTH = 200


    # Custom Variable dialog
    class Custom_controls_dialog(QtWidgets.QDialog):
        # Dialog for setting and getting task variables.
        def __init__(self, parent, board):
            super(QtWidgets.QDialog, self).__init__(parent)
            self.setWindowTitle(TITLE)
            self.controls_grid = Controls_grid(self, board)

            ##### add scrollable area
            self.scroll_area = QtWidgets.QScrollArea(parent=self)
            self.scroll_area.setWidgetResizable(True)
            self.controls_grid = Controls_grid(self.scroll_area, board)
            self.scroll_area.setWidget(self.controls_grid)
            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.addWidget(self.scroll_area)

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
            controls_layout.addWidget(QtWidgets.QLabel("<b>Trial structure:</b> <br>(all delays are calculated from start of trial)"), row, 0, 1, 4)
            row += 1

            ##### wheel timing #####
            self.delay_to_start_wheel=Spin_var(init_var_dict=init_vars,label="Delay to start wheel:",spin_min=1,spin_max=100000,step=1,varname="delay_to_start_wheel")
            self.delay_to_start_wheel.add_to_grid(controls_layout,row)
            self.delay_to_start_wheel.setBoard(board)
            row+=1

            self.wheel_delay_offset=Spin_var(init_var_dict=init_vars,label="Wheel delay offset:",spin_min=1,spin_max=100,step=1,varname="wheel_delay_offset")
            self.wheel_delay_offset.add_to_grid(controls_layout,row)
            self.wheel_delay_offset.setBoard(board)
            row+=1


            ##### water timing #####
            self.pump_duration=Spin_var(init_vars,"Pump duration:",1,500,1,"pump_duration")
            self.pump_duration.add_to_grid(controls_layout,row)
            self.pump_duration.setBoard(board)
            row+=1

            ##### stimulus timing #####
            self.stimulus_time_window=Spin_var(init_vars,"Stimulus time window:<br>(duration of stimulus in whisking range)",1,10000,1,"stimulus_time_window")
            self.stimulus_time_window.add_to_grid(controls_layout,row)
            self.stimulus_time_window.setBoard(board)
            row+=1

            ##### trial timing #####          
            self.inter_trial_interval=Spin_var(init_var_dict=init_vars,label="Inter trial interval:",spin_min=1,spin_max=100000,step=1,varname="inter_trial_interval")
            self.inter_trial_interval.add_to_grid(controls_layout,row)
            self.inter_trial_interval.setBoard(board)
            row+=1
            
            ##### Laser controls #####
            controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
            row += 1
            controls_layout.addWidget(QtWidgets.QLabel("<b>Laser controls:</b>"), row, 0, 1, 4)
            row += 1

            self.laser_on=Checkbox_var(init_vars,"Laser on/off:","laser_on")
            self.laser_on.add_to_grid(controls_layout,row)
            self.laser_on.setBoard(board)
            row +=1

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


            ##### Position controls #####
            controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
            row += 1
            controls_layout.addWidget(QtWidgets.QLabel("<b>Stimulus positioning:</b>"), row, 0, 1, 4)
            row += 1

            ##### correct stimulus variables #####
            self.correct_stimulus_x_value=Spin_var(init_var_dict=init_vars,label="Correct stimulus X coordinate:",spin_min=1,spin_max=4800,step=1,varname="correct_stimulus_x_value")
            self.correct_stimulus_x_value.add_to_grid(controls_layout,row)
            self.correct_stimulus_x_value.setBoard(board)
            row+=1

            self.correct_stimulus_y_value=Spin_var(init_var_dict=init_vars,label="Correct stimulus Y coordinate:",spin_min=1,spin_max=4800,step=1,varname="correct_stimulus_y_value")
            self.correct_stimulus_y_value.add_to_grid(controls_layout,row)
            self.correct_stimulus_y_value.setBoard(board)
            row+=1

            self.correct_stimulus_z_value=Spin_var(init_var_dict=init_vars,label="Correct stimulus Z coordinate:",spin_min=1,spin_max=4800,step=1,varname="correct_stimulus_z_value")
            self.correct_stimulus_z_value.add_to_grid(controls_layout,row)
            self.correct_stimulus_z_value.setBoard(board)
            row+=1
            
            ##### outer bounds variables #####
            controls_layout.addWidget(QtWidgets.QLabel("<br>Outer bounds are the area where the stimulus moves to after being in whisking range<br>(waiting between trials) <br> The stimulus X/Y/Z coordinates can't be inside the bounds.<br> Written in format (start_position,end_position)"), row, 0, 1, 4)
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

            ##### offset positions #####
            controls_layout.addWidget(QtWidgets.QLabel("<br>Offset position list contains the coordinates for the corelated axis.<br>The position is calculated as an offset from the correct position coordinate.<br>Format: [integer,integer,...]"), row, 0, 1, 4)
            row += 1
            
            self.x_stimulus_offset = Text_var(init_vars, "Stimulus X offset list:", "x_stimulus_offset", text_width=INPUT_WIDTH)
            self.x_stimulus_offset.add_to_grid(controls_layout, row)
            self.x_stimulus_offset.setBoard(board)
            row += 1

            self.y_stimulus_offset = Text_var(init_vars, "Stimulus Y offset list:", "y_stimulus_offset", text_width=INPUT_WIDTH)
            self.y_stimulus_offset.add_to_grid(controls_layout, row)
            self.y_stimulus_offset.setBoard(board)
            row += 1

            self.z_stimulus_offset = Text_var(init_vars, "Stimulus Z offset list:", "z_stimulus_offset", text_width=INPUT_WIDTH)
            self.z_stimulus_offset.add_to_grid(controls_layout, row)
            self.z_stimulus_offset.setBoard(board)
            row += 1

            ##### Probability list #####
            controls_layout.addWidget(QtWidgets.QLabel("<br>The probability list gives probabilities of a certain position being used in a trial.<br>First one is for the correct position, then the rest are in order of offset list.<br>Total probabilities have to sum up to 1.<br>Format: [float,float,...]"), row, 0, 1, 4)
            row += 1

            self.position_probability_list = Text_var(init_vars, "Position probability list:", "position_probability_list", text_width=INPUT_WIDTH)
            self.position_probability_list.add_to_grid(controls_layout, row)
            self.position_probability_list.setBoard(board)
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
            """
            holds all the validation functions needed 
            connects the respective variable to their validation functions
            """
            def position_validator():
                """
                check that correct stimulus position does not fall in the outer bounds range
                """
                #pull correct position values
                correct_stimulus_x_value=eval(self.correct_stimulus_x_value.spn.text())
                correct_stimulus_y_value=eval(self.correct_stimulus_y_value.spn.text())
                correct_stimulus_z_value=eval(self.correct_stimulus_z_value.spn.text())

                #pull offset list values
                x_stimulus_offset=eval(self.x_stimulus_offset.line_edit.text())
                y_stimulus_offset=eval(self.y_stimulus_offset.line_edit.text())
                z_stimulus_offset=eval(self.z_stimulus_offset.line_edit.text())

                #pull outer bounds values (automatically parses into tuple type)
                stimulus_x_outer_bounds=eval(self.stimulus_x_outer_bounds.line_edit.text())
                stimulus_y_outer_bounds=eval(self.stimulus_y_outer_bounds.line_edit.text())
                stimulus_z_outer_bounds=eval(self.stimulus_z_outer_bounds.line_edit.text())

                #check that offset lists are of the same length
                if not len(x_stimulus_offset)==len(y_stimulus_offset)==len(z_stimulus_offset):
                    msg = QtWidgets.QMessageBox()
                    msg.setText("Offset lists have to be of the same length")
                    msg.exec()
                    #set values because user might be in the process of inputting values
                    self.x_stimulus_offset.set()
                    self.y_stimulus_offset.set()
                    self.z_stimulus_offset.set()
                    return
                


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
                
                #get minimum values for each axis (from all positions)
                #while also checking that offset+correct_position is withing legal bounds of the axis
                x_min=correct_stimulus_x_value
                for i in range(len(x_stimulus_offset)):
                    new_val=x_stimulus_offset[i]+correct_stimulus_x_value
                    x_min=min(x_min,new_val)
                    if new_val<0 or new_val>4800:
                        msg = QtWidgets.QMessageBox()
                        msg.setText("Offset value plus correct position value must be within 0-4800 range.<br>Found problem in x offset list in position " + str(i))
                        msg.exec()
                        return
                y_min=correct_stimulus_y_value
                for i in range(len(y_stimulus_offset)):
                    new_val=y_stimulus_offset[i]+correct_stimulus_y_value
                    y_min=min(y_min,new_val)
                    if new_val<0 or new_val>4800:
                        msg = QtWidgets.QMessageBox()
                        msg.setText("Offset value plus correct position value must be within 0-4800 range.<br>Found problem in y offset list in position " + str(i))
                        msg.exec()
                        return
                z_min=correct_stimulus_z_value
                for i in range(len(z_stimulus_offset)):
                    new_val=z_stimulus_offset[i]+correct_stimulus_z_value
                    z_min=min(z_min,new_val)
                    if new_val<0 or new_val>4800:
                        msg = QtWidgets.QMessageBox()
                        msg.setText("Offset value plus correct position value must be within 0-4800 range.<br>Found problem in z offset list in position " + str(i))
                        msg.exec()
                        return

                #validate correct position is outside the outer bounds
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
                
                for i in range(len(x_stimulus_offset)):
                    if x_stimulus_offset[i]==y_stimulus_offset[i]==z_stimulus_offset[i]==0:
                        msg = QtWidgets.QMessageBox()
                        msg.setText("Can't set offset position as zero in all axes (axis "+str(i) + ")")
                        msg.exec()
                        return

                self.correct_stimulus_x_value.set()
                self.correct_stimulus_y_value.set()
                self.correct_stimulus_z_value.set()

                self.stimulus_x_outer_bounds.set()
                self.stimulus_y_outer_bounds.set()
                self.stimulus_z_outer_bounds.set()

                self.x_stimulus_offset.set()
                self.y_stimulus_offset.set()
                self.z_stimulus_offset.set()



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



            def probability_validator():
                """
                checks probabilities sum to 1 and that every position has a corresponding probability
                """
                #pull probability list
                position_probability_list=eval(self.position_probability_list.line_edit.text())

                #run through values making sure the're floats that sum to 1
                sum=0
                for i in range(len(position_probability_list)):
                    if type(position_probability_list[i])==float:
                        sum+=position_probability_list[i]
                    else:
                        msg=QtWidgets.QMessageBox()
                        msg.setText("Probabilities have to be numbers less then 1 and in float format.<br>Problem with number in position "+str(i))
                        msg.exec()
                        return
                if sum!=1:
                    msg=QtWidgets.QMessageBox()
                    msg.setText("Probabilities have to sum to 1")
                    msg.exec()
                    return
                if len(position_probability_list) != len(eval(self.x_stimulus_offset.line_edit.text()))+1:
                    msg=QtWidgets.QMessageBox()
                    msg.setText("Length of probabilities list has to match number of positions.<br>(length of offset list + 1 for correct position)")
                    msg.exec()
                    return
                
                self.position_probability_list.set()


            ##### sound variables #####
            self.start_beep_frequency.set_btn.clicked.disconnect()
            self.start_beep_frequency.set_btn.clicked.connect(sound_validator)

            self.start_beep_frequency.set_btn.clicked.disconnect()
            self.start_beep_frequency.set_btn.clicked.connect(sound_validator)

            ##### stimulus position variables #####
            self.correct_stimulus_x_value.set_btn.clicked.disconnect()
            self.correct_stimulus_x_value.set_btn.clicked.connect(position_validator)

            self.correct_stimulus_y_value.set_btn.clicked.disconnect()
            self.correct_stimulus_y_value.set_btn.clicked.connect(position_validator)

            self.correct_stimulus_z_value.set_btn.clicked.disconnect()
            self.correct_stimulus_z_value.set_btn.clicked.connect(position_validator)

            ##### outer bounds variables #####
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

            ##### offset lists #####
            self.x_stimulus_offset.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.x_stimulus_offset.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.x_stimulus_offset.line_edit.returnPressed.connect(position_validator)
            self.x_stimulus_offset.set_btn.clicked.connect(position_validator)

            self.y_stimulus_offset.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.y_stimulus_offset.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.y_stimulus_offset.line_edit.returnPressed.connect(position_validator)
            self.y_stimulus_offset.set_btn.clicked.connect(position_validator)

            self.z_stimulus_offset.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
            self.z_stimulus_offset.set_btn.clicked.disconnect()  # disconnect the default clicked event
            self.z_stimulus_offset.line_edit.returnPressed.connect(position_validator)
            self.z_stimulus_offset.set_btn.clicked.connect(position_validator)

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