# Mini Project "Rock_Papaer_Scissors_Lizard_Spock"
import random

#Helper Function: Convert number to name 

def number_to_name(number):
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        print number + ' is an invalid entry. Valid entry is from 0 to 4.'
    

# Helper Function: Convert name to number

def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        print name + ' is an invalid entry. Valid entries are rock, Spock, paper, lizard, scissors.'
    
def rpsls(name): 
    
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,4)

    # compute difference of player_number and comp_number modulo five
    difference = (player_number - comp_number) % 5
   
     # use if/elif/else to determine winner
    if difference == 1:
        winner = 'Player wins!'
    elif difference == 2:
        winner = 'Player wins!'      
    elif difference == 0:
        winner = 'Player and computer tie!'
    else:
        winner = 'Computer wins!'
        
    # convert comp_number to name using number_to_name
    comp_name = number_to_name(comp_number)
    
    # print results
    print 'Player chooses ' + name
    print 'Computer chooses ' + comp_name
    print winner
    print ''
    
    
# test!!!
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
    