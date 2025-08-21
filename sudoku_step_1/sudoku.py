'''Sudoku game built with python'''

import tkinter as tk
from tkinter import font

class SudokuBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sudoku Game')
        self._cells = {}
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

def main():
    board = SudokuBoard()
    board.geometry('400x500')
    board.mainloop()

if __name__ == '__main__':
    main()
