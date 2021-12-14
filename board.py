from player import Player

class Space:
    def __init__(self, row, column):
        self._height = 0
        self._worker = None
        self._row = row
        self._column = column

    def has_worker(self):
        if not self._worker:
            return False
        else:
            return True
        
    def place_worker(self, worker):
        self._worker = worker
    
    def remove_worker(self):
        self._worker = None

    def print_space(self):
        if not self.has_worker():
            print("|{} ".format(self._height), end="")
        else:
            print("|{}{}".format(self._height, self._worker.get_name()), end="")


class Board:
    def __init__(self):
        self._board = []
        for i in range(5):
            row = []
            for j in range(5):
                space = Space(i, j)
                row.append(space)
            self._board.append(row)

    def print_board(self):
        print("+--+--+--+--+--+")
        for row in self._board:
            for space in row:
                space.print_space()
            print("|")
            print("+--+--+--+--+--+")