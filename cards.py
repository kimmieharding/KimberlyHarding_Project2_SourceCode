"""Cards, the murder solution, and dealing."""
import random

CHARACTERS = [
    "Miss Scarlett",
    "Colonel Mustard",
    "Mrs. White",
    "Reverend Green",
    "Mrs. Peacock",
    "Professor Plum",
]

WEAPONS = [
    "Candlestick",
    "Dagger",
    "Lead Pipe",
    "Revolver",
    "Rope,",
    "Wrench"
]

ROOMS = [
    "Study",
    "Hall", 
    "Lounge", 
    "Library", 
    "Billiard Room",
    "Dining Room", 
    "Conservatory", 
    "Ballroom", 
    "Kitchen"
]

def murder_solution():
    """The confidential envelope: character, weapon, room"""
    #random.choice works on index-able datastructures
    return (random.choice(CHARACTERS), random.choice(WEAPONS), random.choice(ROOMS))

def deal(num_players, confidential_envelope):
    """Shuffle the reamining cards ad deal them to players; hands may differ by one card."""
    
    # 1. Remove character, weapon, room in confidential envelope form the deck
    deck = []
    for c in CHARACTERS + WEAPONS + ROOMS:
        if c not in confidential_envelope:
            deck.append(c)

    # 2. Shuffle the cards in the list
    random.shuffle(deck)

    # 3. Split the deck into hands
    hands = []
    for i in range(num_players):
        hands.append(deck[i::num_players])
    return hands