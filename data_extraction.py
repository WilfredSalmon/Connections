import pickle
from Connections_parser import Connections_parser

whatsapp_data_file = '_chat.txt'
parsed_file = 'parsed_text.py'

with open(whatsapp_data_file, mode = 'r', encoding='utf-8-sig') as fl:
    lines = fl.readlines()

parser = Connections_parser(lines)
parser.extract_blocks()

print(parser.blocks[-1])

with open(parsed_file, 'wb') as fl:
    pickle.dump(parser.blocks, fl)