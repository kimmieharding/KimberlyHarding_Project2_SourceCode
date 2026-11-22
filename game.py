
""""Game setup, turn loop, and movement."""
import random
from board import START_POSITIONS, render, dot
from movement import STEPS, moves_from_room, move_from_secret_passage, step_from
from cards import CHARACTERS, WEAPONS, murder_solution, deal
from utils import prompt_choice, ask_yes_no

class Game:
    TURN_ORDER = ["Scarlett", "Mustard", "White", "Green", "Peacock", "Plum"]

    def __init__(self, players):
        """"Sort by position in TURN_ORDER; only characters actually playing are kept."""
        self.players = sorted(players, key=lambda p: CHARACTERS.index(p.character))
        self.murder_solution = murder_solution()

        # Deal the hand for each player with the remaining cards
        for player, hand in zip(self.players, deal(len(self.players), self.murder_solution)):
            player.hand = hand
            player.position = START_POSITIONS[player.character]

        self.weapon_locations = {} #Weapon token which is moved during suggestions
        self.current = 0 # index for self.players
        self.over = False # Continue playing until False

    # ------------------------ HELPERS ---------------------------------------
    @property 
    def current_player(self):
        return self.players[self.current]

    def next_turn(self):
        """Advance to the next player who hasn't been eliminated."""
        for _ in range(len(self.players)):
            self.current = (self.current + 1) % len(self.players)
            if not self.current_player.eliminated:
                return

    @staticmethod
    def roll_dice():
        """Return 1-6 from one dice roll."""
        return random.randint(1, 6)
    
    def occupied_squares(self, exclude):
        """Hallyway squares blocked by other players' tokens."""
        return {p.position for p in self.players if p is not exclude and not isinstance(p.position, str)}

    def show_board(self):
        """Print the board."""
        # locate the players tokens - show the movement across the board
        tokens = {p.position: dot(p.character) for p in self.players if isinstance(p.position, tuple)}
        print(render(tokens))

        # print the coordinates of each of the players for reference
        for p in self.players:
            where = f"in the {p.position}" if isinstance(p.position, str) else f"at {p.position}"
            print(f"  {dot(p.character)} {p.character} ({p.name}) {where}")
        print("\n")

    # --------------------------- TURN ------------------------------------
    def play_turn(self, player):
        print(f"\n{player.name} : {player.character}")
        print(f"Your cards: {', '.join(sorted(player.hand))}\n")

        # 1. Render the board at the start
        self.show_board()

        # 1. Optional: Move through Secret Passage if available
        if isinstance(player.position, str): #Indicates location is a room - not a coordinate
            destination = move_from_secret_passage(player.position)
            if destination and ask_yes_no(f"Use secret passage to {destination}? (y/n) "):
                player.position = destination
                self.make_suggestion(player) #Must make a suggestion when entering new room
                # if ask_yes_no("Would you like to make an accusation? (y/n) "):
                #     self.make_accusation(player)
                if not self.over:
                    self.show_board()
                return

        # 2. Prompt Enter and the roll die
        input(f"{player.name}, press Enter to roll.")
        roll = self.roll_dice()
        print(f"\n{player.character}, your roll is {roll}.\n")

        # 3. Movement: returns True if character enters room; therefore, must make a suggestion
        if self.movement(player, roll):
            self.make_suggestion(player)

        # # 4. Offer accusation on every single turn - Project 2 Part 2 
        # print("\n")
        # if ask_yes_no("Would you like to make an accusation? (y/n) "):
        #     self.make_accusation(player)

    def movement(self, player, roll):
        """Returns True if the player ends the move inside a room."""
        entered = None
        blocked = self.occupied_squares(exclude=player)
        visited = set()

        # Leaving a room: choose a door to exit, costs one step
        if isinstance(player.position, str):
            exits = [e for e in moves_from_room(player.position) if e not in blocked]
            if not exits:
                print("All exits are blocked.")
                return None
            player.position = prompt_choice("Choose an exit: ", exits)
            roll -= 1 #Roll is finished
        visited.add(player.position)

        # Move through the hallway for remainder of rolls, or until enter a new room
        while roll > 0 and isinstance(player.position, tuple):
            direction = input(f"{roll} steps left. up/down/left/right or done: ").strip().lower()
            if direction == "done":
                break
            if direction not in STEPS:
                print("Type up, down, left or right")
                continue

            new_pos = step_from(player.position, direction)
            
            if new_pos is None:
                print("A wall is in the way. ")
                continue
            if isinstance(new_pos, tuple) and (new_pos in blocked or new_pos in visited):
                print("That square is occupied or already used this turn.")
                continue

            player.position = new_pos
            roll -= 1
            if isinstance(new_pos, str):
                entered = new_pos
                print(f"You entered the {new_pos}.")
            else: 
                visited.add(new_pos)

            self.show_board() #Show character token moving across board for every step

        return entered

    
    def make_suggestion(self, player):
        """Player must make a suggestion when they enter a room.
        Room is fixed to the player's current room."""

        # 1. Prompt player must make a suggestion 
        room = player.position
        print(f"\n{player.name} is in the {room}. Make a suggestion.")

        # 2. prompt_choice for CHARACTER and WEAPON
        character = prompt_choice("Pick a character: ", CHARACTERS)
        weapon = prompt_choice("Pick a weapon: ", WEAPONS)

        # 3. Move suggested character (if playing) and weapon into the room
        target = next((p for p in self.players if p.character == character), None)
        if target and target.position != room:
            target.position = room
        self.weapon_locations[weapon] = room

        print(f"\n{player.name}: I suggest it was {character} with the {weapon} in the {room}.")

        # 4. Resolve the suggestion
        # result = self.resolve_suggesion(player, character, weapon, room)
        # if result:
        #     disprover, card = result
        #     print(f"{disprover.name} showed you: {card}")

        return character, weapon, room

    # For Project 2 Part 2 
    # def resolve_suggesion(self, player, character, weapon, room):
    #     """Ask other players to disprove suggestion.
    #     Returns (disprover, card), or None if nobody can disprove."""
    #     suggestion = (character, weapon, room)
    #     start = self.players.index(player)

    #     for i in range(1, len(self.players)): # loop through every character for testing
    #         other = self.players[(start + i) % len(self.players)] #ensure in clockwise order
    #         matches = [card for card in suggestion if card in other.hand] #determine if other hand has any of the cards form suggesting palyer

    #         if matches: #returns the first match from players
    #             # Refuting player chooses which card to show if they have multiple cards
    #             # Implement a feature for that player to select
    #             print(F"{other.name} disproves the suggestion.")
    #             return other, matches[0]

    #         print(f"{other.name} cannot disprove the suggestion.")

    #     print("Nobody could disprove the suggestion.")
    #     return None

    # For Project 2 Part 2
    # def make_accusation(self, player):
    #     """Prompt for character/weapon/room, compare to murder_solution.
    #     If correct game is over and player wins, if wrong the player is eliminated.
    #     Needs to ask for accusation every turn."""
    #
    #     character = prompt_choice("Pick a character: ", CHARACTERS)
    #     weapon = prompt_choice("Pick a weapon: ", WEAPONS)
    #     room = prompt_choice("Pick a room: ", ROOMS)

    #     if (character, weapon, room) == self.murder_solution:
    #         print(f"{player.name} wins!")
    #     else:
    #         print(f"Wrong accusation. {player.name} is out of the game.")
    #         player.eliminated = True

    #         #Check if all the players have been eliminated
    #         if all(p.eliminated for p in self.players):
    #             print("Everyone has been eliminated. Game over.")
    #             self.over = True
    # Next step is to introduce log or display for keeping track of suggestions (player and their repsective cards)

    def play(self):
        """Continue playing the game until someone wins or everyone is eliminated."""
        while not self.over:
            player = self.current_player
            self.play_turn(player)
            if not self.over:
                self.next_turn()
