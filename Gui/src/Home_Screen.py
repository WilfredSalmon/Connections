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
    state_changed = QtCore.pyqtSignal()
    _horizontal_padding = 10
    _vertical_padding = 5
    _sort_icon_brush = QtGui.QBrush(QtGui.QColor("black"))
    _sort_icon_width = 10
    _sort_icon_height = 7
    _sort_icon_gap = 2
    _transparent_pen = QtGui.QPen(Qt.GlobalColor.transparent)
    
    def __init__(self, header_title : str, sorting_method : Callable[[Player], float], font : QtGui.QFont, initial_state : _Sorting_State = _Sorting_State.NOT_SORTED, parent : QtWidgets.QWidget = None):
        super().__init__(parent = parent)
        self.state = initial_state
        self.sorting_method = sorting_method
        self.header_title = header_title
        self.header_font = font
        
        self.font_metric = QtGui.QFontMetrics(self.header_font)

        self.split_header = header_title.split()
        self.widths = [self.get_width(word) for word in self.split_header]
        
        self.space_width = self.get_width(" ")

        max_text_width = max(self.widths)
        self.sorting_icon_width = self._horizontal_padding + self._sort_icon_width
        
        self.min_width = max_text_width + self.sorting_icon_width + 2*self._horizontal_padding
        max_lines = len(self.split_header)
        self.max_height = self.font_metric.height() * max_lines + 2*self._vertical_padding

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Minimum)

    def get_width(self, string : str) -> int:
        return self.font_metric.horizontalAdvance(string)
    
    def set_state(self, new_state : _Sorting_State):
        self.state = new_state
        self.update()

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(self.min_width, self.max_height)

    def mouseReleaseEvent(self, e : QtGui.QMouseEvent):
        self.state = self.state.cycle()
        self.state_changed.emit()
        self.update()

    def paintEvent(self, e : QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setFont(self.header_font)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        content_rectangle = self.contentsRect()
        text_rect = QtCore.QRect(
            self._horizontal_padding, 
            self._vertical_padding, 
            content_rectangle.width() - 3*self._horizontal_padding - self._sort_icon_width,
            content_rectangle.height() - 2*self._vertical_padding
        )
        
        allowable_width = text_rect.width()
        self.update_wrapped_text(allowable_width)

        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter, self.text_to_draw)

        sort_icon_middle_right = content_rectangle.topRight().toPointF() + QtCore.QPointF(-self._horizontal_padding, content_rectangle.height()/2)
        self.draw_sort_icon(painter, sort_icon_middle_right)

    def draw_sort_icon(self, painter : QtGui.QPainter, middle_right : QtCore.QPointF):
        painter.setPen(self._transparent_pen)

        match self.state:
            case _Sorting_State.NOT_SORTED:
                self.draw_up_arrow(painter, middle_right - QtCore.QPointF(0, self._sort_icon_height/2 + self._sort_icon_gap/2))
                self.draw_down_arrow(painter, middle_right + QtCore.QPointF(0, self._sort_icon_height/2 + self._sort_icon_gap/2))
            
            case _Sorting_State.DESCENDING:
                self.draw_down_arrow(painter, middle_right)
            
            case _Sorting_State.ASCENDING:
                self.draw_up_arrow(painter, middle_right)

    def draw_up_arrow(self, painter : QtGui.QPainter, middle_right : QtCore.QPointF):
        path = QtGui.QPainterPath(middle_right + QtCore.QPointF(0, self._sort_icon_height/2))
        path.lineTo(path.currentPosition() + QtCore.QPointF(-self._sort_icon_width/2, -self._sort_icon_height))
        path.lineTo(path.currentPosition() + QtCore.QPointF(-self._sort_icon_width/2, +self._sort_icon_height))
        path.lineTo(path.currentPosition() + QtCore.QPointF(self._sort_icon_width, 0))
        painter.fillPath(path, self._sort_icon_brush)  
    
    def draw_down_arrow(self, painter : QtGui.QPainter, middle_right : QtCore.QPointF):
        path = QtGui.QPainterPath( middle_right + QtCore.QPointF(0, -self._sort_icon_height/2) )
        path.lineTo(path.currentPosition() + QtCore.QPointF(-self._sort_icon_width/2, self._sort_icon_height))
        path.lineTo(path.currentPosition() + QtCore.QPointF(-self._sort_icon_width/2, -self._sort_icon_height))
        path.lineTo(path.currentPosition() + QtCore.QPointF(self._sort_icon_width, 0))
        painter.fillPath(path, self._sort_icon_brush)

    def update_wrapped_text(self, allowable_width : int):
        # Start negative to account for no initial space
        current_width = - self.space_width
        self.text_to_draw = ""
        self.line_breaks = 0

        for text, width in zip(self.split_header, self.widths):
            current_width += self.space_width + width

            if current_width > allowable_width:
                join_char = "\n"
                current_width = width
                self.line_breaks += 1
            else:
                join_char = " "

            self.text_to_draw += join_char + text

        #Remove leading space
        self.text_to_draw = self.text_to_draw[1:]

