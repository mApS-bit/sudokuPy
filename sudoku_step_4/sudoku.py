import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import font
from typing import NamedTuple
import random

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

class SudokuBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title('Sudoku Game')
        self._cells = {}
        self._buttons_by_coord = {}
        self._game = game
        self._selected_cell = None
        self._create_board_display()
        self._create_board_grid()
        self._create_key_bindings()
    
    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text='Sudoku - Haz clic en una celda y luego presiona un número (1-9) o Borrar',
            font=font.Font(size=12, weight='bold'),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack(expand=True, fill=tk.BOTH)
        for row in range(9):
            grid_frame.rowconfigure(row, weight=1, minsize=50)
            grid_frame.columnconfigure(row, weight=1, minsize=50)
            for col in range(9):
                # Configurar colores de fondo para los bloques 3x3
                bg_color = 'white'
                if (row // 3 + col // 3) % 2 == 0:
                    bg_color = '#f0f0f0'
                
                button = tk.Button(
                    master=grid_frame,
                    text='',
                    font=font.Font(size=18, weight='bold'),
                    fg='black',
                    bg=bg_color,
                    relief='solid',
                    borderwidth=1,
                    command=lambda r=row, c=col: self._on_cell_click(r, c)
                )
                button.grid(row=row, column=col, sticky="nsew")
                self._cells[button] = (row, col)
                self._buttons_by_coord[(row, col)] = button

    def _create_key_bindings(self):
        # Vincular teclas numéricas y tecla de borrado
        for num in range(1, 10):
            self.bind(str(num), self._on_number_key)
        self.bind('<BackSpace>', self._on_backspace)
        self.bind('<Delete>', self._on_backspace)
        self.bind('<Escape>', self._on_escape)

    def _on_cell_click(self, row, col):
        # Deseleccionar celda anterior
        if self._selected_cell:
            prev_row, prev_col = self._selected_cell
            self._buttons_by_coord[(prev_row, prev_col)].config(relief='solid')
        
        # No permitir seleccionar celdas iniciales
        if (row, col) in self._game._initial_values:
            self._selected_cell = None
            return
        
        # Seleccionar nueva celda
        self._selected_cell = (row, col)
        self._buttons_by_coord[(row, col)].config(relief='raised')

    def _on_number_key(self, event):
        if not self._selected_cell:
            return
        
        row, col = self._selected_cell
        value = event.char
        
        # Actualizar interfaz y estado del juego
        button = self._buttons_by_coord[(row, col)]
        button.config(text=value)
        self._game._current_moves[row][col] = Move(row, col, value)
        
        # Verificar si el juego ha terminado
        if self._game._check_game_over():
            messagebox.showinfo("¡Felicidades!", "Has completado el Sudoku correctamente 🎉")
            self.destroy()

    def _on_backspace(self, event):
        if not self._selected_cell:
            return
        
        row, col = self._selected_cell
        button = self._buttons_by_coord[(row, col)]
        button.config(text="")
        self._game._current_moves[row][col] = Move(row, col, "")

    def _on_escape(self, event):
        # Deseleccionar celda actual
        if self._selected_cell:
            row, col = self._selected_cell
            self._buttons_by_coord[(row, col)].config(relief='solid')
            self._selected_cell = None

    def display_numbers(self, moves_matrix):
        for row in moves_matrix:
            for move in row:
                if move.label:
                    button = self._buttons_by_coord[(move.row, move.col)]
                    button.config(text=str(move.label))
                    # Marcar celdas iniciales como no editables
                    if (move.row, move.col) in self._game._initial_values:
                        button.config(fg='blue', state='disabled')


class SudokuGame:
    def __init__(self):
        self._initial_values = set()
        self._current_moves = [[Move(r, c) for c in range(9)] for r in range(9)]
        self._is_game_over = False
        self._generate_initial_numbers()

    def _generate_initial_numbers(self):
        """Genera un tablero de Sudoku válido con números iniciales"""
        # Crear un tablero resuelto válido
        self._create_valid_board()
        
        # Seleccionar celdas iniciales al azar (sin repetir)
        count = 20  # número de celdas iniciales
        all_cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_cells)
        
        for i in range(count):
            row, col = all_cells[i]
            value = self._current_moves[row][col].label
            self._initial_values.add((row, col))
            
        # Limpiar las celdas no iniciales
        for row in range(9):
            for col in range(9):
                if (row, col) not in self._initial_values:
                    self._current_moves[row][col] = Move(row, col, "")

    def _create_valid_board(self):
        """Crea un tablero de Sudoku válido usando backtracking"""
        # Inicializar el tablero vacío
        self._current_moves = [[Move(r, c, "") for c in range(9)] for r in range(9)]
        
        # Llenar la diagonal de las 3 cajas principales
        for i in range(0, 9, 3):
            self._fill_box(i, i)
        
        # Resolver el resto del tablero
        self._solve_sudoku()
    
    def _fill_box(self, row, col):
        """Llena una caja 3x3 con números aleatorios"""
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for i in range(3):
            for j in range(3):
                self._current_moves[row + i][col + j] = Move(row + i, col + j, str(numbers.pop()))
    
    def _is_valid(self, row, col, num):
        """Verifica si es válido colocar un número en una posición"""
        # Verificar fila
        for c in range(9):
            if self._current_moves[row][c].label == str(num):
                return False
        
        # Verificar columna
        for r in range(9):
            if self._current_moves[r][col].label == str(num):
                return False
        
        # Verificar caja 3x3
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self._current_moves[box_row + i][box_col + j].label == str(num):
                    return False
        
        return True
    
    def _solve_sudoku(self):
        """Resuelve el Sudoku usando backtracking"""
        for row in range(9):
            for col in range(9):
                if not self._current_moves[row][col].label:
                    for num in range(1, 10):
                        if self._is_valid(row, col, num):
                            self._current_moves[row][col] = Move(row, col, str(num))
                            
                            if self._solve_sudoku():
                                return True
                            
                            self._current_moves[row][col] = Move(row, col, "")
                    
                    return False
        return True

    def get_initial_board(self):
        return self._current_moves

    # Check for game over
    def _check_row_and_columns(self):
        # Verificar filas
        for row in self._current_moves:
            seen = set()
            for move in row:
                if move.label:
                    if move.label in seen:
                        return False
                    seen.add(move.label)
        
        # Verificar columnas
        for col in range(9):
            seen = set()
            for row in range(9):
                move = self._current_moves[row][col]
                if move.label:
                    if move.label in seen:
                        return False
                    seen.add(move.label)
        
        return True

    def _check_mini_board(self):
        xs = [0, 3, 6]
        for r in xs:
            for c in xs:
                seen = set()
                mini = self._extract_mini_board(r, c)
                for move in mini:
                    if move.label:
                        if move.label in seen:
                            return False
                        seen.add(move.label)
        return True

    def _extract_mini_board(self, row, col):
        rows = self._current_moves[row:row+3]
        mini = rows[0][col:col+3] + rows[1][col:col+3] + rows[2][col:col+3]
        return mini

    def _check_game_over(self):
        # Primero verificar que todas las celdas estén llenas
        for r in self._current_moves:
            for m in r:
                if not m.label:
                    return False
        
        # Luego verificar que todas las reglas se cumplan
        return self._check_row_and_columns() and self._check_mini_board()

    def get_is_game_over(self):
        return self._check_game_over()


def main():
    game = SudokuGame()
    board = SudokuBoard(game)
    board.geometry('500x550')
    board.display_numbers(game.get_initial_board())
    board.mainloop()


if __name__ == '__main__':
    main()