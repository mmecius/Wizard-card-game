import random
import time
import sys
import copy
#---------------------------------------------------------Wizard Card Game--------------------------------------------------------------------
#Game flow: https://en.wikipedia.org/wiki/Wizard_(card_game)
#deck has 60 cards. 13 of each colour (52) + 8 special cards(4 wizards & 4 fools)
#wizard card is most powerful. The first player to place wizard card always wins the round.
#fool card is the least powerful. The first player to place fool card always looses the round.
#regular card works based on their numerical value (i.e. red fighter 3 < red captain 7)

#There is 1 human player and 2-5 CPU players.
#The game is divided in sessions. Each session increases the number of cards in hand and therefore rounds.
#Before the start of each session players are asked how many rounds they expect to win.
#First session has players 1 card in hand -> 1 round. Next session 2 and so forth until all the deck is distributed among players.
#Key to win the game is to correctly predict how many rounds you can win in session.
#During round each player must place 1 card of their hand (complying with the card placing rules). Highest value card wins the round.
#After each session the score is calculated and updated.
#highest total score at the end of the game wins!
#--------------------------------------------------------------------------------------------------------------------------------------------
#Starting variables:
#cards - Full list of all cards that are used in deck
#cards_values - a dictionary of cards with [card game value, card bid likelyhood(%) for cpu]
#cards & card_values are copied into the deck class each session, where their card game values may be modified depending on the session dominant card.
#CPU_names - list of available CPU players to join in the game.
#
#player_list - the master list of lists cointaining:
#1. player name
#2. player score
#3. player line number for session
#4. player line number for round
#5. player class object (had for human, computer_hand for computer)
#
#--------------------------------------------------------------------------------------------------------------------------------------------
#Classes
#1. Deck_class - recreated each time a new session starts: 
# 1.1 Copies in the cards and card_values. 
# 1.2 Determines the session dominant card, enhances the card_values for dominant colour cards.
# 1.3 distributes the cards to players.
#
# 2. Hand - A human player class. Recreated each time a new session starts:
# 2.1 Holds available cards for human player for current session.
# 2.2 placing the bid for current session function.
# 2.3 placing card for current round function.

# 3. Computer_Hand - recreated each time a new session starts:
# 3.1 Holds available cards for computer player for current session.
# 3.2 Evaluating cards &placing the bid for current session function.
# 3.3 Evaluating cards & placing card for current round function
#
#FUNCTIONS
#identify_winner()
#global player_list

# CARDS AND OTHER MAIN VARIABLES
colours = ('Red', 'Blue', 'Green', 'Yellow')
cards = ['[Red] Peasant, 1','[Red] Archer, 2','[Red] Fighter, 3','[Red] Defender, 4', '[Red] Warrior, 5','[Red] Seargeant, 6','[Red] Captain, 7','[Red] Lieutenant, 8','[Red] Sage, 9', '[Red] Advisory, 10', '[Red] Prince, 11','[Red] Queen, 12', '[Red] King, 13',
             '[Blue] Peasant, 1','[Blue] Archer, 2','[Blue] Fighter, 3','[Blue] Defender, 4', '[Blue] Warrior, 5','[Blue] Seargeant, 6','[Blue] Captain, 7','[Blue] Lieutenant, 8','[Blue] Sage, 9', '[Blue] Advisory, 10', '[Blue] Prince, 11','[Blue] Queen, 12', '[Blue] King, 13',
              '[Green] Peasant, 1','[Green] Archer, 2','[Green] Fighter, 3','[Green] Defender, 4', '[Green] Warrior, 5','[Green] Seargeant, 6','[Green] Captain, 7','[Green] Lieutenant, 8','[Green] Sage, 9', '[Green] Advisory, 10', '[Green] Prince, 11','[Green] Queen, 12', '[Green] King, 13',
              '[Yellow] Peasant, 1','[Yellow] Archer, 2','[Yellow] Fighter, 3','[Yellow] Defender, 4', '[Yellow] Warrior, 5','[Yellow] Seargeant, 6','[Yellow] Captain, 7','[Yellow] Lieutenant, 8','[Yellow] Sage, 9', '[Yellow] Advisory, 10', '[Yellow] Prince, 11','[Yellow] Queen, 12', '[Yellow] King, 13',
              'Wizard', 'Wizard','Wizard', 'Wizard',
              'Fool', 'Fool','Fool', 'Fool',
             ]
