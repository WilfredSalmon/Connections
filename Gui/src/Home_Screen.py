from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from typing import Dict
from .util.Player import Player

class Home_Screen(QtWidgets.QWidget):
    def __init__(self, name_player_dict : Dict[str, Player], parent : QtWidgets.QWidget = None):
        super().__init__(parent = parent)
        self.name_player_dict = name_player_dict
        
        self.model = _Player_Stats_Model(self.name_player_dict)
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.table.setShowGrid(False)
        self.table.setWordWrap(True)


        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.table)
        self.setLayout(layout)

class _Player_Stats_Model(QtCore.QAbstractTableModel):
    _headers = ["Name", "Win Percentage", "Longest Streak", "Current Streak", "Total Puzzles", "Average Categories Found", "Average Number of Attempts"]
    
    def __init__(self, name_player_dict : Dict[str, Player], parent : QtWidgets.QWidget = None):
        super().__init__(parent = parent)
        self.names = [name for name in name_player_dict]
        self.name_player_dict = name_player_dict

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            name = self.names[index.row()]
            player = self.name_player_dict[name]

            match index.column():
                case 0:
                    return name
                
                case 1:
                    return f'{player.total_wins/player.total_puzzles:.0%}'
                
                case 2:
                    if player.longest_streak is None:
                        return 0
                    
                    return player.longest_streak.length
                
                case 3:
                    if player.current_streak is None:
                        return 0
                    
                    return player.current_streak.length
                
                case 4:
                    return player.total_puzzles
                
                case 5:
                    return f'{player.total_categories_found/player.total_puzzles:.2f}'
                
                case 6:
                    return f'{player.total_attempts/player.total_puzzles:.2f}'
                
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                    return self._headers[section]
            else:
                return ""
    
    def rowCount(self, index):
        return len(self.names)
    
    def columnCount(self, index):
        return 7