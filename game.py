from misc.sudoku import Sudoku
from misc.sudoku_solver import SudokuSolver
from random import randint
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo, showwarning
from copy import deepcopy


class GUI:
    scale = 270

    def __init__(self):
        self.root = Tk()
        cells_container = Frame(self.root)
        cells_container.grid(row=0, column=0)
        self.cells_list = []
        for row_index in range(9):
            row_frame = Frame(cells_container)
            row_frame.grid(row=row_index, column=0)
            self.cells_list.append([])
            for cell_index in range(9):
                cell_entry = Entry(row_frame, font=int(GUI.scale/10.8), width=int(GUI.scale/135), highlightbackground='lightgray',
                                   highlightthickness=1, fg='black',
                                   state='readonly'
                                   )
                self.cells_list[row_index].append(cell_entry)
                cell_entry.grid(row=0, column=cell_index)
        panel = Frame(self.root)
        dif = IntVar(self.root, 2)
        difficulty = Frame(panel, width=GUI.scale/3, height=GUI.scale/270)
        difficulty.grid(row=0, column=0)
        easy_dif = Radiobutton(difficulty, text='easy', variable=dif, value=1)
        easy_dif.grid(row=0, column=0)
        easy_dif.anchor(W)
        normal_dif = Radiobutton(
            difficulty, text='normal', variable=dif, value=2)
        normal_dif.grid(row=0, column=1)
        normal_dif.anchor(W)
        hard_dif = Radiobutton(difficulty, text='hard', variable=dif, value=3)
        hard_dif.grid(row=0, column=2)
        hard_dif.anchor(W)
        gen_button = Button(panel, width=int(35*GUI.scale/270), height=int(GUI.scale/270), text='generate',
                            command=lambda: self.gen_sudoku(dif.get()))
        gen_button.grid(row=1, column=0)
        solve_button = Button(panel, width=int(35*GUI.scale/270), height=int(GUI.scale/270), text='solve',
                              command=self.solve_sudoku)
        solve_button.grid(row=2, column=0)
        open_button = Button(panel, width=int(35*GUI.scale/270), height=int(GUI.scale/270), text='open',
                             command=self.open_sudoku)
        open_button.grid(row=3, column=0)
        check_button = Button(panel, width=int(35*GUI.scale/270), height=int(GUI.scale/270), text='check',
                              command=self.check_sudoku)
        check_button.grid(row=4, column=0)
        panel.grid(row=1, column=0)

    def gen_sudoku(self, dif=1):
        sudoku = Sudoku()
        self.sudoku_table = sudoku.run()
        for _ in range(10*(dif + 2)):
            random_cell = (randint(0, 8), randint(0, 8))
            while not self.sudoku_table[random_cell[1]][random_cell[0]]:
                random_cell = (randint(0, 8), randint(0, 8))
            self.sudoku_table[random_cell[1]][random_cell[0]] = 0
        for row_index, row in enumerate(self.cells_list):
            for cell_index, cell_entry in enumerate(row):
                cell_entry.config(state='normal', fg='black')
                cell_entry.delete(0, END)
                if self.sudoku_table[row_index][cell_index]:
                    cell_entry.insert(
                        0, self.sudoku_table[row_index][cell_index])
                    cell_entry.config(state='readonly')
                else:
                    cell_entry.config(fg='red')
                    cell_entry.insert(0, '')

    def solve_sudoku(self):
        try:
            stc = deepcopy(self.sudoku_table)
        except AttributeError:
            showerror('Sudoku', 'invalid input')
            return
        sudoku_solver = SudokuSolver(self.sudoku_table)
        solved_sudoku = sudoku_solver.run()
        if not (solved_sudoku := sudoku_solver.run()):
            showerror('Sudoku', 'unsolvable input')
            return
        for row_index, row in enumerate(stc):
            for cell_index, cell in enumerate(row):
                cell_entry = self.cells_list[row_index][cell_index]
                if not cell:
                    cell_entry.delete(0, END)
                    cell_entry.config(fg='red')
                    cell_entry.insert(
                        0, solved_sudoku[row_index][cell_index])

    def open_sudoku(self):
        with fd.askopenfile() as f:
            self.sudoku_table = [list(eval(row))
                                 for row in f.read().split('\n')]
            for row_index, row in enumerate(self.sudoku_table):
                for cell_index, cell in enumerate(row):
                    cell_entry = self.cells_list[row_index][cell_index]
                    cell_entry.config(
                        state='normal', fg='black')
                    cell_entry.delete(0, END)
                    if cell:
                        cell_entry.insert(
                            0, self.sudoku_table[row_index][cell_index])
                        cell_entry.config(state='readonly')
                    else:
                        cell_entry.config(fg='red')

    def check_sudoku(self):
        check_flag = True
        try:
            sudoku_final_input = list(map(lambda row: list(
                map(lambda cell_entry: int(cell_entry.get()) if cell_entry.get() else 0, row)), self.cells_list))
            for row in sudoku_final_input:
                if len(set(row)) < len(row):
                    check_flag = False
            for i in range(9):
                if len(set([row[i] for row in sudoku_final_input])) < len(
                        [row[i] for row in sudoku_final_input]):
                    check_flag = False
            for i in range(3):
                for j in range(3):
                    print([sudoku_final_input[x + 3*i][y + 3*j]
                           for x in range(3) for y in range(3)])
                    if len(set([sudoku_final_input[x + 3*i][y + 3*j]
                                for x in range(3) for y in range(3)])) < len([sudoku_final_input[x + 3*i][y + 3*j]
                                                                              for x in range(3) for y in range(3)]):
                        check_flag = False
        except ValueError:
            check_flag = False
        if check_flag:
            showinfo('Sudoku', 'Correct!')
        else:
            showwarning('Sudoku', 'Wrong!')


gui = GUI()
gui.root.mainloop()
