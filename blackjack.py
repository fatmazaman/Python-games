# Mini-project #6 - Blackjack
import simpleguitk as simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (CARD_SIZE[0] / 2, CARD_SIZE[1] / 2)
TITLE_POS = (100,40)
SCORE_POS = (480, 30)
MESSAGE_POS = (100, 80)
MY_HAND_POS = (60, 410)
DEALER_HAND_POS = (60, 210)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
CARD_BACK_SIZE = (71, 96)
#CARD_BACK_CENTER = (35.5, 48)
CARD_BACK_CENTER = (CARD_BACK_SIZE[0] / 2, CARD_BACK_SIZE[1] / 2)
card_back_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
# used to determine when one of the two dealer's cards should be hidden
in_play = False
uncover_dealers_card = True
message = "Hit or stand?"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        # check for allowed values
        if (suit in SUITS) and (rank in RANKS):
            # assign
            self.suit = suit
            self.rank = rank
        else:
            # None is a special default value in Python
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        # concatenation works because both are strings in the lists above
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, flipped):
        ''' get this card's image and draw it in pos. Flipped is a boolean that determines if facing up. '''
        #print card_loc
        if not flipped:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        # print back card    
        else:
            canvas.draw_image(card_back_image, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
# define hand class
class Hand:
    def __init__(self, owner):
        # hand is a list of cards. Start empty.
        self.cards = []
        # sometimes we'll need to cover the second card in dealer's hand
        self.cover_second = False
    def __str__(self):
        s = ''
        #print "[",
        for crd in self.cards:
            s = s + " " + str(crd)
        #    print crd,
        #print "]"
        #return str(self.cards)
        return s
      
    def add_card(self, card):
        ''' add this card to the hand list '''
        self.cards.append(card)
        
    def get_card(self, pos):
        ''' retrieve rank and suit of a card given its position in the hand '''
        return self.cards[pos]

    def set_cover_second(self, cover):
        self.cover_second = cover
        
    def second_covered(self):
        return self.cover_second
    
    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        ''' calculate total value of the hand '''
        value = 0 
        for card in self.cards:
            value += VALUES[card.get_rank()]
        # counting aces: two aces counted at 11 => 22, so a bust. Only cases are zero or one
        # ace counted as 11.
        # no aces make it easy
        if self.count_aces() == 0:
            return value
        # there is at least one ace
        else:
            # don't count that one ace as 11 if doing so would cause a bust
            if value + 10 > 21:
                return value
            # we are assuming if you can you want to count one ace as 11. Notice, we already
            # counted that ace as 1, so we only need to add 10.
            else:
                return value + 10
            
    def number_cards(self):
        ''' count how many cards are now in the hand. '''
        number = 0
        for crd in self.cards:
            number += 1
        return number
        
    def busted(self):
        ''' check if hand is busted. '''
        if self.get_value() > 21:
            return True
        else:
            return False
    
    # drawing of the hand
    def draw(self, canvas, p):
        ''' go through all the cards in the hand and run draw method for each in the proper position. '''
        i = 0
        for crd in self.cards:
            # we draw at the same height (y), but advance the x. The 20 is space between cards.
            if self.cover_second and i == 1:
                # print second card covered
                crd.draw(canvas, [p[0] + i * (CARD_SIZE[0] + 20), p[1]], True)
            else:
                crd.draw(canvas, [p[0] + i * (CARD_SIZE[0] + 20), p[1]], False)
            i += 1
    
    def hit(self, deck):
        ''' get a card from the end of the deck and add it to the hand '''
        card = deck.deal_card()
        self.add_card(card)
        
    def count_aces(self):
        ''' go through the hand and count aces '''
        aces = 0
        for crd in self.cards:
            if crd.get_rank() == 'A':
                aces += 1
        return aces
    
# define deck class
class Deck:
    def __init__(self):
        # the longer method
        #self.deck = []
        #for suit in SUITS:
        #    for rank in RANKS:
        #        #print suit, rank
        #        crd = Card(suit, rank)
        #        self.deck.append(crd)
        # initialize deck using collection with two loops
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]   
        # shuffle right after initialization
        self.shuffle()
        
    # add cards back to deck and shuffle
    def shuffle(self):
        # modifies list deck, so no assignment needed
        random.shuffle(self.deck)

    def deal_card(self):
        ''' pick the last one from the deck. Remove it and return.'''
        return self.deck.pop()
    
    def __str__(self):
        print "[",
        for crd in self.deck:
            print crd,
        print "]"
        #print len(self.deck)

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, my_hand, dealer_hand, message, score
    init()
    # hittind deal in the middle of a hand causes player to lose
    if in_play:
        score -= 1
    # game is on
    in_play = True
    # get cards from the deck - the initial two cards for each side
    my_hand.hit(deck)
    my_hand.hit(deck)
    #print "my hand:", my_hand, "value:", my_hand.get_value()
    #print "number of aces:", my_hand.count_aces()
    dealer_hand.hit(deck)
    dealer_hand.hit(deck)
    #print "dealer's hand:", dealer_hand, "value:", dealer_hand.get_value()
    message = "In play. Hit or stand?"
    dealer_hand.set_cover_second(True)
    
