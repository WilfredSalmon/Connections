from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt

class Default_Button(QtWidgets.QPushButton):
    _border_pen = QtGui.QPen(Qt.GlobalColor.transparent)
    
    _unpressed_brush = QtGui.QBrush(QtGui.QColor("#9999ff"))
    _pressed_brush = QtGui.QBrush(QtGui.QColor("#4d4dff"))

    _unpressed_text_pen = QtGui.QPen(QtGui.QColor("black"))
    _pressed_text_pen = QtGui.QPen(QtGui.QColor("black"))

    _shadow_color = QtGui.QColor("#c2c4c4")

    def __init__(self, text : str = None, parent = None):
        super().__init__(parent = parent)
        self.button_text = text
        self.button_held = False

        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(5)
        shadow.setColor(self._shadow_color)

        self.setGraphicsEffect(shadow)

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