class _Stats_Table(QtWidgets.QWidget):

    _columns : List[_Column] = [
        _Column (
            "Name",
            lambda player : player.name,
            "",
            True
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

        self.grid_layout = QtWidgets.QGridLayout()
        
        self.set_headers()
        self.set_rows()
        
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setHorizontalSpacing(15)
        self.grid_layout.setVerticalSpacing(10)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.grid_layout)

    def set_headers(self):
        header_font = QtGui.QFont()
        header_font.setBold(True)

        default_sort_set = False

        for index, column in enumerate(self._columns):
            if column.sortable:
                header_widget = _Sortable_Header(column.title, column.value_getter, header_font, parent = self)
                header_widget.state_changed.connect(lambda header = header_widget : self.header_clicked(header))
                
                if not default_sort_set:
                    self.default_sort = header_widget
                    self.current_sort = header_widget
                    self.current_sort.set_state(_Sorting_State.NOT_SORTED.cycle())
                    default_sort_set = True

            else:
                header_widget = QtWidgets.QLabel(column.title, parent = self)
                header_widget.setAlignment(Qt.AlignmentFlag.AlignRight)
                header_widget.setFont(header_font)
            
            self.grid_layout.addWidget(
                header_widget,
                0,
                index
            )

    def set_rows(self):
        player_list = self.sort_rows()
        
        for row_index, player in enumerate(player_list):
            for col_index, column in enumerate(self._columns): 
                entry = QtWidgets.QLabel(column.get_string(player))
                entry.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
                
                self.grid_layout.addWidget(
                    entry,
                    row_index + 1,
                    col_index
                )

    def sort_rows(self) -> List[Player]:
        player_list : List[Player] = []

        match self.current_sort.state:           
            case _Sorting_State.ASCENDING:
                player_list = sorted(self.player_list, key = self.current_sort.sorting_method)
            
            case _Sorting_State.DESCENDING:
                player_list = sorted(self.player_list, key = self.current_sort.sorting_method, reverse = True)
        
        return player_list

    def header_clicked(self, header : _Sortable_Header):
        match header.state:
            case _Sorting_State.NOT_SORTED:
                if header is self.current_sort:
                    self.current_sort = self.default_sort
                    self.default_sort.set_state(_Sorting_State.NOT_SORTED.cycle())
            
            case _:
                if self.current_sort is not header:
                    self.current_sort.set_state(_Sorting_State.NOT_SORTED)
                self.current_sort = header

        self.set_rows()

class Home_Screen(QtWidgets.QWidget):
    def __init__(self, player_list : List[Player], parent : QtWidgets.QWidget = None):
        super().__init__(parent = parent)

        title = QtWidgets.QLabel("NYT Connections Data")
        title_font = title.font()
        title_font.setPixelSize(20)
        title.setFont(title_font)

        table = _Stats_Table(player_list, parent = self)

        layout = QtWidgets.QVBoxLayout()
        layout.addStretch(10)
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(table, 60)
        layout.addStretch(10)

        self.setLayout(layout)
