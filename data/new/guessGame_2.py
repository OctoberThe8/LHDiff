# Source - https://stackoverflow.com/a
# Posted by Farmer Joe
# Retrieved 2025-11-28, License - CC BY-SA 3.0

import random

randomNumber = random.randint(1,10)

while numberofGuesses < 3: 

    numberofGuesses = numberofGuesses + 1 

    userInput = 0

    userInput = input() 

    userInput = int(userInput) 

    if randomNumber > userInput: 

        print("Too Low! Try again")

    if randomNumber < userInput:

        print("Too High! Try Again")
