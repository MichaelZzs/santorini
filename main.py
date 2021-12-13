import sys
import os

class Worker:
    def __init__(self, name):
        self._name = name
        self._row = None
        self._column = None
    
    def move(self, row, column):
        self._row = row
        self._column = column

    def build(self, direction):
        pass

    def get_name(self):
        return self._name


class Player:
    def __init__(self, color, worker_1, worker_2):
        self._color = color
        self._worker_1 = worker_1
        self._worker_2 = worker_2


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
        

class Play:
    def __init__(self):
        self._board = Board()

        worker_a = Worker("A")
        self.move_worker(worker_a, 3, 1)
        worker_b = Worker("B")
        self.move_worker(worker_b, 1, 3)
        worker_y = Worker("Y")
        self.move_worker(worker_y, 1, 1)
        worker_z = Worker("Z")
        self.move_worker(worker_z, 3, 3)

        player_1 = Player("white", worker_a, worker_b)
        player_2 = Player("blue", worker_y, worker_z)

    def move_worker(self, worker, row, column):
        worker.move(row, column)
        space = self._board._board[row][column]
        space.place_worker(worker)
        


if __name__ == "__main__":
    game = Play()
    game._board.print_board()
#     white = blue = undo = display = None
#     if len(sys.argv) < 2:
#         white = "human"
#     else:
#         white = sys.argv[1]
#     if len(sys.argv) < 3:
#         blue = "human"
#     else:
#         blue = sys.argv[2]
#     if len(sys.argv) < 4:
#         undo = "human"
#     else:
#         undo = sys.argv[3]
#     if len(sys.argv) < 5:
#         display = "human"
#     else:
#         display = sys.argv[4]

#     game = Santorini(white, blue, undo, display)
#     game.run()