cards_values = {'[Red] Peasant, 1':[1, 0.05],'[Red] Archer, 2':[2, 0.1],'[Red] Fighter, 3':[3, 0.15],'[Red] Defender, 4':[4, 0.2], '[Red] Warrior, 5':[5, 0.25],
                '[Red] Seargeant, 6':[6, 0.3],'[Red] Captain, 7':[7, 0.35],'[Red] Lieutenant, 8':[8, 0.4],'[Red] Sage, 9':[9, 0.5], '[Red] Advisory, 10':[10, 0.55], 
                '[Red] Prince, 11':[11, 0.6],'[Red] Queen, 12':[12, 0.65], '[Red] King, 13':[13, 0.7],
                '[Blue] Peasant, 1':[1, 0.05],'[Blue] Archer, 2':[2, 0.1],'[Blue] Fighter, 3':[3, 0.15],'[Blue] Defender, 4':[4, 0.2], '[Blue] Warrior, 5':[5, 0.25],
                '[Blue] Seargeant, 6':[6, 0.3],'[Blue] Captain, 7':[7, 0.35],'[Blue] Lieutenant, 8':[8, 0.4],'[Blue] Sage, 9':[9, 0.5], '[Blue] Advisory, 10':[10, 0.55] ,
                '[Blue] Prince, 11':[11, 0.6],'[Blue] Queen, 12':[12, 0.65], '[Blue] King, 13':[13, 0.7],
                '[Green] Peasant, 1':[1, 0.05],'[Green] Archer, 2':[2, 0.1],'[Green] Fighter, 3':[3, 0.15],'[Green] Defender, 4':[4, 0.2], '[Green] Warrior, 5':[5, 0.25],
                '[Green] Seargeant, 6':[6, 0.3],'[Green] Captain, 7':[7, 0.35],'[Green] Lieutenant, 8':[8, 0.4],'[Green] Sage, 9':[9, 0.5], '[Green] Advisory, 10':[10, 0.55] ,
                '[Green] Prince, 11':[11, 0.6],'[Green] Queen, 12':[12, 0.65], '[Green] King, 13':[13, 0.7],
                '[Yellow] Peasant, 1':[1, 0.05],'[Yellow] Archer, 2':[2, 0.1],'[Yellow] Fighter, 3':[3, 0.15],'[Yellow] Defender, 4':[4, 0.2], '[Yellow] Warrior, 5':[5, 0.25],
                '[Yellow] Seargeant, 6':[6, 0.3],'[Yellow] Captain, 7':[7, 0.35],'[Yellow] Lieutenant, 8':[8, 0.4],'[Yellow] Sage, 9':[9, 0.5], '[Yellow] Advisory, 10':[10, 0.55] ,
                '[Yellow] Prince, 11':[11, 0.6],'[Yellow] Queen, 12':[12, 0.65], '[Yellow] King, 13':[13, 0.7],
                'Wizard':[50,1],'Fool':[0,0],
                  }

CPU_names = ['Gendalf', 'Dumbledoure', 'Severus Snape', 'Saruman', 'Sauron', 'Harry Potter', 'Hermione', 'Doctor Strange']

