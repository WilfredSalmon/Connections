from Streak import Streak, Streak_Type

class Player:
    def __init__(self, name):
        self.name = name
        
        self.blocks = []
        self.block_dictionary = {}

        self.streaks = []
        self.scores = dict.fromkeys(range(-4, 6), 0)

        self.total_puzzles = 0
        self.total_wins = 0
        self.total_categories_found = 0
        self.total_attempts = 0
        self.total_score = 0

    def add_block(self, block):
        self.blocks.append(block)
        self.block_dictionary[block.number] = block
        
        self.update_stats(block)

    def update_stats(self, block):
        self.total_puzzles += 1
        self.total_wins += block.won
        self.total_categories_found += block.number_found
        self.total_attempts += block.attempts

        self.scores[block.score] += 1
        self.total_score += block.score

    def process_data(self):
        self.sort_blocks()
        self.find_streaks()
        self.set_longest_streak()
    
    def sort_blocks(self):
        self.blocks.sort(key = lambda x : x.number)
    
    def find_streaks(self):
        current_streak_length = 0
        current_streak_blocks = []
                
        for block in self.blocks:
            
            if block.won:
                current_streak_blocks.append(block)
                
                if len(current_streak_blocks) > 1:
                    if current_streak_blocks[-2].number + 1 == block.number:
                        current_streak_length += 1
                    
                    else:
                        self.streaks.append(Streak(current_streak_blocks, Streak_Type.INTERRUPTED))
                        current_streak_length = 1
                        current_streak_blocks = [block]
                
                else:
                    current_streak_length += 1
            
            elif current_streak_length > 0:
                current_streak_blocks.append(block)

                self.streaks.append(Streak(current_streak_blocks, Streak_Type.LOST))
                current_streak_length = 0
                current_streak_blocks = []

        if current_streak_length > 0:
            self.streaks.append(Streak(current_streak_blocks, Streak_Type.ONGOING))
            self.current_streak = self.streaks[-1]
        else:
            self.current_streak = None
    
    def set_longest_streak(self):
        if len(self.streaks) == 0:
            self.longest_streak = None
        else:
            self.streaks.sort(key = lambda x : x.length, reverse = True)
            self.longest_streak = self.streaks[0]

    def __repr__(self):
        win_percent = self.total_wins/self.total_puzzles
        avg_catergories_found = self.total_categories_found/self.total_puzzles
        avg_attempts = self.total_attempts/self.total_puzzles
        avg_score = self.total_score/self.total_puzzles

        return f'''Player {self.name} has submitted {self.total_puzzles} puzzles, with {self.total_wins} wins.
    They have a win rate of {win_percent:.0%}, finding on average {avg_catergories_found:.2f} catergories in {avg_attempts:.2f} attempts.
    They have a total score of {self.total_score}, with an average score of {avg_score:.2f}.
    They have score distribution {self.scores}
    Their longest streak is {get_streak_string(self.longest_streak)}
    Their current streak is {get_streak_string(self.current_streak)}\n'''

def get_streak_string(streak):
    if streak == None:
        return 'length 0 :('
    
    return streak.__repr__()
