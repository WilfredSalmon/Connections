from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from typing import Dict, List
from .util.Player import Player

class _Column():
    def __init__(self, title : str, value_getter, format : str, sortable : bool):
        self.title = title
        self.value_getter = value_getter
        self.format = format
        self.sortable = sortable

    def get_string(self, player : Player):
        return f'{self.value_getter(player):{self.format}}'


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
            lambda player : player.total_attempts,
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

    def __init__(self, name_player_dict : Dict[str, Player], parent : QtWidgets.QWidget = None):
        super().__init__(parent = parent)
        self.name_player_dict = name_player_dict

        self.names = [name for name in name_player_dict]
        layout = QtWidgets.QGridLayout()
        
        self.set_headers(layout)
        self.set_rows(layout)
        
        self.setLayout(layout)

    def set_headers(self, layout : QtWidgets.QGridLayout):
        for index, column in enumerate(self._columns):
            layout.addWidget(
                QtWidgets.QLabel(column.title),
                0,
                index   
            )

    def set_rows(self, layout : QtWidgets.QGridLayout):
        for row_index, name in enumerate(self.names):
            player = self.name_player_dict[name]
            
            for col_index, column in enumerate(self._columns): 
                layout.addWidget(
                    QtWidgets.QLabel(column.get_string(player)),
                    row_index + 1,
                    col_index
                )