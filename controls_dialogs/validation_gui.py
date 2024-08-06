from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
from source.gui.custom_controls_dialog import Text_var
from source.gui.settings import get_setting

TITLE = "Example controls with input validation"
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

        self.positions = Text_var(init_vars, "📍 <b>Positions</b>", "positions", text_width=INPUT_WIDTH)
        self.positions.add_to_grid(controls_layout, row)
        self.positions.setBoard(board)
        row += 1

        self.probabilites = Text_var(init_vars, "🎲 <b>Probabilities</b>", "position_probability_list", text_width=200)
        self.probabilites.add_to_grid(controls_layout, row)
        self.probabilites.setBoard(board)
        row += 1

        self.create_validators()

        # separator
        controls_layout.addWidget(QtWidgets.QLabel("<hr>"), row, 0, 1, 4)
        row += 1

        # add other variables that don't need validation
        other_variables = [
            "var_a",
            "var_b",
            "var_c",
        ]
        for other_var in other_variables:
            var_input = Text_var(init_vars, f"<b>{other_var}</b>", other_var, text_width=INPUT_WIDTH)
            var_input.add_to_grid(controls_layout, row)
            var_input.setBoard(board)
            row += 1

        #if you want to add event trigger uncomment the following 3 lines
        # self.create_events_trigger_groupbox()
        # controls_layout.addWidget(self.events_groupbox, row, 0, 1, 4)
        # row += 1

        #if you want to add notes uncomment the following 3 lines
        # self.create_notes_groupbox()
        # controls_layout.addWidget(self.notes_groupbox, row, 0, 1, 4)
        # row += 1

        controls_layout.setRowStretch(row, 1)
        widget.setLayout(controls_layout)
        grid_layout.addWidget(widget, 0, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        # add close shortcut
        self.close_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(self.close)


    def create_validators(self):
        # creat position validator
        def postion_validator():
            positions = eval(self.positions.line_edit.text())  # grab value from the line edit
            probabilites = eval(self.probabilites.line_edit.text())  # grab value from the line edit

            # validate that the input is a list
            if type(positions) is not list:
                msg = QtWidgets.QMessageBox()
                msg.setText("positions must be a list")
                msg.exec()
                return

            # validate that the input is the correct length
            position_list_length = len(positions)
            probabilites_list_length = len(probabilites)
            if position_list_length != probabilites_list_length:
                msg = QtWidgets.QMessageBox()
                msg.setText(
                    f"positions and probabilites should have the same length.\n Right now positions has length {position_list_length} and probabilites has length {probabilites_list_length}"
                )
                msg.exec()
                return

            # if the input is valid then we can set the value as normal
            self.positions.set()

        # connect the validator to the line edit and set button
        self.positions.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
        self.positions.set_btn.clicked.disconnect()  # disconnect the default clicked event
        self.positions.line_edit.returnPressed.connect(postion_validator)
        self.positions.set_btn.clicked.connect(postion_validator)

        # creat probabilities validator
        def probabilities_validator():
            probabilites = eval(self.probabilites.line_edit.text())  # grab value from the line edit
            positions = eval(self.positions.line_edit.text())  # grab value from the line edit

            # validate that the input is a list
            if type(probabilites) is not list:
                msg = QtWidgets.QMessageBox()
                msg.setText("positions must be a list")
                msg.exec()
                return

            # validate that the input is the correct length
            position_list_length = len(positions)
            probabilites_list_length = len(probabilites)
            if position_list_length != probabilites_list_length:
                msg = QtWidgets.QMessageBox()
                msg.setText(
                    f"positions and probabilites should have the same length.\n Right now positions has length {position_list_length} and probabilites has length {probabilites_list_length}"
                )
                msg.exec()
                return

            # validate that the input sums to 1
            probability_sum = round(sum(probabilites),3)
            if probability_sum != 1:
                msg = QtWidgets.QMessageBox()
                msg.setText(f"probabilities must sum to 1. It currently sums to {probability_sum}")
                msg.exec()
                return

            # if the input is valid then we can set the value as normal
            self.positions.set()

        # connect the validator to the line edit and set button
        self.probabilites.line_edit.returnPressed.disconnect()  # disconnect the default returnPressed event
        self.probabilites.set_btn.clicked.disconnect()  # disconnect the default clicked event
        self.probabilites.line_edit.returnPressed.connect(probabilities_validator)
        self.probabilites.set_btn.clicked.connect(probabilities_validator)



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