import sys
import os

from worker import Worker
from player import Player, Human, Random
from board import Space, Board

directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]

class Santorini:
    def __init__(self, white="human", blue="human", undo="off", display="off"):
        self._board = Board()

        worker_a = Worker("A")
        self.move_worker(worker_a, 3, 1)
        worker_b = Worker("B")
        self.move_worker(worker_b, 1, 3)
        worker_y = Worker("Y")
        self.move_worker(worker_y, 1, 1)
        worker_z = Worker("Z")
        self.move_worker(worker_z, 3, 3)

        if white == "human":
            self._player_1 = Human("white", worker_a, worker_b)
        elif white == "random":
            self._player_1 = Random("white", worker_a, worker_b)
        elif white == "heuristic":
            pass
        else:
            raise ValueError
        if blue == "human":
            self._player_2 = Human("blue", worker_y, worker_z)
        elif blue == "random":
            self._player_2 = Random("blue", worker_y, worker_z)
        elif blue == "heuristic":
            pass
        else:
            raise ValueError

        self._curr = self._player_1

    def move_worker(self, worker, row, column):
        new_space = self._board.get_board()[row][column]
        new_space.update_worker(worker)
        if worker._row != None:
            old_space = self._board.get_board()[worker._row][worker._column]
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
            print("{} has won".format(self._player_1.get_color()))
            return True
        elif self._player_2.worker_1().get_height() >= 3 or self._player_2.worker_2().get_height() >= 3:
            print("{} has won".format(self._player_2.get_color()))
            return True
        for dir in directions:
            if self._curr.check_viable_move(self._curr.worker_1(), dir, self._board.get_board()) or self._curr.check_viable_move(self._curr.worker_2(), dir, self._board.get_board()):
                return False
        self.change_player()
        print("{} has won".format(self._curr.get_color()))
        return True


    def play(self):
        turn = 1
        while True:
            self._board.print_board()
            print("Turn: {}, {}".format(turn, self._curr))
            if self.check_end():
                break

            self._curr.make_move(self._board.get_board())
            turn += 1
            self.change_player()



if __name__ == "__main__":
    if len(sys.argv) == 1:
        game = Santorini()
    elif len(sys.argv) == 2:
        game = Santorini(sys.argv[1])
    elif len(sys.argv) == 3:
        game = Santorini(sys.argv[1], sys.argv[2])        
    elif len(sys.argv) == 4:
        game = Santorini(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        game = Santorini(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("There can only be maximum of 4 arguments!")
        raise ValueError
    
    game.play()
