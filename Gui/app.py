from PyQt6 import QtWidgets, QtCore
from pathlib import Path
from src.Chat_Loader import Chat_Loader

STYLE_SHEET = """
    QWidget
    {
        color : black
    }
"""

class Main_Window(QtWidgets.QMainWindow):
    _background_color = "#e0ebeb"
    
    def __init__(self):
        super().__init__()
        
        self.resize(QtCore.QSize(1000, 600))
        self.setWindowTitle("NYT Connections stats")
        self.setStyleSheet(f"background-color : {self._background_color}")

        chat_file_path = Path("./Gui/files/_chat.txt")

        if chat_file_path.is_file():
            self.chat_loaded()
        else:
            chat_loader = Chat_Loader(self)
            self.setCentralWidget(chat_loader)
            chat_loader.chat_loaded.connect(self.chat_loaded)

    def chat_loaded(self):
        self.setCentralWidget(QtWidgets.QLabel("Chat loaded!"))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(STYLE_SHEET)
    window = Main_Window()
    window.show()
    app.exec()