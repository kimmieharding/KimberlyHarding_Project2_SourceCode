 # Kimberly Harding CS670 Project 2 Cluedo Game

 ## Cloning the Repository: Using HTTPS
```
# Navigate to the location you want to upload repo
cd path/to/folder 

# Clone the repository using the URL
git clone https://github.com/kimmieharding/KimberlyHarding_Project2_SourceCode.git

# Locate the folder
cd KimberlyHarding_Project2_SourceCode
```

 ## Running the Game
```
# After navigating to the folder
python main.py

# Example output
Kimberly Harding CS670 Project 2
Welcome to Cluedo
Would you like to play? (y/n)
```

 ## Repository Structure
 clue/
 
├── board.py  # the mansion layout and rendering the board  
 
├── cards.py  # CHARACTERS, WEAPONS, ROOMS, plus solution and dealing  
 
├── game.py # initializing the game, taking turns, and making suggestions  
 
├── player.py # class for player object: hand, character, eliminated, etc.  
 
├── movement.py # locating valid locations, moving from secret passages and rooms  
 
|── utils.py # Helpers for printing options and prompt to command line  
 
└── main.py #Run the game: python main.py

 **Board is inspired from the following image**
 https://i.pinimg.com/736x/36/63/dd/3663ddb1e8b96771a46c6026eccca804.jpg 
