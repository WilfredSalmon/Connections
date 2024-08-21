from .Raw_Block import Raw_Block
from .Player import Player
from .Block import Block
import re, pickle
from typing import Dict, List

class Connections_parser():
    def __init__(self, import_path : str, export_path : str):
        with open(import_path, mode = 'r', encoding='utf-8-sig') as fl:
            self.lines = fl.readlines()
        
        self.lines.append('buffer line')
        
        self.raw_blocks : List[Raw_Block] = []
        self.export_path = export_path

    def extract_data(self):
        print('beginning parsing')

        for index, line in enumerate(self.lines):
            if contains_puzzle_number(line):
                self.raw_blocks.append(self.extract_block_at_index(index))

        print(f'done parsing, found {len(self.raw_blocks)} valid puzzles')
        print(self.raw_blocks[-1])
        print('Analysing data')

        self.name_player_dict : Dict[str, Player] = {}
        self.puzzle_numbers : List[int] = []

        for raw_block in self.raw_blocks:
            block = Block(raw_block) # TODO add error handling
            name = block.name

            if name not in self.name_player_dict:
                self.name_player_dict[name] = Player(name)

            if block.number not in self.puzzle_numbers:
                self.puzzle_numbers.append(block.number)

            self.name_player_dict[name].add_block(block)
        
        self.puzzle_numbers.sort()
        
        for player in self.name_player_dict.values():
            player.process_data()

        with open(self.export_path, 'wb') as fl:
            pickle.dump(self.name_player_dict, fl)
            pickle.dump(self.puzzle_numbers, fl)
        
    def extract_block_at_index(self, puzzle_line_index : int) -> Raw_Block:
        raw_block = Raw_Block()

        raw_block.add_lines(self.get_header_line(puzzle_line_index))
        raw_block.add_lines(self.get_puzzle_line(puzzle_line_index))
        raw_block.add_lines(self.get_square_lines(puzzle_line_index))

        return raw_block

    def get_header_line(self, puzzle_line_index : int) -> str:
        j = 1
        while not constains_message_header(self.lines[puzzle_line_index-j]):
            j += 1

        return trim_newline_character(self.lines[puzzle_line_index-j])
    
    def get_puzzle_line(self, puzzle_line_index : int) -> str:
        return trim_newline_character(self.lines[puzzle_line_index])

    def get_square_lines(self, puzzle_line_index : int) -> str:
        square_lines : List[str] = []
        j = 1
        
        while is_square_line(self.lines[puzzle_line_index+j]):
            square_lines.append(trim_newline_character(self.lines[puzzle_line_index+j]))
            j += 1
        
        return square_lines
    
def contains_puzzle_number(string : str) -> bool:
    search_attempt = re.search('Puzzle #[0-9]+', string)
    
    if search_attempt == None:
        return False
    
    return re.search('Puzzle #[0-9]+', string)[0] == trim_newline_character(string)

def constains_message_header(string : str) -> bool:
    return re.search(r'\[\d{2}\/\d{2}\/\d{4}, \d{2}:\d{2}:\d{2}\]', string) != None

def is_square_line(string : str) -> bool:
    return re.search('[🟨🟩🟦🟪]{4}', string) != None

def trim_newline_character(string : str) -> str:
    return string[0:-1]