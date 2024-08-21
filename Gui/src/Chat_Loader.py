from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from shutil import copy2
from .buttons.Default_Button import Default_Button

class Chat_Loader(QtWidgets.QWidget):
    chat_loaded = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent = parent)

        label = QtWidgets.QLabel("No chat history loaded", parent = self)
        font = label.font()
        font.setPointSize(20)
        label.setFont(font)

        button = Default_Button("Load chat", parent = parent)

        button.pressed.connect(self.load_chat)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        layout.addSpacing(100)
        layout.addWidget(button, alignment = Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        
    def load_chat(self) -> None:
        print("Loading chat")
        popup = QtWidgets.QFileDialog(self)
        popup.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        popup.setNameFilter("Text files (*.txt)")
        
        if popup.exec():
            copy2(popup.selectedFiles()[0], "./Gui/files/_chat.txt")
            self.chat_loaded.emit()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to select file")