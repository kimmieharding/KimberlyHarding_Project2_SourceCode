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

ROOM_NAMES = {
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