#---------------------------------------------------------------------DECK------------------------------------------------
class Deck_class():

    def __init__(self):
        self.dominant_colour = ''
        self.dominant_card = ''
        self.deck = []
        self.deck_values = {}
        self.deck_values = copy.deepcopy(cards_values)
        for card in cards:
            self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def find_dominant(self):
        #once deck is shuffled, random card is selected (popped) out of deck.
        # if it's a colour card it determines the session dominant colour. If it's not colour, there is no dominant card.
        # the popped card is out of the game for that session.
        self.dominant_card = str(self.deck.pop())
        if self.dominant_card.find('[') == -1:
            self.dominant_colour = 'None'
        else:
            colour_list = self.dominant_card.split(']')
            self.dominant_colour = colour_list[0].replace('[','')
        return self.dominant_colour

    def evaluate_deck(self):
        #for cards in deck with dominant colour, the deck_values are adjusted:
        #20 basis points so that dominant card would overrule any other colour card if allowed
        # +0.25 % chance that cpu would bid to win on this card during bidding session.
        for value in self.deck_values:
            if value.find(self.dominant_colour) == -1:
                pass
            else:
                self.deck_values[value][0] = self.deck_values[value][0] + 20
                self.deck_values[value][1] = self.deck_values[value][1] + 0.25

    def deal(self):
        #function used to pop cards out of deck and return to player hand(s)
        single_card = self.deck.pop()
        return single_card
#--------------------------------------------------------------------- PLAYER HAND------------------------------------------------
class Hand():
    def __init__(self,name):
        self.cards = {}
        self.bid = 0
        self.name = name

    def add_card(self,card):
        #1. human adds cards to his hand from the deck (function connected to the deck class)
        self.cards[card_nr] = card

    def place_bid(self):
        #1. player is given a question how many bids he wants to make in a session
        #2. answer within game rules is inserted into bid_list
        bidding = 1
        while bidding == 1:
            try:
                print('your cards:', self.cards)
                input_bid = int(input('Make a bid on how many rounds you expect to win: ')) 
                if input_bid > session_nr:
                    print("Can't bid more than there are rounds in this session!")
                else:
                        self.bid = int(input_bid)
                        bid_list[self.name] = [int(input_bid),0]
                        print(self.name, ' bids ', bid_list[self.name][0] )
                        break
            except:
                print('invalid number provided!')
                continue 

    def place_card(self):
        #1. player is asked what card from his hand he wants to place:
        print('--------------------------------------------------------')
        print('Dominant Colour of this session: ', deck.dominant_colour)
        print('Dominant Colour of this round: ', round_colour[0])
        print('Remaining cards in your hand:', self.cards)
        print('--------------------------------------------------------')
        card_valid = False
        while card_valid == False:
            try:
                player_move = int(input('Place a card (Key nr)'))
    #------------------------------------Input validation----------------------------------------------
                if not int(player_move) in self.cards.keys():
                    print(self.cards)
                    print('invalid card, try again:')
                elif self.cards[player_move] == 'Wizard' or self.cards[player_move] == 'Fool':
                    #wizard and fool can be placed at all times
                    card_valid = True
                    break
    #------------------------------------Checks if user has no round colours in case he is using another colour-------------
                elif round_colour[0] != 'None' and self.cards[player_move].split(']')[0].replace('[','') != round_colour[0]:
                    for card in self.cards.values():
                        if round_colour[0] in card:
                            #round colour found in user deck, he is forced to use either colour card or wizard/fool
                            print('You must select the round colour card if you have one in your hand!')
                            card_valid = False
                            break
                        card_valid = True
                else:
                    card_valid = True
                    break
            except:
                print('invalid key provided!')
                continue 
    
#------------------------------------Placing the card-----------------------------------------------------------------------
        if card_valid == True: 
            #card is put in the placed_card list which is then used to determined if newly put card is a winner.
            placed_card[0] = self.name 
            placed_card[1] = self.cards[player_move] 
            placed_card[2] = deck.deck_values[self.cards[player_move]][0]
            print(self.name, ' places: ',self.cards[player_move])
            if round_colour[0] == 'None' and self.cards[player_move].find('[') != -1:
            #if there was no round colour and the placed card is coloured the round colour is updated
                round_colour[0] = self.cards[player_move].split(']')[0].replace('[','')
            del self.cards[player_move] 


