class BoardIterator:
    def __init__(self, board):
        self._spaces = []
        for row in board:
            for space in row:
                self._spaces.append(space)
        self._index = 0
    
    def __next__(self):
        if self._index == len(self._spaces):
            raise StopIteration()

        space = self._spaces[self._index]
        self._index += 1
        return space
    
    def __iter__(self):
        return self