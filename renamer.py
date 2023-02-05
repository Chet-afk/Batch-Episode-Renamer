import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class main_window(QMainWindow):

    def __init__(self):
        super(main_window, self).__init__()

        # Create variables for filepaths, combobox choices etc.
        self.file_path = ""
        self.start_number = 1

        self.test_output = QCheckBox()

        self.show_name = QLineEdit()

        self.rename_type = QComboBox()
        self.season_pick_label = QLabel("What Season is this?")
        self.season_pick = QSpinBox()

        self.file_label = QLabel()

        self.setWindowTitle("Batch Renamer")

        self.setGeometry(0, 0, 1280, 720)

        central_widget = QWidget()  # Must have central widget set
        central_widget.setLayout(self.create_vlayout())

        self.setCentralWidget(central_widget)

        self.show()


    def create_vlayout(self):   # Creates the interactions in central widget
        vbox = QVBoxLayout(self)
        vbox.addLayout(self.choose_folder())
        vbox.addSpacing(20)
        vbox.addWidget(self.horizontal_line())
        vbox.addSpacing(20)
        vbox.addLayout(self.settings_layout())
        vbox.addSpacing(20)
        vbox.addWidget(self.horizontal_line())
        vbox.addSpacing(20)
        vbox.addWidget(self.output_log())
        return vbox

    def choose_folder(self):
        hbox = QHBoxLayout()

        btn = QPushButton("Choose Folder", self)
        btn.clicked.connect(self.select_directory) # Connect button to begin renaming.
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

        vbox_settings.addWidget(title)
        vbox_settings.addLayout(self.choose_rename_type())
        vbox_settings.addSpacing(10)
        vbox_settings.addLayout(self.rename_to())
        vbox_settings.addSpacing(10)
        vbox_settings.addWidget(self.test_output)


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

        hbox.addWidget(show_name_label)
        hbox.addWidget(self.show_name)

        return hbox


    def horizontal_line(self):
        # Create a horizontal line separator
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setLineWidth(1)
        return h_line
    def output_log(self):
        # Field for any kind of output
        output_field = QTextEdit()
        output_field.setReadOnly(True)
        output_field.setLineWrapColumnOrWidth(True)

        font = QFont()
        font.setFamily("Serif")
        font.setPointSize(12)

        output_field.setFont(font)

        scroll_bar = output_field.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

        output_field.setPlaceholderText("Output Logs")
        return output_field

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
            self.file_path = directory
            self.file_label.setText(directory)


    def rename_click(self):
        file_path = input("Please enter file path: ")
        os.chdir(file_path)
        cwd = os.getcwd()

        print("\nCurrent Directory: " + cwd + "\n")

        files = os.listdir(".")

        renamed = input("What would you like to rename the files to?: ").strip()

        fileType = input("What is the file extension? (i.e .mkv, .mp4): ").strip()

        epNum = 1

        for each_file in files:

            if os.path.isdir(each_file):
                print("\"" + each_file + "\"", "is a directory.")

                continue

            print("\n" + each_file, "is being renamed to: " + renamed + " Episode " + str(epNum).zfill(
                2) + fileType)  # .zfill puts it to at least 2 digits for single digits

            os.rename(each_file, renamed + " Episode " + str(epNum).zfill(
                2) + fileType)  # Rename instead of Replace so program stops if it tries to replace itself
            epNum += 1


def main():
    app = QApplication([])
    window = main_window()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
