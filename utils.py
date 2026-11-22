"""Utils: helpers for printing the options and prompts."""

def prompt_choice(prompt, options):
    """Numbered menu (e.g, CHARACTERS or WEAPONS or ROOMS). 
    Continues prompting until valid and returns the selected option."""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"  {i}) {option}") #Print every option from list using a numbered index
    while True:
        text = input(f"Choose 1-{len(options)}: ").strip()
        if text.isdigit() and 1 <= int(text) <= len(options):
            return options[int(text) - 1] #If number is within range, return that options (accoutnt for 1 switching to 0 index)
        print(f"Please enter a number from 1 to {len(options)}.")
    
def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n"):
            return answer == "y" #Returns true of the answer is yes, false otherwise
        print("Please enter y or n.")

def ask_num_players():
    while True:
        text = input("Enter the number of players: ").strip()
        if text.isdigit() and 3 <= int(text) <= 6:
            return int(text) 
        print("Cluedo is played with 3 to 6 players.")