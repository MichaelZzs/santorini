class AbstractCommand():
    def execute(self):
        raise NotImplementedError

class NextCommand(AbstractCommand):
    def __init__(self, caretaker, player, turn, board, func):
        self._caretaker = caretaker
        self._player = player
        self._turn = turn
        self._board = board
        self._func = func

    def execute(self):
        self._player.make_move(self._board)
        self._caretaker.remove(self._turn)
        self._caretaker.create()
        self._func()
        return self._turn + 1


class UndoCommand(AbstractCommand):
    def __init__(self, caretaker, turn, func):
        self._caretaker = caretaker
        self._turn = turn
        self._func = func

    def execute(self):
        success = self._caretaker.restore(self._turn - 2)
        if success:
            self._func()
            return self._turn - 1
        
        else:
            return -1


class RedoCommand(AbstractCommand):
    def __init__(self, caretaker, turn, func):
        self._caretaker = caretaker
        self._turn = turn
        self._func = func

    def execute(self):
        success = self._caretaker.restore(self._turn)
        if success:
            self._func()
            return self._turn + 1

        else:
            return -1