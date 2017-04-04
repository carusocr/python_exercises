# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
 
    def __str__(self):
        ans=""
        for i in range(len(self.cards)):
            ans += str(self.cards[i])
        return ans

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        sum = 0
        has_ace = False
        for i in self.cards:
            sum += VALUES[i.get_rank()]
            if i.get_rank() == "A":
                has_ace = True
        if has_ace:
            if sum+10 <= 21:
                sum+=10
        return sum

    def draw(self, canvas, pos):
        pass
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(x,y) for x in SUITS for y in RANKS]

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        ans = ""
        ans += [str(x) for x in self.deck]
        return ans

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    dealer_hand.add_card(deck.deal_card())    
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    print "Dealer hand:", dealer_hand
    print "Player hand:", player_hand
    #print dealer_hand.get_value()
    in_play = True
    

def hit():
    global in_play, player_hand
    if player_hand.get_value() < 21:
        if in_play == True:
            player_hand.add_card(deck.deal_card())
            print player_hand.get_value()
            if player_hand.get_value() > 21:
                print "Busted!"
                in_play = False
                
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    
    global in_play
    
    if in_play == False:
        print "You've busted, dumbass!"
    else:
        while dealer_hand.get_value() < 17:
            print dealer_hand.get_value()
            dealer_hand.add_card(deck.deal_card())
            if dealer_hand.get_value() > 21:
                print "Dealer busted! HA-ha."
    if (dealer_hand.get_value() >= player_hand.get_value()) and dealer_hand.get_value() < 22:
        print "You lost. Dealer had ", dealer_hand.get_value(), "and you had ", player_hand.get_value()
    else:
        print "You win! Dealer had ", dealer_hand.get_value(), "and you had ", player_hand.get_value()

   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global player_hand, dealer_hand
    # test to make sure that card.draw works, replace with your code below
    dealer_hand.draw(canvas, [300,300])

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

# remember to review the grading rubric
