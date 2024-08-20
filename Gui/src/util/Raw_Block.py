class Raw_Block():
    '''
        The raw block class should contain the important lines from the corresponding message. They are, in order:
            Line with message header
            Line with puzzle number
            Lines made up of only square emojis
    '''
    def __init__(self):
        self.lines = []

    def add_lines(self, lines_to_add):
        if type(lines_to_add) == str:
            self.lines.append(lines_to_add)
        else:
            self.lines.extend(lines_to_add)

    def __repr__(self):
        return '\n'.join(self.lines)