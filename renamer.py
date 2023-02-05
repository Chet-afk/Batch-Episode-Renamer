import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class main_window(QMainWindow):

    def __init__(self):
        super(main_window, self).__init__()

        # Create variables for filepaths, combobox choices etc.
        self.file_path = ""
        self.rename_type = 1
        self.start_number = 1

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

    def output_log(self):
        output_field = QTextEdit()
        output_field.setReadOnly(True)
        output_field.setLineWrapColumnOrWidth(True)
        return output_field

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
