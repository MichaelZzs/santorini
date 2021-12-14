from worker import Worker

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