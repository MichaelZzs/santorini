import sys

from player import Human, Random, Heuristic
from board import Board
from memento import Caretaker

directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]

class Santorini:
    def __init__(self, white="human", blue="human", undo="off", display="off"):
        self._board = Board()

        if display in ["on", "off"]:
            self._display = display

        if white == "human":
            self._player_1 = Human("white")
        elif white == "random":
            self._player_1 = Random("white")
        elif white == "heuristic":
            if display == "on":
                self._player_1 = Heuristic(color="white", display=True)
            else:
                self._player_1 = Heuristic(color="white")
        else:
            raise ValueError
        if blue == "human":
            self._player_2 = Human("blue")
        elif blue == "random":
            self._player_2 = Random("blue")
        elif blue == "heuristic":
            if display == "on":
                self._player_2 = Heuristic(color="blue", display=True)
            else:
                self._player_2 = Heuristic(color="blue")
        else:
            raise ValueError

        self._curr = self._player_1

        if undo in ["on", "off"]:
            self._undo = undo
        else:
            raise ValueError

        self._undo_redo_manager = Caretaker(self._board)

    def change_player(self):
        if self._curr == self._player_1:
            self._curr = self._player_2
        elif self._curr == self._player_2:
            self._curr = self._player_1

    def check_end(self):
        if self._board.get_worker("white", "A").get_height() >= 3 or self._board.get_worker("white", "B").get_height() >= 3:
            print("white has won")
            return True
        elif self._board.get_worker("blue", "Y").get_height() >= 3 or self._board.get_worker("blue", "Z").get_height() >= 3:
            print("blue has won")
            return True
        curr_workers = list(self._board.player_workers(self._curr.get_color()).values())
        for dir in directions:
            if self._board.check_viable_move(curr_workers[0], dir) or self._board.check_viable_move(curr_workers[1], dir):
                return False
        self.change_player()
        print("{} has won".format(self._curr.get_color()))
        return True

    def play(self):
        turn = 1
        while True:
            self._board.print_board()
            if self._display == "on":
                print("Turn: {}, {}, ".format(turn, self._curr), end="")
                height_score, center_score, distance_score = self._curr.player_score(self._board)
                print("({}, {}, {})".format(height_score, center_score, distance_score))
            else:
                print("Turn: {}, {}".format(turn, self._curr))
            if self.check_end():
                break

            if self._undo == "on":
                while True:
                    action = input("undo, redo, or next\n")
                    if action == "next":
                        self._curr.make_move(self._board)
                        self._undo_redo_manager.remove(turn)
                        self._undo_redo_manager.create()
                        turn += 1
                        self.change_player()
                        break
                    elif action == "undo":
                        success = self._undo_redo_manager.restore(turn - 2)
                        if success:
                            turn -= 1
                            self.change_player()
                        break
                    elif action == "redo":
                        success = self._undo_redo_manager.restore(turn)
                        if success:
                            turn += 1
                            self.change_player()
                        break
            else:
                self._curr.make_move(self._board)
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
        print("There can only be a maximum of 4 arguments!")
        raise ValueError
    
    game.play()
