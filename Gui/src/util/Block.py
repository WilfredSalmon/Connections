from .Raw_Block import Raw_Block
import re 
from enum import Enum
from typing import List

class Line_Type(Enum):
    FAIL = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    PURPLE = 5

class Block:
    def __init__(self, raw_block : Raw_Block):
        self.lines = raw_block.lines
        self.parse()
    
    def parse(self) -> None:
        self.parsed = True
        
        self.set_name()
        self.set_number()
        self.extract_submission_data()

    def set_name(self) -> None:
        try:
            self.name = re.search('\][~  ]+([a-zA-Z ]+)', self.lines[0]).group(1)
        except:
            print(f'#WARNING: failed to parse name from string \n {self.lines} \n#')
            self.parsed = False
            self.name = 'UNKNOWN'

    def set_number(self) -> None:
        try:
            self.number = int(re.search('[0-9]+', self.lines[1]).group())
        except:
            print(f'#WARNING: failed to parse puzzle number from string \n {self.lines} \n#')
            self.parsed = False
            self.number = 0
    
    def extract_submission_data(self) -> None:
        self.number_found = 0
        self.attempts = 0
        self.fails = 0
        self.line_types : List[Line_Type] = []

        for square_line in self.lines[2:]:
            self.attempts += 1
            
            if square_line_is_success(square_line):
                self.number_found += 1
                self.add_line_type(square_line)
            else:
                self.fails += 1
                self.line_types.append(Line_Type.FAIL)
        
        self.won = (self.number_found == 4)

    def add_line_type(self, square_line : str) -> None:
        match square_line[0]:
            case '🟨':
                self.line_types.append(Line_Type.YELLOW)
            case '🟩':
                self.line_types.append(Line_Type.GREEN)
            case '🟦':
                self.line_types.append(Line_Type.BLUE)
            case '🟪':
                self.line_types.append(Line_Type.PURPLE)

    def __repr__(self):
        return f'On puzzle number {self.number}, {self.name} found {self.number_found} categories in {self.attempts} attempts, won = {self.won}\n'
    
def square_line_is_success(string : str) -> bool:
    return all((c == string[0] for c in string))