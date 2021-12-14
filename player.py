# from worker import Worker
# from board import Board, Space
import random

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

class Player:
    def __init__(self, color, worker_1, worker_2):
        self._color = color
        self._worker_1 = worker_1
        self._worker_2 = worker_2
        if color == "white":
            self._viable_workers = ["A", "B"]
        elif color == "blue":
            self._viable_workers = ["Y", "Z"]
    
    def __str__(self):
        if self._color == "white":
            return "white (AB)"
        elif self._color == "blue":
            return "blue (YZ)"

    def viable_workers(self):
        return self._viable_workers

    def worker_1(self):
        return self._worker_1

    def worker_2(self):
        return self._worker_2

    def get_color(self):
        return self._color
    
    def check_viable_move(self, worker, direction, board):
        row_change, column_change = direction_dict[direction]
        old_space = board[worker._row][worker._column]
        new_row, new_column = worker._row + row_change, worker._column + column_change
        if new_row < 0 or new_row > 4 or new_column < 0 or new_column > 4:
            return False
        new_space = board[new_row][new_column]
        if new_space.height() > old_space.height() + 1 or new_space.has_worker():
            return False
        else:
            return True

    def check_viable_build(self, worker, direction, board):
        row_change, column_change = direction_dict[direction]
        build_row, build_column = worker._row + row_change, worker._column + column_change
        if build_row < 0 or build_row > 4 or build_column < 0 or build_column > 4:
            return False
        build_space = board[build_row][build_column]
        if build_space.height() >= 4 or build_space.has_worker():
            return False
        else:
            return True

    def move_worker(self, worker, row, column, board):
        new_space = board[row][column]
        new_space.update_worker(worker)
        if worker._row != None:
            old_space = board[worker._row][worker._column]
            old_space.update_worker()
        worker.move(row, column)
        worker.set_height(new_space.height())

    def all_viable_moves(self, worker, board):
        list = []
        for dir in directions:
            if self.check_viable_move(worker, dir, board):
                list.append(dir)
        return list

    def all_viable_builds(self, worker, board):
        list = []
        for dir in directions:
            if self.check_viable_build(worker, dir, board):
                list.append(dir)
        return list

    def make_move(self):
        raise NotImplementedError


class Human(Player):
    def __init__(self, color, worker_1, worker_2):
        super().__init__(color, worker_1, worker_2)

    def make_move(self, board):
        while True:
            name = input("Select a worker to move\n")
            if name not in ["A", "B", "Y", "Z"]:
                print("Not a valid worker")
            elif name not in self.viable_workers():
                print("That is not your worker")
            else:
                if self.worker_1().get_name() == name:
                    worker = self.worker_1()
                elif self.worker_2().get_name() == name:
                    worker = self.worker_2()
                break
        
        while True:
            move_dir = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if move_dir not in directions:
                print("Not a valid direction")
            elif not self.check_viable_move(worker, move_dir, board):
                print("Cannot move {}".format(move_dir))
            else:
                row_change, column_change = direction_dict[move_dir]
                self.move_worker(worker, worker._row + row_change, worker._column + column_change, board)
                break

        while True:
            build_dir = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if build_dir not in directions:
                print("Not a valid direction")
            elif not self.check_viable_build(worker, build_dir, board):
                print("Cannot build {}".format(build_dir))
            else:
                row_change, column_change = direction_dict[build_dir]
                build_space = board[worker._row + row_change][worker._column + column_change]
                if build_space.height() == 4 or build_space.has_worker():
                    print("Cannot build {}".format(build_dir))
                else:
                    build_space.build()
                    break


class Random(Player):
    def __init__(self, color, worker_1, worker_2):
        super().__init__(color, worker_1, worker_2)

    def make_move(self, board):
        choice = random.choice([1, 2])
        if choice == 1:
            worker = self._worker_1
        elif choice == 2:
            worker = self._worker_2

        viable_moves = self.all_viable_moves(worker, board)
        if len(viable_moves) == 0:
            if choice == 1:
                worker = self._worker_2
                viable_moves = self.all_viable_moves(worker, board)
            elif choice == 2:
                worker = self._worker_1
                viable_moves = self.all_viable_moves(worker, board)
        move_dir = random.choice(viable_moves)
        row_change, column_change = direction_dict[move_dir]
        self.move_worker(worker, worker._row + row_change, worker._column + column_change, board)

        viable_builds = self.all_viable_builds(worker, board)
        build_dir = random.choice(viable_builds)
        row_change, column_change = direction_dict[build_dir]
        build_space = board[worker._row + row_change][worker._column + column_change]
        build_space.build()
        
        print("{},{},{}".format(worker.get_name(), move_dir, build_dir))