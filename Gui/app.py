from PyQt6 import QtWidgets, QtCore
from pathlib import Path
from src.Chat_Loader import Chat_Loader
from src.util.Connections_parser import Connections_parser

base_file_path = "./Gui/"
chatlog_file_path = f"{base_file_path}files/_chat.txt"
parsed_file_path = f"{base_file_path}files/parsed_text.py"

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

        chat_file_path = Path(chatlog_file_path)

        if chat_file_path.is_file():
            self.chat_loaded()
        else:
            chat_loader = Chat_Loader(self)
            self.setCentralWidget(chat_loader)
            chat_loader.chat_loaded.connect(self.chat_loaded)

    def chat_loaded(self):
        parsed_text_filepath = Path(parsed_file_path)

        if not parsed_text_filepath.is_file():
            parser = Connections_parser(chatlog_file_path, parsed_file_path)
            parser.extract_blocks()

        self.setCentralWidget(QtWidgets.QLabel("Chat loaded and parsed!"))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(STYLE_SHEET)
    window = Main_Window()
    window.show()
    app.exec()