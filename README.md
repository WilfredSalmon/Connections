# NYT connections

## Description:
Have you and your friends been sending the results of your NYT connections puzzles to each other in a whataspp group? Do you want to know how well everyone is doing? Do you want to ruin the fun, lighthearted nature of the game with stats?? If so, then this is the script for you. Given a copy of your whatsapp chat, this script will trawl through and extract data on everyone who has sent a puzzle to the chat, including win percentages, streaks (consecutive wins), scores (performance) and cumulative wins. What fun! 

## Requires:
- Python >= 3.10
- matplotlib
- numpy

## Instructions:
1. Clone the repository
2. Export the whatsapp chat (without media), save the exported file as `_chat.txt` in the repository folder
3. Run `data_extraction.py`, double check that the last NYT connections puzzle that was sent in the chat is printed to the console
4. Run `data_analysis.py` - follow the console instructions