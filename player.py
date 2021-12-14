from worker import Worker


class Player:
    def __init__(self, color, worker_1, worker_2):
        self._color = color
        self._worker_1 = worker_1
        self._worker_2 = worker_2
