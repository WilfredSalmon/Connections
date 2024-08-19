class Puzzle:
    def __init__(self, number):
        self.number = number
        
        self.blocks = []
        
        self.submissions = 0
        self.wins = 0
        self.number_found = 0
        self.attempts = 0
        
        self.players = {}

    def add_block(self, block):
        self.blocks.append(block)
        self.submissions += 1
        
        self.wins += block.won
        self.number_found += block.number_found
        self.attempts += block.attempts

    def add_player(self, player):
        self.players.append(player)

    def __repr__(self):
        win_percent = self.wins/self.submissions
        avg_catergories_found = self.number_found/self.submissions
        avg_attempts = self.attempts/self.submissions

        return f'''Puzzle Number {self.number}:
    {self.submissions} attempts registered, with a {win_percent:.1%} win percentage
    On average, {avg_catergories_found:.2f} categories found in {avg_attempts:.2f} attempts\n'''