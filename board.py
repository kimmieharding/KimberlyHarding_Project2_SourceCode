""" Cluedo board as a 2D Grid.

Legend 
    S H L B R D C A K Room squares
    s h l b r d c a k Door squares
    X                 Cellular
    .                 Hallway
    1-6               Character start squares
"""

GRID = [
    "SSSSSSS··HHHHHH·1LLLLLLL", 
    "SSSSSSS··HHHHHH··LLLLLLL",
    "SSSSSSS··HHHHHH··LLLLLLL",   
    "SSSSSSs··HHHHHH··LLLLLLL",   
    "·········hHHHHH··LLLLLLL",  
    "6········HHHHHH··lLLLLLL",   
    "·········HHhhHH·········",   
    "BBBBBB·················2",   
    "BBBBBb···XXXXX··········",   
    "BBBBBB···XXXXX··DdDDDDDD",   
    "BBBbBB···XXXXX··DDDDDDDD",  
    "·········XXXXX··DDDDDDDD",  
    "RrRRRR···XXXXX··dDDDDDDD",   
    "RRRRRR···XXXXX··DDDDDDDD",   
    "RRRRRR···XXXXX··DDDDDDDD",   
    "RRRRRr··········DDDDDDDD",   
    "RRRRRR··················",   
    "········AaAAAAaA········",   
    "5·······AAAAAAAA··KkKKKK",  
    "CCCCcC··aAAAAAAa··KKKKKK",   
    "CCCCCC··AAAAAAAA··KKKKKK",   
    "CCCCCC··AAAAAAAA··KKKKKK",   
    "CCCCCC··AAAAAAAA··KKKKKK",  
    "CCCCCC·4AAAAAAAA3·KKKKKK",
]
ROWS, COLS = len(GRID), len(GRID[0])

ROOMS = {
    "S": "Study", 
    "H": "Hall", 
    "L": "Lounge", 
    "B": "Library",
    "R": "Billiard Room", 
    "D": "Dining Room", 
    "C": "Conservatory",
    "A": "Ballroom", 
    "K": "Kitchen", 
    "X": "CLUE",
}

"""ANSI 256 Color-Code for each room."""
ROOM_COLORS = {
    "S": 94, 
    "H": 24, 
    "L": 90, 
    "B": 58, 
    "R": 22, 
    "D": 88,
    "C": 30, 
    "A": 61, 
    "K": 136, 
    "X": 238
}

START_SQUARES = {
    "1": "Miss Scarlett", 
    "2": "Colonel Mustard", 
    "3": "Mrs. White",
    "4": "Reverend Green", 
    "5": "Mrs. Peacock", 
    "6": "Professor Plum",
}

SECRET_PASSAGES = {
    "Study": "Kitchen", 
    "Kitchen": "Study",
    "Lounge": "Conservatory", 
    "Conservatory": "Lounge",
}

"""ANSI 256 Color-Code for each Character's dot."""
TOKEN_COLORS = {
    "Miss Scarlett": 9, 
    "Colonel Mustard": 11, 
    "Mrs. White": 15,
    "Reverend Green": 10, 
    "Mrs. Peacock": 12, 
    "Professor Plum": 92
}

"""Starting coordinates for each of the characters."""
START_POSITIONS = {}
for r, row in enumerate(GRID):
    for c, ch in enumerate(row):
        if ch in START_SQUARES:
            START_POSITIONS[START_SQUARES[ch]] = (r, c)

"""Coordinates for each room on the board."""
DOORS_TO_ROOM = {}
for r, row in enumerate(GRID):
    for c, ch in enumerate(row):
        if ch.islower() and ch.upper() in ROOMS:
            DOORS_TO_ROOM[(r, c)] = ROOMS[ch.upper()]

""""Player movement options throughout the board."""
STEPS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

def neighbors(pos):
    """"Calculate the neighbors positions that ar valid.
        Players can walk one step either into a hallway or door."""
    valid_neighbors = []
    r, c = pos
    for dr, dc in STEPS.values():
        nr, nc = r + dr, c + dr
        if (0 <= nr < ROWS and 
            0 <= nc < COLS and 
            (GRID[nr][nc] == "·" or 
            GRID[nr][nc] in START_SQUARES or 
            (nr, nc) in DOORS_TO_ROOM)):
            valid_neighbors.append((nr, nc))
    return valid_neighbors

def moves_from_square(pos):
    """Valid hallway cooridnates or doorways to enter."""
    moves = []
    for n in neighbors(pos):
        if n in DOORS_TO_ROOM:
            moves.append(DOORS_TO_ROOM[n]) # name of door to enter
        else:
            moves.append(n) # hallway coordinate
    return moves

def moves_from_room(room):
    """Valid coordinates to leave room."""
    moves = []
    for door, name in DOORS_TO_ROOM.items():
        if name == room:
            for n in neighbors(door):
                if n not in DOORS_TO_ROOM:
                    moves.append(n)
    return moves

def move_from_secret_passage(room):
    """If can move through secret passage return destination room name."""
    return SECRET_PASSAGES.get(room)
 
def dot(character):
    """A coloured dot for this character."""
    # Text color: \033[38;5;...\033[0m]
    return f"\033[38;5;{TOKEN_COLORS[character]}m\u25cf\033[39m"

def render(tokens=None):
    """Board as text. Doors show as +.
    Each room has its own background color, 
    and characters repersented by colored dot."""
    lines = []
    for r, row in enumerate(GRID):
        squares = []
        for c, grid_ch in enumerate(row):
            ch = grid_ch
            if (r, c) in tokens: # indicating a players location
                ch = tokens[(r, c)]
            elif ch.islower(): # indicating a door positon
                ch = "+"
            elif ch in START_SQUARES:
                ch = "·"
            cell = ch + " "
            if grid_ch.upper() in ROOM_COLORS: # indicating a room - color code the background
                cell = f"\033[48;5;{ROOM_COLORS[grid_ch.upper()]};38;5;231m{cell}\033[0m"
            squares.append(cell)
        lines.append(f"{r:>2} " + "".join(squares))
    return "\n".join(lines)

if __name__ == "__main__":
    print(render())