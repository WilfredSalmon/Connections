from .Raw_Block import Raw_Block
import re, pickle

class Connections_parser():
    def __init__(self, import_path : str, export_path : str):
        with open(import_path, mode = 'r', encoding='utf-8-sig') as fl:
            lines = fl.readlines()
        
        lines.append('buffer line')
        self.lines = lines
        
        self.length = len(lines)
        self.blocks = []
        self.export_path = export_path

    def extract_blocks(self):
        print('beginning parsing')

        for i in range(self.length):
            if contains_puzzle_number(self.lines[i]):
                self.blocks.append(self.extract_block_at_index(i))

        print(f'done parsing, found {len(self.blocks)} valid puzzles')
        print(self.blocks[-1])

        with open(self.export_path, 'wb') as fl:
            pickle.dump(self.blocks, fl)
        
    def extract_block_at_index(self, puzzle_line_index):
        block = Raw_Block()

        block.add_lines(self.get_header_line(puzzle_line_index))
        block.add_lines(self.get_puzzle_line(puzzle_line_index))
        block.add_lines(self.get_square_lines(puzzle_line_index))

        return block

    def get_header_line(self, puzzle_line_index):
        j=1
        while not constains_message_header(self.lines[puzzle_line_index-j]):
            j += 1

        return trim_newline_character(self.lines[puzzle_line_index-j])
    
    def get_puzzle_line(self, puzzle_line_index):
        return trim_newline_character(self.lines[puzzle_line_index])

    def get_square_lines(self, puzzle_line_index):
        square_lines = []
        j=1
        
        while is_square_line(self.lines[puzzle_line_index+j]):
            square_lines.append(trim_newline_character(self.lines[puzzle_line_index+j]))
            j += 1
        
        return square_lines
    
def contains_puzzle_number(string):
    search_attempt = re.search('Puzzle #[0-9]+', string)
    if search_attempt == None:
        return False
    
    return re.search('Puzzle #[0-9]+', string)[0] == trim_newline_character(string)

def constains_message_header(string):
    return re.search(r'\[\d{2}\/\d{2}\/\d{4}, \d{2}:\d{2}:\d{2}\]', string) != None

def is_square_line(string):
    return re.search('[🟨🟩🟦🟪]{4}', string) != None

def trim_newline_character(string):
    return string[0:-1]