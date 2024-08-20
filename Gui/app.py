from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt
from shutil import copy2

STYLE_SHEET = """
    QWidget
    {
        color : black
    }
"""

class Main_Window(QtWidgets.QMainWindow):
    background_color = "#e0ebeb"
    
    def __init__(self):
        super().__init__()
        
        self.resize(QtCore.QSize(1000, 600))
        self.setWindowTitle("NYT Connections stats")
        self.setStyleSheet(f"background-color : {self.background_color}")

        self.setCentralWidget(Chat_Loader(self))

class Chat_Loader(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

        label = QtWidgets.QLabel("No chat history loaded", parent = self)
        button = QtWidgets.QPushButton("Add Chat", parent = self)

        button.pressed.connect(self.load_chat)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)
        
    def load_chat(self):
        print("Loading chat")
        popup = QtWidgets.QFileDialog(self)
        popup.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        popup.setNameFilter("Text files (*.txt)")
        
        if popup.exec():
            copy2(popup.selectedFiles()[0], "./Gui/files/_chat.txt")
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to select file")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(STYLE_SHEET)
    window = Main_Window()
    window.show()
    app.exec()