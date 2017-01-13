#import pyb
import os
import ubinascii
import utime

try:
	import pyb
	print("Running on a PYB")
	red = pyb.LED(1)
	grn = pyb.LED(2)
	yel = pyb.LED(3)
	blu = pyb.LED(4)	
	sw  = pyb.Switch()
except ImportError:
	# Create dummy pyb module
	print("Not running on a PYB")
	class LED:
		'Dummy LED class for non PYB boards'
		state = 0
		def __init__(self, name):
			self.name = name
		def on(self):
			'turns LED on'	
			state = 1
			return
		def off(self):
			'turns LED off'
			state = 0
			return
try:
	red
except NameError:
	print("WiPy Initialisation")
	red = LED(1)
	grn = LED(2)
	yel = LED(3)
	blu = LED(4)

# Timers 1,2,4,7-14 available for use
#ti = pyb.Timer(4, freq=4)

# Ensure all LEDs are off 
red.off()
grn.off()
yel.off()
blu.off()

# Setup callback to toggle Yellow LED when the switch is pressed
try:
	sw.callback(lambda:yel.toggle())
except NameError:
	print('Stil need to implement switch input on WiPy')

# Declare and define Globals
Number_of_cards_to_deal = 5
Master_Pack = [1,2,3,4,5,6,7,8,9,10]
Pack = []
SelectedCards = []

def play():
    #
    # pack of cards
    # select N from pack of cards
    for i in range(0, len(Master_Pack)):
        Pack.append(Master_Pack[i])
    deal(Number_of_cards_to_deal)
    #print("Remaining: ", Pack)
    #print("Selected: ", SelectedCards)
    N = len(SelectedCards)
    M = 0
    Score = 0
    print("")	
    print("Welcome to MicroPython Play your Cards Right")
    print("============================================")	
    while M < (N-1):
        #print("Turn: ", M)
        if turn(M):
            Score = Score + 1
        #print("Score: ", Score)
        M += 1		
        utime.sleep_ms(2000)
        # move to next card...
    print("Score: ", Score, "out of ", N-1)
    # Tidy Up
    for i in range(0, N):
        del SelectedCards[0]
    for i in range(0,len(Pack)):
        del Pack[0]	
    utime.sleep_ms(1000)
    red.off()
    grn.off()
    yel.on()
    print("Bye")
		
def deal(NumCardsToDeal):
    #card = 1
    for i in range(0, NumCardsToDeal):
        #SelectedCards.append(random.choice(cards))		
        NumCards = len(Pack)
        if 0 < NumCards:
            # Select a card at random from those left in the pack		
            card = random(NumCards)
            SelectedCards.append(Pack[card])
            Pack.remove(Pack[card])

			
def random(NumRandomValues):
    # Random number from 0 to NumRandomValues-1
    return (int(ubinascii.hexlify(os.urandom(1)), 16) % NumRandomValues)			
		
		
def turn(M):		
    # reveal selected card M
    if M == 0:
        # First round we need to start with a card	    
		print("First card: ", SelectedCards[M])
    blu.on()
    # request input H or L
    Guess = input("Do you think the next card is higher or lower?")
    Guess = Guess.lstrip()  # Remove whitespace from left of string
    Guess = Guess.upper()   # Force string to upper case 
    #print("I think you said:", Guess)
    blu.off()
    # reveal selected card M+1
    print("Card: ", SelectedCards[M+1], end=" ")
    # compare card M and M+1 : > or < 
    Difference = SelectedCards[M+1] - SelectedCards[M]
    #print("Difference:", Difference)
    if Difference < 0:
        # Lower
        #print("Lower")
        Result = 'L'
    elif Difference > 0:
        # Higher
        #print("Higher")
        Result = 'H'
    else:
        # Equal
        Result = 'E'
    # Score Result	
    if Result == Guess[0]:
        # Correct
        print("CORRECT - you win!!!")
        grn.on()
        red.off()
        return 1
    else:	
        # Wrong
        print("WRONG - sorry")
        red.on()
        grn.off()
        return 0





