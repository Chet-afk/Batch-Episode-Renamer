import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class main_window(QMainWindow):

    def __init__(self):
        super(main_window, self).__init__()

        # Create variables for items that need info retrieved

        self.test_output = QCheckBox()
        self.test_output.setChecked(True)

        self.show_name = QLineEdit()

        self.rename_type = QComboBox()
        self.season_pick_label = QLabel("What Season is this?")
        self.season_pick = QSpinBox()

        self.file_label = QLabel()

        self.output_field = QTextEdit()

        self.setWindowTitle("Batch Renamer")

        self.setGeometry(0, 0, 1280, 720)

        central_widget = QWidget()  # Must have central widget set
        central_widget.setLayout(self.create_vlayout())

        self.setCentralWidget(central_widget)

        self.show()


    def create_vlayout(self):   # Creates the interactions in central widget
        vbox = QVBoxLayout(self)
        vbox.addSpacing(20)
        vbox.addLayout(self.choose_folder())
        vbox.addSpacing(20)
        vbox.addWidget(self.horizontal_line())
        vbox.addSpacing(20)
        vbox.addLayout(self.settings_layout())
        vbox.addSpacing(20)
        vbox.addWidget(self.horizontal_line())
        vbox.addSpacing(20)
        vbox.addLayout(self.output_log())
        return vbox

    def choose_folder(self):
        hbox = QHBoxLayout()

        btn = QPushButton("Choose Folder", self)
        btn.clicked.connect(self.select_directory)
        btn.setMaximumWidth(100)

        font = QFont()
        font.setFamily("Serif")
        font.setBold(True)
        font.setPointSize(12)

        self.file_label.setFont(font)
        self.file_label.setText("No Folder Chosen")

        hbox.addWidget(btn)
        hbox.addWidget(self.file_label)

        return hbox

    def settings_layout(self):

        vbox_settings = QVBoxLayout()

        title = QLabel("Settings")

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)

        title.setFont(font)

        self.test_output.setToolTip("Enable this if you want to test the output.")
        self.test_output.setText("Test Output")
        self.test_output.setFont(QFont("Serif", 10))
        self.test_output.setMaximumWidth(150)

        execute = QPushButton("Execute Renamer")
        execute.setMaximumWidth(100)
        execute.clicked.connect(self.rename_click)



        vbox_settings.addWidget(title)
        vbox_settings.addSpacing(10)
        vbox_settings.addLayout(self.choose_rename_type())
        vbox_settings.addSpacing(10)
        vbox_settings.addLayout(self.rename_to())
        vbox_settings.addSpacing(10)
        vbox_settings.addWidget(self.test_output)
        vbox_settings.addSpacing(10)
        vbox_settings.addWidget(execute)



        return vbox_settings

    def choose_rename_type(self):
        # 0 will be in the form of SxxEyy
        # 1 is sequential starting from 1. i.e. Episode 1 etc.
        hbox = QHBoxLayout()

        rename_label = QLabel("Rename Scheme: ")
        rename_label.setFont(QFont("Serif", 10))

        self.rename_type.addItem("Seasonal [SxxEyy]")
        self.rename_type.addItem("Sequential [Episode X]")
        self.rename_type.activated.connect(self.show_season)

        self.season_pick_label.setFont(QFont("Serif", 10))

        hbox.addWidget(rename_label)
        hbox.addWidget(self.rename_type)
        hbox.addWidget(self.season_pick_label)
        hbox.addWidget(self.season_pick)
        hbox.addStretch(1)

        return hbox

    def rename_to(self):
        # Layout for entering the show name
        hbox = QHBoxLayout()

        show_name_label = QLabel("Enter the show name:")
        show_name_label.setFont(QFont("Serif", 10))
        self.show_name.setPlaceholderText("E.g. Overlord, Gravity Falls, Wednesday, etc.")
        self.show_name.setMinimumWidth(250)

        hbox.addWidget(show_name_label)
        hbox.addWidget(self.show_name)
        hbox.addStretch(1)

        return hbox


    def horizontal_line(self):
        # Create a horizontal line separator
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setLineWidth(1)
        return h_line
    def output_log(self):
        # Field for any kind of output

        vbox_all = QVBoxLayout()
        hbox_buttons = QHBoxLayout()

        clear_log = QPushButton("Clear Logs")
        clear_log.setMaximumWidth(100)
        clear_log.clicked.connect(self.clear_log)

        list_files = QPushButton("List Files in Directory")
        list_files.setMaximumWidth(150)
        list_files.clicked.connect(self.list_items)

        hbox_buttons.addWidget(clear_log)
        hbox_buttons.addWidget(list_files)

        self.output_field.setReadOnly(True)
        self.output_field.setLineWrapColumnOrWidth(True)

        font = QFont()
        font.setFamily("Serif")
        font.setPointSize(10)

        self.output_field.setFont(font)

        scroll_bar = self.output_field.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

        self.output_field.setPlaceholderText("Output Logs")

        vbox_all.addLayout(hbox_buttons)
        vbox_all.addSpacing(20)
        vbox_all.addWidget(self.output_field)

        return vbox_all

    def clear_log(self):
        self.output_field.clear()

    def show_season(self):
        if (self.rename_type.currentIndex() == 0):
            self.season_pick_label.show()
            self.season_pick.show()
        else:
            self.season_pick_label.hide()
            self.season_pick.hide()

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if not (directory == ""):
            os.chdir(directory)
            self.file_label.setText(directory)
            self.output_field.append("Moved to " + directory + "\n")
            self.line_break()

    def list_items(self):
        try:

            self.output_field.append("Listing items in directory...\n")

            for each_item in os.listdir("."):

                if (os.path.isdir(each_item)):
                    self.output_field.append(each_item + " is a directory\n")
                else:
                    self.output_field.append(each_item + "\n")

            self.line_break()
        except:
            self.output_field.append("Error: Could not list files in directory - " + os.getcwd())
            self.line_break()

    def line_break(self):
        # Helper function for line breaking after output is written
        self.output_field.append("--------------------------\n")

    def rename_click(self):

        renamed = self.show_name.text().strip()
        rename_type = self.rename_type.currentIndex() # 0 is SxxEyy, 1 is sequential

        epNum = 1

        for each_file in os.listdir("."):
            if os.path.isdir(each_file):
                continue

            file_type = "." + each_file.split(".")[-1]
            start_of_string = each_file + " is being renamed to: "

            match(rename_type):
                # Case SxxEyy
                case 0:
                    season = self.season_pick.value()
                    self.output_field.append(start_of_string + renamed + " S" + str(season).zfill(2) +
                                     "E" + str(epNum).zfill(2) + file_type + "\n")

                    if not self.test_output.isChecked():
                        os.rename(each_file, renamed + " S" + str(season).zfill(2) +
                                     "E" + str(epNum).zfill(2) + file_type)

                case 1:
                    # .zfill puts it to at least 2 digits for single digits
                    self.output_field.append(start_of_string + renamed +
                                     " Episode " + str(epNum).zfill(2) + file_type + "\n")
                    if not self.test_output.isChecked():
                        os.rename(each_file, renamed +
                                     " Episode " + str(epNum).zfill(2) + file_type)


            # os.rename(each_file, renamed + " Episode " + str(epNum).zfill(
            #     2) + file_type)  # Rename instead of Replace so program stops if it tries to replace itself
            epNum += 1

        self.line_break()


def main():
    app = QApplication([])
    window = main_window()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
