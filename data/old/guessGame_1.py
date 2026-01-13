# Source - https://stackoverflow.com/q
# Posted by user2917305, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-28, License - CC BY-SA 3.0

import random 
numberofGuesses = 0 
print ("I'm thinking of a number between 1 and 10. What is it? You have three guesses.") 
randomNumber = (random.randint(1,10))

while numberofGuesses < 3: 
    numberofGuesses = numberofGuesses +1
    userInput = input () 
    userInput = int(userInput) 
    if randomNumber > userInput: 
        print("Too Low! Try again")
    if randomNumber < userInput:
        print("Too High! Try Again")
    if randomNumber == userInput:
        print("Well done! Your guess was correct!")
        break

if numberofGuesses == 3 and randomNumber != userInput:
    print("Sorry! You lose. The correct number was:",randomNumber)