def hit():
    global in_play, score, message
    # only let hitting if hand below and still game on
    if not my_hand.busted() and in_play:
        #print "hitting."
        my_hand.hit(deck)
        # busted if with the new card you exceeded the limit
        if my_hand.busted():
            #print "You have busted!"
            # uncover dealer's card
            dealer_hand.set_cover_second(False)
            # stop the game
            in_play = False
            message = "You have busted! Deal?"
            score -= 1
    #print "hand:", my_hand, "value:", my_hand.get_value()
    #print "dealer's hand:", dealer_hand, "value:", dealer_hand.get_value()
    
def stand():
    global dealer_hand, in_play, score, message
    # make sure dealer's card flipped
    #uncover_dealers_card = False
    # if hand is not busted, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        if not my_hand.busted():
            # standing will always show you the dealer's hand
            dealer_hand.set_cover_second(False)
            # keep hitting the dealer until hand value over 17
            while dealer_hand.get_value() < 17:
                dealer_hand.hit(deck)
                #print "dealer hand after hitting:", dealer_hand
            # did dealer bust?
            if dealer_hand.busted():
                message = "Dealer busted. You won! New deal?"
                score += 1
            else:
                # nobody busted, so compare scores. dealer wins ties.
                if dealer_hand.get_value() >= my_hand.get_value():
                    message = "Dealer wins! New deal?"
                    score -= 1
                else:
                    message = "You won! New deal?"
                    score += 1
            # stop the game
            in_play = False
        else:
            message = "You have already busted. New deal?"
    # this case happens when you haven't busted. Game just ended with a score comparison
    else:
        message = "New deal?"

def init():
    global in_play, my_hand, dealer_hand, deck
    # initialize the deck
    deck = Deck()
    # you get two cards in your hand
    my_hand = Hand("player")
    # dealer's hand
    dealer_hand = Hand("dealer")
    
# draw handler    
def draw(canvas):
    # decoration
    canvas.draw_text("Blackjack", TITLE_POS, 36, "Turquoise")
    canvas.draw_text("score " + str(score), SCORE_POS, 24, "Black")
    canvas.draw_text(message, MESSAGE_POS, 24, "Black")
    canvas.draw_text("Dealer", (60, 200), 24, "Black")
    canvas.draw_text("Player", (60, 400), 24, "Black")
    # test to make sure that card.draw works, replace with your code below
    #card = Card("D", "K")
    #card.draw(canvas, [300, 300])
    # draw hands
    my_hand.draw(canvas, MY_HAND_POS)
    dealer_hand.draw(canvas, DEALER_HAND_POS)
    
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric