import random

def generate_numbers():
    return random.randint(0, 9)

def generate_coord():
    '''Generates random coordinates to start the game'''
    total = generate_numbers()
    # generate pairs (x, y) directly
    fill = [(generate_numbers(), generate_numbers()) for _ in range(total)]
    print("Initial fill:", fill)
    # generate point for each row
    coords = coords_to_fill(fill)
    print("Coords:", coords)
    return coords

def coords_to_fill(arr):
    '''Helper method to generate coordinates
    @arr list of (x, y)
    '''
    coords = []
    for x, y in arr:
        for _ in range(x):  # loop x times
            coords.append((generate_numbers(), y))
    return coords

def main():
    generate_coord()

if __name__ == '__main__':
    main()
