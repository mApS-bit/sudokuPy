
points = [(i,j) for i in range(3) for j in range(3)]

points_2 = []
for i in range(3):
    for j in range(3):
        points_2.append((i,j))

xs = [0,3,6]
verts = [(i,j) for i in xs for j in xs]

print(verts)


board = [
    [1,2,3,4,5,6,7,8,9],
    [10,11,12,13,14,15,16,17,18],
    [19,20,21,22,23,24,25,26,27],
    [28,29,30,31,32,33,34,35,36],
    [37,38,39,40,41,42,43,44,45],
    [46,47,48,49,50,51,52,53,54],
    [55,56,57,58,59,60,61,62,63],
    [64,65,66,67,68,69,70,71,72],
    [73,74,75,76,77,78,79,80,81],
]

xs = [0,3,6]
verts = [(i,j) for i in xs for j in xs]  # esquinas de cada mini-board 3x3

def extract_mini_board(board, row, col):
    rows = board[row: row+3]
    mini_board = [r[col:col+3] for r in rows]
    return mini_board

for v in verts:
    print(f"Mini board desde {v}:")
    print(extract_mini_board(board, *v))
