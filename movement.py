"""Movement helper functions: lovating valid squares, moving from rooms, secret passages, etc."""

from board import (GRID, ROWS, COLS, START_SQUARES, DOORS_TO_ROOM, SECRET_PASSAGES)

""""Player movement options throughout the board."""
STEPS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

def neighbors(pos):
    """"Calculate the neighbors positions that ar valid.
        Players can walk one step either into a hallway or door."""
    valid_neighbors = []
    r, c = pos
    for dr, dc in STEPS.values():
        nr, nc = r + dr, c + dc
        if (0 <= nr < ROWS and #within row length
            0 <= nc < COLS and  #within column length
            (GRID[nr][nc] == "·" or # open coordinate
            GRID[nr][nc] in START_SQUARES or # or staring location
            (nr, nc) in DOORS_TO_ROOM)): # or door to room
            valid_neighbors.append((nr, nc)) #add valid neighbors
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

def step_from(position, direction):
    """Check movement from one square - to be called in movement()"""
    dr, dc = STEPS[direction]
    target = (position[0] + dr, position[1] + dc)
    if target not in neighbors(position):
        return None
    return DOORS_TO_ROOM.get(target, target)