#--------------------------------------------------------------------- COMPUTER HAND------------------------------------------------
class Computer_Hand():
    def __init__(self,name):
        self.cards = []
        self.bid = 0
        self.name = name

    def add_card(self,card):
        #1. CPU adds cards to his hand from the deck (function connected to the deck class)
        self.cards.append(card)
    
    def place_bid(self):
        #1.CPU evalutes all his cards and based on its value and % chance determines if he wants to bid on it.
        cp_bid = 0
        for card in self.cards:
            if random.random() < deck.deck_values[card][1]:
                cp_bid += 1
        bid_list[self.name] = [cp_bid,0]
        print(self.name, ' bids ', cp_bid)

    def place_card(self): 
        #CPU place_card function:
        #1. defines what cards cpu can place in the round (cpu_round_cards list generated)
        #2. defines min/max values of his cpu_round_cards.
        #3. defines if CPU wants to win/lose, can cpu win/lose and takes the action (based on its score in the bid_list and the current winner score)
        #4. round dominant colour determined.
        cpu_round_cards = []
        for cpu_card1 in self.cards:
            if round_colour[0] == 'None':
                #1.1 no round dominant colour yet, all cards can be used:
                cpu_round_cards.append([cpu_card1, deck.deck_values[cpu_card1][0]])
                #1.2 wizard and fool can be used all the time:
            elif cpu_card1 == 'Wizard' or cpu_card1 == 'Fool':
                cpu_round_cards.append([cpu_card1, deck.deck_values[cpu_card1][0]])
            elif round_colour[0] != 'None':
                #1.3 round dominant colour exists, if cpu has card in deck he is limited to only using round dominant colour.
                cpu_w_dominant_colour = 0
                #1.3.1checks if cpu player has dominant colour
                for cpu_card2 in self.cards:
                    if round_colour[0] in cpu_card2:
                        cpu_w_dominant_colour = 1
                #1.3.2 if cpu has no round dominant all cards can be placed.Else only the round dominant ones
                if cpu_w_dominant_colour == 0 or round_colour[0] in cpu_card1:
                    if round_colour[0] in cpu_card1 or deck.dominant_colour in cpu_card1:
                        #1.3.2.1 if card is session or round dominant, it retains its value
                        cpu_round_cards.append([cpu_card1, deck.deck_values[cpu_card1][0]])
                    else: #1.3.2.2 other colour cards can be added but they have no value
                        cpu_round_cards.append([cpu_card1, 1])
                else:
                    pass    
        #2 Define max/min values
        cpu_cards_min_val = None
        cpu_cards_max_val = None
        for cpu_card3 in cpu_round_cards:     
            if cpu_cards_min_val == None or cpu_cards_min_val > cpu_card3[1]:
                cpu_cards_min_val = cpu_card3[1]
            if cpu_cards_max_val == None or cpu_cards_max_val < cpu_card3[1]:
                cpu_cards_max_val = cpu_card3[1]
        #3.defines if cpu wants to win
        if bid_list[self.name][0] > bid_list[self.name][1]:
            if cpu_cards_max_val > winner[2]:
                #3.1.1cpu wants to win and can win:
                for cpu_card1 in cpu_round_cards:
                    if cpu_card1[1] == cpu_cards_max_val:
                        #max value card is used:
                        placed_card[0] = self.name 
                        placed_card[1] = cpu_card1[0]
                        card_string  = cpu_card1[0]
                        placed_card[2] = deck.deck_values[card_string][0]
                        self.cards.remove(placed_card[1])
                        print(self.name, 'places to win:', placed_card[1])
                        break
            else:
                #3.1.2 cpu wants to win but he cannot:
                for cpu_card1 in cpu_round_cards:
                    if cpu_card1[1] == cpu_cards_min_val:
                        #min value card is used:
                        placed_card[0] = self.name 
                        placed_card[1] = cpu_card1[0]
                        card_string  = cpu_card1[0]
                        placed_card[2] = deck.deck_values[card_string][0]
                        self.cards.remove(placed_card[1])
                        print(self.name, 'places to lose:', placed_card[1])
                        break                      
        else:
            #print(self.name,' wants to lose')
            #3.2 CPU wants to lose
            #CPU is interested to place highest possible card without taking the win.
            cpu_less_than_w_card_val = None
            for cpu_card1 in cpu_round_cards:
                if cpu_less_than_w_card_val == None:
                    cpu_less_than_w_card_val = cpu_card1[1]
                    placed_card[0] = self.name 
                    placed_card[1] = cpu_card1[0]
                    card_string  = cpu_card1[0]
                    placed_card[2] = deck.deck_values[card_string][0]
            #checks if next card is higher than the existing but still lower than the currenct winner card
                elif cpu_less_than_w_card_val < cpu_card1[1] and cpu_card1[1] < winner[2]:
                    cpu_less_than_w_card_val = cpu_card1[1]
                    placed_card[0] = self.name 
                    placed_card[1] = cpu_card1[0]
                    card_string  = cpu_card1[0]
                    placed_card[2] = deck.deck_values[card_string][0]
            print(self.name, 'places to lose:', placed_card[1])
        #4. round dominant colour is determined if it was not before and the placed card is coloured.
        if round_colour[0] == 'None' and card_string.find('[') != -1:
            round_colour[0] = card_string.split(']')[0].replace('[','')  

