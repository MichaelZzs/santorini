import sys
import os

from worker import Worker
from player import Player
from board import Space, Board

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

