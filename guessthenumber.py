# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simpleguitk as simplegui
import random
import math


# initialize global variables used in your code

number = 0
guesses = 0

# helper function to start and restart the game

def new_game():
     rand_game = random.randrange(0,2)
     print ""
     print "::NEW GAME::"
     if rand_game == 0:
         range100()
     else:
         range1000()
     print ""



# define event handlers for control panel
def range100():
      global number, guesses
      number = random.randrange(0,100)
      guesses = 7
      print "The range is 0 - 100"
      print "The number of guesses remaining: ", guesses
     

def range1000():
    # button that changes range to range [0,1000) and restarts
      global number, guesses
      number = random.randrange(0,1000)
      guesses = 10
      print "The range is 0 - 1000"
      print "The number of guesses remaining: ", guesses
    
    
    
def input_guess(guess):
       
    global number, guesses
    my_guess = int(guess)
    guesses -= 1
    print "Guess was ", my_guess
    print "Number of guesses remaining: ", guesses
    if guesses < 0:
        print "You lose! The number was ", number
        new_game()
    elif number < my_guess:
        print "Guess lower"
    elif number > my_guess:
        print "Guess higher"
    elif number == my_guess:
        print "You guessed it! The number is ", number
        new_game()
    print ""

    
# create frame

frame = simplegui.create_frame("Guess the number", 200, 200, 200)
 
# register event handlers for control elements

frame.add_button("range is [0, 100]", range100, 200)
frame.add_button("range is [0, 1000]", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

# call new_game and start frame

new_game()
frame.start()
# always remember to check your completed program against the grading rubric
