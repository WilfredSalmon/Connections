from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt
from typing import List, Callable
from .util.Player import Player
from enum import Enum

class _Column():
    def __init__(self, title : str, value_getter : Callable[[Player], any], format : str, sortable : bool):
        self.title = title
        self.value_getter = value_getter
        self.format = format
        self.sortable = sortable

    def get_string(self, player : Player):
        return f'{self.value_getter(player):{self.format}}'

class _Sorting_State(Enum):
    NOT_SORTED = 0
    DESCENDING = 1
    ASCENDING = 2

    def cycle(self):
        new_index = (self.value + 1) % 3
        return _Sorting_State(new_index)

class _Sortable_Header(QtWidgets.QPushButton):
    
    state_changed = QtCore.pyqtSignal(_Sorting_State)
    _font = QtGui.QFont()
    _horizontal_padding = 10
    _vertical_padding = 10
    
    def __init__(self, header_title : str, initial_state : _Sorting_State = _Sorting_State.NOT_SORTED, parent : QtWidgets.QWidget = None):
        super().__init__(parent = parent)
        self.state = initial_state
        
        self.font_metric = QtGui.QFontMetrics(self._font)

        self.split_header = header_title.split()
        self.widths = [self.get_width(word) for word in self.split_header]
        self.space_width = self.get_width(" ")

        max_text_width = max(self.widths)
        self.sorting_icon_width = self._horizontal_padding + self.get_width("^")
        
        self.min_width = max_text_width + self.sorting_icon_width + self._horizontal_padding
        self.max_height = self.font_metric.height() * len(self.split_header) + self._vertical_padding

        self.header_title = header_title
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Maximum)

    def sizeHint(self):
        return QtCore.QSize(self.min_width, self.max_height)
    
    def get_width(self, string : str) -> int:
        return self.font_metric.horizontalAdvance(string)

    def mouseReleaseEvent(self, e : QtGui.QMouseEvent):
        self.state = self.state.cycle()
        self.state_changed.emit(self.state)
        self.update()
        print(self.state)

    def paintEvent(self, e : QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setFont(self._font)
        # painter.setPen(QtGui.QColor("black"))
        content_rectangle = self.contentsRect()
        padded_rect = QtCore.QRect(0, 0, content_rectangle.width() - self._horizontal_padding, content_rectangle.height() - self._vertical_padding)
        padded_rect.moveCenter(content_rectangle.center())
        allowable_width = padded_rect.width() - self.sorting_icon_width

        #Start negative to account for no initial space
        current_width = - self.space_width
        text_to_draw = ""

        for text, width in zip(self.split_header, self.widths):
            current_width += self.space_width + width

            if current_width > allowable_width:
                join_char = "\n"
                current_width = width
            else:
                join_char = " "

            text_to_draw += join_char + text

        #Remove leading space
        text_to_draw = text_to_draw[1:]
        painter.drawText(padded_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text_to_draw)

class Home_Screen(QtWidgets.QWidget):

    _columns : List[_Column] = [
        _Column (
            "Name",
            lambda player : player.name,
            "",
            False
        ),

        _Column (
            "Win Percentage",
            lambda player : player.total_wins/player.total_puzzles,
            ".0%",
            True
        ),

        _Column (
            "Longest Streak",
            lambda player : "0" if player.longest_streak is None else f'{player.longest_streak.length}',
            "",
            True
        ),

        _Column(
            "Current Streak",
            lambda player : "0" if player.current_streak is None else f'{player.current_streak.length}',
            "",
            True
        ),

        _Column (
            "Submitted Puzzles",
            lambda player : player.total_puzzles,
            "",
            True
        ),

        _Column (
            "Average Categories Found",
            lambda player : player.total_categories_found/player.total_puzzles,
            ".2f",
            True 
        ),

        _Column (
            "Average Attempts",
            lambda player : player.total_attempts/player.total_puzzles,
            ".2f",
            True
        )
    ]

    def __init__(self, player_list : List[Player], parent : QtWidgets.QWidget = None):
        super().__init__(parent = parent)
        self.player_list = player_list

        layout = QtWidgets.QGridLayout()
        
        self.set_headers(layout)
        self.set_rows(layout)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(10)
        self.setLayout(layout)

    def set_headers(self, layout : QtWidgets.QGridLayout):
        for index, column in enumerate(self._columns):
            if column.sortable:
                header_widget = _Sortable_Header(column.title, parent = self)
            else:
                header_widget = QtWidgets.QLabel(column.title)
            
            layout.addWidget(
                header_widget,
                0,
                index   
            )   

    def set_rows(self, layout : QtWidgets.QGridLayout):
        for row_index, player in enumerate(self.player_list):
            for col_index, column in enumerate(self._columns): 
                layout.addWidget(
                    QtWidgets.QLabel(column.get_string(player)),
                    row_index + 1,
                    col_index
                )