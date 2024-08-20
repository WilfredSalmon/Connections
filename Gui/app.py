from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt
from shutil import copy2
from pathlib import Path

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

class Custom_Button(QtWidgets.QPushButton):
    _border_pen = QtGui.QPen(Qt.GlobalColor.transparent)
    
    _unpressed_brush = QtGui.QBrush(QtGui.QColor("#9999ff"))
    _pressed_brush = QtGui.QBrush(QtGui.QColor("#4d4dff"))

    _unpressed_text_pen = QtGui.QPen(QtGui.QColor("black"))
    _pressed_text_pen = QtGui.QPen(QtGui.QColor("black"))

    def __init__(self, text : str = None, parent = None):
        super().__init__(parent = parent)
        self.button_text = text
        self.button_held = False

    def sizeHint(self):
        return QtCore.QSize(100, 30)

    def paintEvent(self, e : QtGui.QPaintEvent):
        content_rectangle = self.contentsRect()
        
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setPen(self._border_pen)

        if self.button_held:
            painter.setBrush(self._pressed_brush)
        else:
            painter.setBrush(self._unpressed_brush)
        
        painter.drawRoundedRect(content_rectangle, 15 , 15)

        # TODO : can these be combined into a single if statement?
        if self.button_held:
            painter.setPen(self._pressed_text_pen)
        else:
            painter.setPen(self._unpressed_text_pen)

        painter.drawText(content_rectangle, Qt.AlignmentFlag.AlignCenter, self.button_text)  

    def mousePressEvent(self, e):
        self.button_held = True
        self.update()

    def mouseReleaseEvent(self, e):
        self.button_held = False
        self.update()
        self.pressed.emit()

class Chat_Loader(QtWidgets.QWidget):

    chat_loaded = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent = parent)

        label = QtWidgets.QLabel("No chat history loaded", parent = self)
        font = label.font()
        font.setPointSize(20)
        label.setFont(font)

        button = Custom_Button("Load chat", parent = parent)

        button.pressed.connect(self.load_chat)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        layout.addSpacing(100)
        layout.addWidget(button, alignment = Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        
    def load_chat(self):
        print("Loading chat")
        popup = QtWidgets.QFileDialog(self)
        popup.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        popup.setNameFilter("Text files (*.txt)")
        
        if popup.exec():
            copy2(popup.selectedFiles()[0], "./Gui/files/_chat.txt")
            self.chat_loaded.emit()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to select file")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(STYLE_SHEET)
    window = Main_Window()
    window.show()
    app.exec()