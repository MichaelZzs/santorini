import sys
import os

from worker import Worker
from player import Player
from board import Space, Board

directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]

direction_dict = {
    "n": (-1, 0),
    "ne": (-1, 1),
    "e": (0, 1),
    "se": (1, 1),
    "s": (1, 0),
    "sw": (1, -1),
    "w": (0, -1),
    "nw": (-1, -1)
}

class Play:
    def __init__(self):
        self._board = Board()
        # self._end = False

        worker_a = Worker("A")
        self.move_worker(worker_a, 3, 1)
        worker_b = Worker("B")
        self.move_worker(worker_b, 1, 3)
        worker_y = Worker("Y")
        self.move_worker(worker_y, 1, 1)
        worker_z = Worker("Z")
        self.move_worker(worker_z, 3, 3)

        self._player_1 = Player("white", worker_a, worker_b)
        self._player_2 = Player("blue", worker_y, worker_z)

        self._curr = self._player_1

    def move_worker(self, worker, row, column):
        new_space = self._board._board[row][column]
        new_space.update_worker(worker)
        if worker._row != None:
            old_space = self._board._board[worker._row][worker._column]
            old_space.update_worker()
        worker.move(row, column)
        worker.set_height(new_space.height())
        
    def change_player(self):
        if self._curr == self._player_1:
            self._curr = self._player_2
        elif self._curr == self._player_2:
            self._curr = self._player_1

    def check_end(self):
        if self._player_1.worker_1().get_height() >= 3 or self._player_1.worker_2().get_height() >= 3:
            print("{} has won".format(self._player_1._color))
            return True
        elif self._player_2.worker_1().get_height() >= 3 or self._player_2.worker_2().get_height() >= 3:
            print("{} has won".format(self._player_2._color))
            return True
        for dir in directions:
            if self.check_viable_move(self._curr.worker_1(), dir) or self.check_viable_move(self._curr.worker_2(), dir):
                return False
        self._change_player()
        print("{} has won".format(self._curr._color))
        return True

    def check_viable_move(self, worker, direction):
        row_change, column_change = direction_dict[direction]
        old_space = self._board._board[worker._row][worker._column]
        new_row, new_column = worker._row + row_change, worker._column + column_change
        if new_row < 0 or new_row > 4 or new_column < 0 or new_column > 4:
            return False
        new_space = self._board._board[new_row][new_column]
        if new_space.height() > old_space.height() + 1 or new_space.has_worker():
            return False
        else:
            return True

    def check_viable_build(self, worker, direction):
        row_change, column_change = direction_dict[direction]
        build_row, build_column = worker._row + row_change, worker._column + column_change
        if build_row < 0 or build_row > 4 or build_column < 0 or build_column > 4:
            return False
        else:
            return True

    def play(self):
        turn = 1
        while True:
            self._board.print_board()
            print("Turn: {}, {}".format(turn, self._curr))
            if self.check_end():
                break

            while True:
                name = input("Select a worker to move\n")
                if name not in ["A", "B", "Y", "Z"]:
                    print("Not a valid worker")
                elif name not in self._curr.viable_workers():
                    print("That is not your worker")
                else:
                    if self._curr.worker_1().get_name() == name:
                        worker = self._curr.worker_1()
                    elif self._curr.worker_2().get_name() == name:
                        worker = self._curr.worker_2()
                    break
            
            while True:
                move_dir = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
                if move_dir not in directions:
                    print("Not a valid direction")
                elif not self.check_viable_move(worker, move_dir):
                    print("Cannot move {}".format(move_dir))
                else:
                    row_change, column_change = direction_dict[move_dir]
                    self.move_worker(worker, worker._row + row_change, worker._column + column_change)
                    break

            while True:
                build_dir = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
                if build_dir not in directions:
                    print("Not a valid direction")
                elif not self.check_viable_build(worker, build_dir):
                    print("Cannot build {}".format(build_dir))
                else:
                    row_change, column_change = direction_dict[build_dir]
                    build_space = self._board._board[worker._row + row_change][worker._column + column_change]
                    if build_space.height() == 4 or build_space.has_worker():
                        print("Cannot build {}".format(build_dir))
                    else:
                        build_space.build()
                        break
            
            turn += 1
            self.change_player()



if __name__ == "__main__":
    # game = Play()
    # game._board.print_board()
    Play().play()
