class Worker:
    def __init__(self, name):
        self._name = name
        self._row = None
        self._column = None
        self._height = 0
    
    def move(self, row, column):
        self._row = row
        self._column = column

    def build(self, direction):
        pass

    def get_name(self):
        return self._name

    def set_height(self, height):
        self._height = height

    def get_height(self):
        return self._height