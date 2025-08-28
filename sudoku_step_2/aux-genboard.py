import random

def generate_numbers():
    return random.randint(1, 9)


def generate_board():
    board = [[0]*9 for i in range(9)]
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            val = generate_numbers()
            while val in row:
                val = generate_numbers()
            row[j] =  val
    return board

def gen_board_with_comprehion():
    return [[generate_numbers() for _ in range(9)] for _ in range(9)]

def main():
    print(generate_board())

if __name__ == '__main__':
    main()
