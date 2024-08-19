import pickle
from math import ceil,floor

from Player import Player
from Puzzle import Puzzle
from Block import Block

import matplotlib.pyplot as plt
import numpy as np

def plot_cumulative_wins(players, puzzle_numbers):
    player_cumulative_wins = [(player, get_cumulative_wins(player, puzzle_numbers)) for player in players] 
    
    _, ax = plt.subplots()

    for data in player_cumulative_wins:
        ax.plot(puzzle_numbers, data[1], label = f'{data[0].name}')

    ax.set_title('Cumulative wins against puzzle number')
    ax.set_xlabel('Puzzle number')
    ax.set_ylabel('Cumulative wins')

    ax.set_xlim(left=puzzle_numbers[0]-1)

    ax.legend()
    plt.show()

def get_cumulative_wins(player, puzzle_numbers):
    current_wins = 0
    cumulative_wins = []

    for number in puzzle_numbers:
        if number in player.block_dictionary:
            current_wins += player.block_dictionary[number].won

        cumulative_wins.append(current_wins)

    return cumulative_wins

def plot_player_histograms(players):
    no_players = len(players)
    rows = ceil(no_players/2)
    
    _, axs = plt.subplots(rows, 2)

    for player_index in range(no_players):
        player = players[player_index]

        axis = get_axis(axs, player_index)

        axis.bar(*zip(*player.scores.items())) # * is the unpacking operator, e.g. unpacks dict into list of vars
        axis.set_title(player.name)

    plt.show()

def get_axis(axs, player_index):
    row_index = floor(player_index/2)
    col_index = player_index % 2
    axis = axs[row_index, col_index]
    return axis

def get_player_correlation(player1, player2):
    player1_data = []
    player2_data = []
    
    for number in player1.block_dictionary.keys():
        if number in player2.block_dictionary:
            player1_data.append(player1.block_dictionary[number].won)
            player2_data.append(player2.block_dictionary[number].won)

    if len(player1_data) > 0:
        return np.corrcoef(player1_data, player2_data)[0,1]
    else:
        return None
    
def get_player_correlations(players):
    num_players = len(players)
    
    if num_players <= 1:
        return 'Not enough players for correlations!'
    
    message = '\n'

    for i in range(num_players):
        player_1 = players[i]

        for j in range(i+1, num_players):
            player_2 = players[j]
            correlation = get_player_correlation(player_2, player_2)

            if correlation == None:
                message += f'Players {player_1.name} and {player_2.name} have no common puzzles\n'
            else:
                message += f'Players {player_1.name} and {player_2.name} have correlation {correlation}\n'
    
    return message

parsed_file = 'parsed_text.py'

with open(parsed_file, 'rb') as fl:
    raw_blocks = pickle.load(fl)

name_player_dict = {}
number_puzzle_dict = {}
blocks = []

for raw_block in raw_blocks:
    block = Block(raw_block) # TODO add error handling
    blocks.append(block)
    name = block.name
    number = block.number
    
    if name not in name_player_dict:
        name_player_dict[name] = Player(name) 
    
    if block.number not in number_puzzle_dict:
        number_puzzle_dict[number] = Puzzle(number)

    name_player_dict[name].add_block(block)
    block.set_player(name_player_dict[name])

    number_puzzle_dict[number].add_block(block)
    block.set_puzzle(number_puzzle_dict[number])
    
players = list(name_player_dict.values())

for player in players:
    player.process_data()

puzzle_numbers = list(number_puzzle_dict.keys())
puzzle_numbers.sort()

def get_menu_string(puzzle_numbers):
    return input(
        f'''\nWelcome to the connections data menu. 
The first puzzle is {puzzle_numbers[0]}, the most recent puzzle is {puzzle_numbers[-1]}.
Options are:
    - Stats : print all player stats
    - Puzzle : examine a specific puzzle
    - Player : examine a specific player
    - Correlation : print player correlations
    - Cumulative : print the cumulative wins graph
    - Quit : quit\n\n'''
        ).lower()

def puzzle_menu(number_puzzle_dict, puzzle_numbers):
    first_puzzle = puzzle_numbers[0]
    latest_puzzle = puzzle_numbers[-1]

    print(f'''\nWelcome to the Puzzle menu, please enter a puzzle number. 
the earliest recorded puzzle is number {first_puzzle}, the most recent is number {latest_puzzle}''')
    
    number = int(input('\nNumber: '))

    if number in number_puzzle_dict:
        print()
        print(number_puzzle_dict[number])
    else:
        print('Puzzle number not found')

def player_menu(name_player_dict):
    print('\nWelcome to the Player menu, please enter a player name from the list below:\n')
    
    for name in name_player_dict.keys():
        print(name)
    
    name = input('\nName: ')

    if name in name_player_dict:
        print()
        print(name_player_dict[name])
    else:
        print('name not recognised')

active = True

while active:
    option = get_menu_string(puzzle_numbers)

    match option:
        case 'stats':
            for player in players:
                print(player)
            plot_player_histograms(players)
        
        case 'puzzle':
            puzzle_menu(number_puzzle_dict, puzzle_numbers)

        case 'player':
            player_menu(name_player_dict)

        case 'correlation':
            print(get_player_correlations(players))

        case 'cumulative':
            plot_cumulative_wins(players, puzzle_numbers)

        case 'quit':
            active = False
        
        case _:
            print('command not understood')

    if active:
        input('Press Enter to Continue:')