from functools import reduce
from random import choice


class SudokuSolver:
    locks_obj = {}

    def __init__(self, sudoku_table) -> None:
        self.sudoku_table = sudoku_table

    def run(self):
        empties = reduce(lambda acc, item: acc + item, [[(col_index, row_index) for col_index, cell in enumerate(row) if not cell]
                                                        for row_index, row in enumerate(self.sudoku_table)], [])
        if not empties:
            return self.sudoku_table
        pos = 0
        self.choose_answers(empties[pos])
        while True:
            if pos == len(empties) - 1:
                return self.sudoku_table
            elif pos < -1:
                return None
            pos += 1
            t = SudokuSolver.locks_obj.get(
                pos) if SudokuSolver.locks_obj.get(pos) else []
            if self.choose_answers(empties[pos], t):
                if not SudokuSolver.locks_obj:
                    SudokuSolver.locks_obj = {
                        pos - 1: [self.sudoku_table[empties[pos - 1][1]][empties[pos - 1][0]]]}
                else:
                    if SudokuSolver.locks_obj.get(pos - 1):
                        SudokuSolver.locks_obj[pos - 1].append(
                            self.sudoku_table[empties[pos - 1][1]][empties[pos - 1][0]])
                    else:
                        SudokuSolver.locks_obj[pos - 1] = [self.sudoku_table[
                            empties[pos - 1][1]][empties[pos - 1][0]]]
                self.sudoku_table[empties[pos - 1][1]][empties[pos - 1][0]] = 0
                pos -= 2
            else:
                for key in list(filter(lambda key: key > pos, SudokuSolver.locks_obj.keys())):
                    del SudokuSolver.locks_obj[key]

    def choose_answers(self, pos, e=[]):
        rx = pos[0] // 3
        ry = pos[1] // 3
        all_answers = list(range(1, 10))
        v_filter = [self.sudoku_table[i][pos[0]]
                    for i in range(9) if self.sudoku_table[i][pos[0]]]
        h_filter = [i for i in self.sudoku_table[pos[1]] if i]
        square_filter = []
        for i in range(3):
            for j in range(3):
                if ry == i and rx == j:
                    for cell in [self.sudoku_table[y + 3*i][x + 3*j] for x in range(3) for y in range(3)]:
                        square_filter.append(cell)
        square_filter = [cell for cell in square_filter if cell != 0]
        filtered_list = [
            answer for answer in all_answers if answer not in square_filter + v_filter + h_filter + e]
        if not filtered_list:
            return True
        self.sudoku_table[pos[1]][pos[0]] = choice(filtered_list)
