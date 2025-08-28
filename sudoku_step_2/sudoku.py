'''Sudoku game built with python'''

import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
from tkinter import font
from typing import NamedTuple

import random 

class Move(NamedTuple):
    row: int
    col: int
    label: str =""

class SudokuBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title('Sudoku Game')
        self._cells = {}
        self._game = game
        self._create_board_display()
        self._create_board_grid()
    
    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text='Sudoku',
            font=font.Font(size=18, weight='bold'),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame =  tk.Frame(master=self)
        grid_frame.pack(expand=True, fill=tk.BOTH)
        for row in range(9):
            grid_frame.rowconfigure(row, weight=1, minsize=50)
            grid_frame.columnconfigure(row, weight=1, minsize=50)
            for col in range(9):            
                button = tk.Button(
                    master=grid_frame,
                    text='',
                    font=font.Font(size=18, weight='bold'),
                    fg='black',
                    bg='white',
                    relief='solid',
                    borderwidth=1,
                )
                self._cells[button] = (row, col)
                button.grid(
                    row=row,
                    column=col,
                    padx=0,
                    pady=0,
                    sticky="nsew"
                )

                button.config(command=lambda b=button: self._on_cell_click(b))

    def _on_cell_click(self, button):
        row, col = self._cells[button]

        if (row,col) in self._game._initial_values:
            return
        
        value = simpledialog.askstring("Input", f"Número para la celda ({row + 1},{col + 1}) [1-9 o vacío]:")
        if not value:
            button.config(text="")
            self._game._current_moves[row][col] = Move(row, col, "")
        elif value.isdigit() and 1 <=  int(value) <= 9:
            button.config(text=value)
            self._game._current_moves[row][col] = Move(row,col, value)
        else:
            messagebox.showerror("Error", "Debe ser un número del 1 al 9 o vacío.")


    def display_numbers(self, moves_matrix):
        for row in moves_matrix:
            for move in row:
                if move.label:  # si no está vacío
                    # buscar el botón correspondiente
                    for button, (r, c) in self._cells.items():
                        if r == move.row and c == move.col:
                            button.config(text=str(move.label))




class SudokuGame:
    def __init__(self):
        self._initial_values = []
        self._current_moves = []
        self._is_game_over = False
        self._gen_init_board()
        self._set_up_board()
        

    #Methods to Fill randomly positions 
    def _generate_numbers(self):
        return random.randint(1, 9)

    def _generate_coord(self):
        '''Generates random coordinates to start the game'''
        total = self._generate_numbers()
        # generate pairs (x, y) directly
        fill = [(self._generate_numbers(), self._generate_numbers()) for _ in range(total)]
        
        # generate point for each row
        coords = self._coords_to_fill(fill)
        
        return coords

    def _coords_to_fill(self ,arr):
        '''Helper method to generate coordinates
        @arr list of (x, y)
        '''
        coords = []
        for x, y in arr:
            for _ in range(x):  # loop x times
                coords.append((self._generate_numbers(), y))
        return coords

    def _gen_init_board(self):
        self._initial_values = self._generate_coord()
        

    def _set_up_board(self):
        self._current_moves = [
            [Move(row,col,self._generate_numbers()) \
                               if (row, col) in self._initial_values else Move(row,col)\
                                for col in range(9)]
                                for row in range(9)
                                ]
    
    def get_initial_board(self):
        return self._current_moves


def main():
    game = SudokuGame()
    board = SudokuBoard(game)
    board.geometry('400x500')
    board.display_numbers(game.get_initial_board())
    board.mainloop()

if __name__ == '__main__':
    main()
