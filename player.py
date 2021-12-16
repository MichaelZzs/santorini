import random
from abc import ABC, abstractmethod

directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
opposite_move = {"n":"s", 
             "ne":"sw", 
             "e":"w",
             "se":"nw",
             "s":"n",
             "sw":"ne",
             "w":"e",
             "nw":"se"}

def dist(x1, y1, x2, y2):
    """
    x1, y1 are your coords
    x2, y2 are comparison coords
    """
    x = abs(x1 - x2)
    y = abs(y1 - y2)

    return max(x, y)

class Player(ABC):
    def __init__(self, color):
        self._color = color
    
    def __str__(self):
        if self._color == "white":
            return "white (AB)"
        elif self._color == "blue":
            return "blue (YZ)"

    def viable_workers(self):
        if self._color == "white":
            return ["A", "B"]
        elif self._color == "blue":
            return ["Y", "Z"]

    def get_color(self):
        return self._color

    def player_score(self, board):
        """
        Displayed score
        """
        # partner
        workers = list(board.player_workers(self._color).values())
        worker = workers[0]
        worker2 = self._get_partner_worker(worker, board)

        # score1
        height_score = self._get_height_score(worker) + self._get_height_score(worker2)

        # score2
        center_score = self._get_center_score(worker) + self._get_center_score(worker2)

        # score3 - can use board, iterate through each space and do a O(N^2) search each time to find enemies
        distance_score = self._get_distance_score(worker, board)

        return height_score, center_score, distance_score

    def _get_height_score(self, worker):
        return worker.get_height()

    def _get_center_score(self, worker):
        row = worker.get_row()
        column = worker.get_column()
        return 2 - dist(row, column, 2, 2)

    def _get_distance_score(self, worker, board):
        """
        Distance scores for both workers
        """
        row = worker.get_row()
        column = worker.get_column()

        partner_location = self._get_partner_location(worker, board)
        enemy_locations = self._get_enemy_locations(worker, board)
        enemy1 = enemy_locations[0]
        enemy2 = enemy_locations[1]
        distance_score = 8 - min(dist(row, column, enemy1[0], enemy1[1]), dist(partner_location[0], 
                                 partner_location[1], enemy1[0], enemy1[1])) - min(dist(row, column, enemy2[0], enemy2[1]), 
                                                                                   dist(partner_location[0], partner_location[1], enemy2[0], enemy2[1]))
        return distance_score

    def _get_enemy_locations(self, worker, board):
        # Find enemy names
        name = worker.get_name()
        if name in ['A', 'B']:
            enemies = ['Y', 'Z']
        else:
            enemies = ['A', 'B']
        
        # Get locations of enemies
        locs = []
        for space in board:
            worker = space.get_worker()
            if worker and worker.get_name() in enemies:
                enemy_row = worker.get_row()
                enemy_column = worker.get_column()
                locs.append((enemy_row, enemy_column))

        return locs

    def _get_partner_location(self, worker, board):
        # Find partner name
        name = worker.get_name()
        if name == 'A':
            helper = 'B'
        elif name == 'B':
            helper = 'A'
        elif name == 'Y':
            helper = 'Z'
        elif name == 'Z':
            helper = 'Y'

        # Get location of partner
        for space in board:
            worker = space.get_worker()
            if worker and worker.get_name() == helper:
                helper_row = worker.get_row()
                helper_column = worker.get_column()
                return (helper_row, helper_column)

    def _get_partner_worker(self, worker, board):
        # Find partner name
        name = worker.get_name()
        if name == 'A':
            helper = 'B'
        elif name == 'B':
            helper = 'A'
        elif name == 'Y':
            helper = 'Z'
        elif name == 'Z':
            helper = 'Y'

        # Get location of partner
        for space in board:
            worker = space.get_worker()
            if worker and worker.get_name() == helper:
                return worker

    @abstractmethod
    def make_move(self, board):
        pass


class Human(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_move(self, board):
        while True:
            name = input("Select a worker to move\n")
            if name not in ["A", "B", "Y", "Z"]:
                print("Not a valid worker")
            elif name not in self.viable_workers():
                print("That is not your worker")
            else:
                worker = board.get_worker(self._color, name)
                break

        while True:
            move_dir = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            if move_dir not in directions:
                print("Not a valid direction")
            elif not board.check_viable_move(worker, move_dir):
                print("Cannot move {}".format(move_dir))
            else:
                board.move_worker(worker, move_dir)
                break

        while True:
            build_dir = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
            if build_dir not in directions:
                print("Not a valid direction")
            elif not board.check_viable_build(worker, build_dir):
                print("Cannot build {}".format(build_dir))
            else:
                board.build(worker, build_dir)
                break


class Random(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_move(self, board):
        workers = list(board.player_workers(self._color).values())
        worker_1, worker_2 = workers[0], workers[1]

        total_viable_moves_num = len(board.all_viable_moves(worker_1)) + len(board.all_viable_moves(worker_2))
        choice = random.randint(1, total_viable_moves_num)
        if choice <= len(board.all_viable_moves(worker_1)):
            worker = worker_1
        else:
            worker = worker_2

        move_dir = random.choice(board.all_viable_moves(worker))
        board.move_worker(worker, move_dir)
        
        build_dir = random.choice(board.all_viable_builds(worker))
        board.build(worker, build_dir)
        print("{},{},{}".format(worker.get_name(), move_dir, build_dir))


class Heuristic(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_move(self, board):
        scores = []
        workers = list(board.player_workers(self._color).values())

        worker_1 = workers[0]
        viable_moves = board.all_viable_moves(worker_1)
        for move in viable_moves:
            score = self.calculate_score(worker_1, move, board)
            scores.append((score, move, 1))

        worker_2 = workers[1]
        viable_moves = board.all_viable_moves(worker_2)
        for move in viable_moves:
            score = self.calculate_score(worker_2, move, board)
            scores.append((score, move, 2))

        random.shuffle(scores)
        score, move_dir, worker_id = max(scores, key=lambda x: x[0])
        if worker_id == 1:
            worker = worker_1
        else:
            worker = worker_2
        
        board.move_worker(worker, move_dir)

        viable_builds = board.all_viable_builds(worker)
        build_dir = random.choice(viable_builds)
        board.build(worker, build_dir)
        print("{},{},{}".format(worker.get_name(), move_dir, build_dir))

    def calculate_score(self, worker, move, board):
        """
        Move score
        """
        # Check if move guarantees victory
        if board.new_space_height(worker, move) == 3:
            return 10000000

        # move here
        board.move_worker(worker, move)

        # score1
        height_score = self._get_height_score(worker)

        # score2
        center_score = self._get_center_score(worker)

        # score3 - can use board, iterate through each space and do a O(N^2) search each time to find enemies
        distance_score = self._get_distance_score_self(worker, board)

        # move back
        move_back = opposite_move[move]
        board.move_worker(worker, move_back)

        score = 3 * height_score + 2 * center_score + 1 * distance_score
        return score

    def _get_distance_score_self(self, worker, board):
        """
        Distance score for one worker
        """
        row = worker.get_row()
        column = worker.get_column()

        enemy_locations = self._get_enemy_locations(worker, board)
        enemy1 = enemy_locations[0]
        enemy2 = enemy_locations[1]

        distance_score = 8 - dist(row, column, enemy1[0], enemy1[1]) - dist(row, column, enemy2[0], enemy2[1])
        return distance_score