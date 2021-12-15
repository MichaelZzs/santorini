class Worker:
    def __init__(self, name, row, column):
        self._name = name
        self._row = row
        self._column = column
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
    
    def get_row(self):
        return self._row

    def get_column(self):
        return self._column