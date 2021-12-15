from copy import deepcopy

from worker import Worker
from memento import Memento
from iterator import BoardIterator

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
        
    def get_worker(self):
        return self._worker

    def build(self):
        self._height += 1

    def __str__(self):
        worker = " "
        if self.has_worker():
            worker = self._worker.get_name()
        return "|{}{}".format(self._height, worker)

class Board:
    def __init__(self):
        self._state = []
        for i in range(5):
            row = []
            for j in range(5):
                space = Space(i, j)
                row.append(space)
            self._state.append(row)
        
        worker_a = Worker("A", 3, 1)
        self._state[3][1].update_worker(worker_a)
        worker_b = Worker("B", 1, 3)
        self._state[1][3].update_worker(worker_b)
        worker_y = Worker("Y", 1, 1)
        self._state[1][1].update_worker(worker_y)
        worker_z = Worker("Z", 3, 3)
        self._state[3][3].update_worker(worker_z)
        self._workers = {"white": {"A": worker_a, "B": worker_b}, "blue": {"Y": worker_y, "Z": worker_z}}

    def __iter__(self):
        return BoardIterator(self._state)

    def get_state(self):
        return self._state

    def player_workers(self, color):
        return self._workers[color]
    
    def get_worker(self, color, name):
        return self._workers[color][name]

    def print_board(self):
        print("+--+--+--+--+--+")
        for row in self._state:
            for space in row:
                print(space, end="")
            print("|")
            print("+--+--+--+--+--+")

    def check_viable_move(self, worker, direction):
        row_change, column_change = direction_dict[direction]
        old_space = self._state[worker._row][worker._column]
        new_row, new_column = worker._row + row_change, worker._column + column_change
        if new_row < 0 or new_row > 4 or new_column < 0 or new_column > 4:
            return False
        new_space = self._state[new_row][new_column]
        if new_space.height() > old_space.height() + 1 or new_space.has_worker():
            return False
        else:
            return True

    def check_viable_build(self, worker, direction):
        row_change, column_change = direction_dict[direction]
        build_row, build_column = worker._row + row_change, worker._column + column_change
        if build_row < 0 or build_row > 4 or build_column < 0 or build_column > 4:
            return False
        build_space = self._state[build_row][build_column]
        if build_space.height() >= 4 or build_space.has_worker():
            return False
        else:
            return True

    def all_viable_moves(self, worker):
        list = []
        for dir in directions:
            if self.check_viable_move(worker, dir):
                list.append(dir)
        return list

    def all_viable_builds(self, worker):
        list = []
        for dir in directions:
            if self.check_viable_build(worker, dir):
                list.append(dir)
        return list

    def move_worker(self, worker, direction):
        row_change, column_change = direction_dict[direction]
        new_row, new_column = worker._row + row_change, worker._column + column_change
        new_space = self._state[new_row][new_column]
        new_space.update_worker(worker)
        if worker._row != None:
            old_space = self._state[worker._row][worker._column]
            old_space.update_worker()
        worker.move(new_row, new_column)
        worker.set_height(new_space.height())

    def build(self, worker, direction):
        row_change, column_change = direction_dict[direction]
        build_row, build_column = worker._row + row_change, worker._column + column_change
        build_space = self._state[build_row][build_column]
        build_space.build()

    def new_space_height(self, worker, direction):
        row_change, column_change = direction_dict[direction]
        new_row, new_column = worker._row + row_change, worker._column + column_change
        new_space = self._state[new_row][new_column]
        return new_space.height()

    @property
    def memento(self):
        return Memento(deepcopy(self._state), deepcopy(self._workers))

    @memento.setter
    def memento(self, memento):
        self._state = deepcopy(memento.state)
        self._workers = deepcopy(memento.workers)