def identify_winner():
    #Function defines the current winner of the round.
    #Runs everytime a new card is placed so the CPU knows the existing winner and can evaluate his option to go for win or loss.
        if  winner[0] == 'test':
            #first card in round, by default becomes winner.
            winner[0] = placed_card[0]
            winner[1] = placed_card[1]
            winner[2] = placed_card[2]
            #print(winner)
        elif placed_card[2] == 50 and winner[2] != 50: 
            #user has wizard card and it has not been placed in this round yet.
            winner[0] = placed_card[0]
            winner[1] = placed_card[1]
            winner[2] = placed_card[2]
            #print(winner)
        elif int(placed_card[2])  == 0 and int(placed_card[2]) == winner[2]:
            #user has fool card but it already has been placed.New placer becomes winner.
            winner[0] = placed_card[0]
            winner[1] = placed_card[1]
            winner[2] = placed_card[2]
            #print(winner)
        elif deck.dominant_colour in placed_card[1] and int(placed_card[2])> winner[2]:
            #user has session colour card that is higher than current winner score
            winner[0] = placed_card[0]
            winner[1] = placed_card[1]
            winner[2] = placed_card[2]
            #print(winner)
        elif round_colour[0] in placed_card[1] and int(placed_card[2]) > winner[2]:
            #user has round colour card that is higher than current winner score
            winner[0] = placed_card[0]
            winner[1] = placed_card[1]
            winner[2] = placed_card[2]
            #print(winner)

def round_winner_reorder():
    global player_list
    #this function reorders player_list after round (winner always starts first)
    i = 0
    for player in player_list:
        if player[0] == winner[0]:
            #winner player gets ordered first - 0 value
            player[3] = 0
            break
        else:
            i += 1
    n = 0
    for player in player_list[i:]:
        player[3] = n
        n += 1

    for player in player_list[:i]:
        player[3] = n
        n += 1
    player_list = sorted(player_list, key=lambda x: x[3], reverse=False)

def session_players_reorder():
    global player_list
#this function reorders player_list after session (sequence incrementaly increases)
    for player in player_list:
        if player[2] == len(player_list)-1:
            #last player becomes first.
            player[2] = 0
        else:
            #other players move by 1 point.
            player[2] += 1
    player_list = sorted(player_list, key=lambda x: x[2], reverse=False)     


def total_score_updater():
    #function calculates the score and updates it in player_list based on bid_list.
    #Run at the end of each session
    for player in player_list:
        player_name = player[0]
        if bid_list[player_name][0] ==  bid_list[player_name][1]:
            #player bid correctly, rewarded.
            player[1] = player[1] + (bid_list[player_name][0]*20)+20
        else:
            #player bid incorrectly, points taken away.
            diff = (abs(bid_list[player_name][0] - bid_list[player_name][1]))*10
            player[1] = player[1] - diff

   
#--------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------GAME STARTS------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

