from random import choice


def pos_to_loc(pos):
    return (pos % 9, pos // 9)


class Sudoku:
    locks_obj = {}
    locked_cell = None

    def __init__(self):
        self.sudoku_table = [
            [0 for _ in range(9)] for _ in range(9)]

    def run(self):
        pos = 0
        self.choose(pos)
        while True:
            if pos == 80:
                return self.sudoku_table
            pos += 1
            t = Sudoku.locks_obj.get(pos) if Sudoku.locks_obj.get(pos) else []
            if not [cell for cell in list(range(1, 10))
                    if cell not in self.filter_choices(pos, self.sudoku_table, t)]:
                if not Sudoku.locked_cell:
                    Sudoku.locked_cell = pos
                if not Sudoku.locks_obj:
                    Sudoku.locks_obj = {pos - 1: [self.sudoku_table[pos_to_loc(pos - 1)[1]][pos_to_loc(pos - 1)[
                        0]]]}
                else:
                    if Sudoku.locks_obj.get(pos - 1):
                        Sudoku.locks_obj[pos - 1].append(self.sudoku_table[pos_to_loc(pos - 1)[
                            1]][pos_to_loc(pos - 1)[0]])
                    else:
                        Sudoku.locks_obj[pos - 1] = [self.sudoku_table[pos_to_loc(
                            pos - 1)[1]][pos_to_loc(pos - 1)[0]]]
                self.sudoku_table[pos_to_loc(
                    pos - 1)[1]][pos_to_loc(pos - 1)[0]] = 0
                pos -= 2
            else:
                if Sudoku.locked_cell == pos:
                    Sudoku.locked_cell = None
                    Sudoku.locks_obj = {}
                for key in list(filter(lambda key: key > pos, Sudoku.locks_obj.keys())):
                    del Sudoku.locks_obj[key]
                self.choose(pos)

    def choose(self, pos):
        filter_choices = self.filter_choices(pos, self.sudoku_table)
        all_choices = list(range(1, 10))
        filtered_choices = list(filter(
            lambda choice: choice not in filter_choices, all_choices))
        self.sudoku_table[pos_to_loc(pos)[1]][pos_to_loc(
            pos)[0]] = choice(filtered_choices)

    def filter_choices(self, pos, table, e=[]):
        rx = pos_to_loc(pos)[0] // 3
        ry = pos_to_loc(pos)[1] // 3
        h_filter = table[pos_to_loc(
            pos)[1]][0:pos_to_loc(pos)[0]]
        v_filter = [table[i][pos_to_loc(pos)[0]]
                    for i in range(pos_to_loc(pos)[1])]
        square_filter = []
        for i in range(3):
            for j in range(3):
                if ry == i and rx == j:
                    for cell in [table[y + 3*i][x + 3*j] for x in range(3) for y in range(3) if y + 3*i < pos_to_loc(pos)[1] or x + 3*j < pos_to_loc(pos)[0]]:
                        square_filter.append(cell)
        square_filter = [cell for cell in square_filter if cell != 0]
        return v_filter + h_filter + square_filter + e
