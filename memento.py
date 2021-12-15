class Memento:
    def __init__(self, state, workers):
        self.state = state
        self.workers = workers

class Caretaker:
    def __init__(self, board):
        self._board = board
        self._mementos = []
        self.create()

    def create(self):
        memento = self._board.memento
        self._mementos.append(memento)

    def restore(self, index):
        if index >= 0 and index < len(self._mementos):
            memento = self._mementos[index]
            self._board.memento = memento
            return True
        else:
            return False

    def remove(self, turn):
        #removes all mementos after turn
        if len(self._mementos) > turn:
            for i in range(len(self._mementos) - turn):
                self._mementos.pop()