while True:
#--------------------------------------------------------------------------------------------------------------------------------
    play_question = input('Welcome to Wizard! play? (Y/N)')

    if not play_question.lower().startswith('y'):
        print('your loss!')
        break
    else:
        players_nr = False
        while players_nr == False:
            try:
                human_player = input("what's your name?: ")
                nr_players = int(input('how many CPU players you want to go against?(2-5)?'))
                if nr_players < 2 or nr_players > 5:
                    print('invalid number of players!')
                    continue
                else:
                    print("let's go!")
                    time.sleep(2)
                    break
            except:
                print('invalid number of players!')
                continue
#-------------------------------------------------------------------------------------------------------------------
        player_list = [] 
        player_list.append([human_player,0,0,0,''])
        
        random.shuffle(CPU_names)
        #Building the numbers for queueing
        nr = 1
        while nr <= nr_players:
            player_list.append([CPU_names[nr], 0, nr, nr, ''])
            player_list[nr][1] = 0
            player_list[nr][2] = nr
            player_list[nr][3] = nr
            player_list[nr][4] = ''
            nr += 1
        #print(player_list)
        print('Players!:')
        for player in player_list:
            print(player[0])

        time.sleep(2)
        total_sessions = int(60/len(player_list))
        print('Number of sessions in the game:', total_sessions)
        session_nr = 1     
    
#----------------------------------Deck initialize----------------------------------------------------------
        while session_nr <= total_sessions:
            deck = Deck_class() 
            deck.shuffle()
            #last session does not look for dominant, all deck is distributed.
            if session_nr != total_sessions: 
                deck.dominant_colour = deck.find_dominant()
            deck.evaluate_deck()
            print('--------------------------------------------------------------------------------')
            print('Session ', session_nr,'out of ',total_sessions, ' begins!')
            time.sleep(2)
            print('This Session dominates: ',deck.dominant_card)
            print('--------------------------------------------------------------------------------')
    #----------------------------------Hands----------------------------------------------------------
            for player in player_list:
                if player[0] == human_player:
                    player[4] = Hand(player[0])
                else:
                    player[4] = Computer_Hand(player[0])
            
            for player in player_list:
                card_nr = 1
                while card_nr <= session_nr:
                    player[4].add_card(deck.deal())
                    card_nr += 1
    #------------------------------------------Bidding----------------------------------------------------------
            bid_list = {}

            for player in player_list:
                player[4].place_bid()
                time.sleep(1)

            print(bid_list)
            time.sleep(2)
            print('--------------------------------------------------------------------------------')    
    #------------------------------------------Round----------------------------------------------------------
            #for i in session_nr:
            round_nr = 1
            while round_nr <= session_nr:
                winner = ['test', 'test', 0]
                placed_card = ['test', 'test', 0]
                round_colour = ['None'] 
                print('Round ', str(round_nr), ' begins!')
                print('--------------------------------------------------------------------------------')
                time.sleep(2)
#------------------------------------------Placing cards----------------------------------------                
                for player in player_list:
                    player[4].place_card()
                    identify_winner()
                    time.sleep(1)
                
                #updating bid_list
                winner2 = winner[0]
                bid_list[winner2][1] = bid_list[winner2][1] +1

#------------------------------------------Declaring winner-------------------------------------------------------
                print('--------------------------------------------------------------------------------')
                print(winner[0], 'wins round number ',str(round_nr),'!, score: ', winner[2])
                print('--------------------------------------------------------------------------------')
                print('Score of this session:')
                print(bid_list)
                time.sleep(2)
                
                #reorder sequence based on winner
                round_winner_reorder()
                round_nr += 1
#------------------------------------------------------------------------------------
            total_score_updater()
            time.sleep(2)    
            print('Results: (sessions ,',session_nr,'/',total_sessions, ')')
            for player in player_list:
                print(player[0], 'score: ', player[1],'bids/wins: ', bid_list[player[0]])
            session_players_reorder()
            #next session!  
            session_nr += 1  
            continue

        print('--------------------------------------------------------------------------------')
        print('-----------------------------Game over------------------------------------------')
        print('--------------------------------------------------------------------------------')


        



   


  
  
  