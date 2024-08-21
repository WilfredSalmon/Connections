from enum import Enum
from typing import List
from .Block import Block

class Streak_Type(Enum):
    ONGOING = 1
    LOST = 2
    INTERRUPTED = 3

class Streak():
    def __init__(self, blocks : List[Block], streak_type : Streak_Type):
        self.blocks = blocks
        self.streak_type = streak_type

        self.starting_number = blocks[0].number

        match streak_type:
            case Streak_Type.ONGOING:
                self.length = len(blocks)
                self.final_win_number = blocks[-1].number
            
            case Streak_Type.LOST:
                self.length = len(blocks) - 1
                self.final_win_number = blocks[-2].number
                self.ended_number = blocks[-1].number
                self.ended_categories_found = blocks[-1].number_found

            case Streak_Type.INTERRUPTED:
                self.length = len(blocks) - 1
                self.final_win_number = blocks[-2].number
                self.ended_number = blocks[-2].number + 1
    
    def __repr__(self):
        match self.streak_type:
            case Streak_Type.ONGOING:
                return f'''length {self.length}, starting on puzzle {self.starting_number} and continuing til their most recent puzzle, number {self.final_win_number}'''
            
            case Streak_Type.LOST:
                category_string = get_category_string(self.ended_categories_found)

                return f'''length {self.length}, starting on puzzle {self.starting_number} and continuing until puzzle {self.final_win_number}.
    This streak ended on puzzle {self.ended_number}, finding {self.ended_categories_found} {category_string}'''
                
            case Streak_Type.INTERRUPTED:
                return f'''length {self.length}, starting on puzzle {self.starting_number} and continuing until puzzle {self.final_win_number}.
    This streak ended on puzzle {self.ended_number}, where no attempt was submitted'''
    
def get_category_string(integer : int) -> str:
    if integer == 1:
        return 'category'
    else:
        return 'categories'