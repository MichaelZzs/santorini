# from player import Player

class Space:
    def __init__(self, row, column):
        self._height = 0
        self._worker = None
        self._row = row
        self._column = column

    def height(self):
        return self._height

    def has_worker(self):
        if not self._worker:
            return False
        else:
            return True
        
    def update_worker(self, worker=None):
        self._worker = worker

    def build(self):
        self._height += 1

    def __str__(self):
        worker = " "
        if self.has_worker():
            worker = self._worker.get_name()
        return "|{}{}".format(self._height, worker)

class Board:
    def __init__(self):
        self._board = []
        for i in range(5):
            row = []
            for j in range(5):
                space = Space(i, j)
                row.append(space)
            self._board.append(row)

    def get_board(self):
        return self._board

    def print_board(self):
        print("+--+--+--+--+--+")
        for row in self._board:
            for space in row:
                print(space, end="")
            print("|")
            print("+--+--+--+--+--+")