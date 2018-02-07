#!/usr/bin/python3
import time, nanpy, nanpy.arduinotree

try:
    import readline
except:
    pass #readline not available

DEBUG_MODE=True
MORSE_PIN=13
unitTime=0.1 #Time of a unit, in seconds
#If the duration of a dot is taken to be one unit then that of a dash is three units. The space between the components of one character is one unit, between characters is three units and between words seven units.
#dot = 1
#dash = 3
#between dots and dashes = 1
##between letters = 3
#between words = 7

toMorse = dict({
" ": "/",
"A": ".-",     "B": "-...",   "C": "-.-.",   "D": "-..",    "E": ".",
"F": "..-.",   "G": "--.",    "H": "....",   "I": "..",     "J": ".---",
"K": "-.-",    "L": ".-..",   "M": "--",     "N": "-.",     "O": "---",
"P": ".--.",   "Q": "--.-",   "R": ".-.",    "S": "...",    "T": "-",
"U": "..-",    "V": "...-",   "W": ".--",    "X": "-..-",   "Y": "-.--",
"Z": "--..",
"0": "-----", "1": ".----",  "2": "..---",  "3": "...--",  "4": "....-",
"5": ".....", "6": "-....",  "7": "--...",  "8": "---..",  "9": "----.",
})

def textToMorse(text):
	morse = ""
	for character in text:
		if character != " ":
			morse+= toMorse[character.upper()]
			morse+= " "
		else:
			morse = morse[:-1]
			morse+= toMorse[character.upper()]

	morse = morse[:-1]
	if DEBUG_MODE:
		print(morse)
	return morse

def sendDot():
	aa.digitalWrite(MORSE_PIN, aa.HIGH)
	time.sleep(unitTime)
	aa.digitalWrite(MORSE_PIN, aa.LOW)
	time.sleep(unitTime)

def sendDash():
	aa.digitalWrite(MORSE_PIN, aa.HIGH)
	time.sleep(3*unitTime)
	aa.digitalWrite(MORSE_PIN, aa.LOW)
	time.sleep(unitTime)

def sendWordSpace():
	aa.digitalWrite(MORSE_PIN, aa.LOW)
	time.sleep(6*unitTime) # 7-1 * unitTime because 1 unit time after every . or -

def sendLetterSpace():
	aa.digitalWrite(MORSE_PIN, aa.LOW)
	time.sleep(2*unitTime) # 3-1 * unitTime  because 1 unit time after every . or -

def sendMorse(morse):
	for m in morse:
		if m == ".":
			sendDot()
		elif m == "-":
			sendDash()
		elif m == "/":
			sendWordSpace()
		elif m == " ":
			sendLetterSpace()

def sendText(text):
	sendMorse(textToMorse(text))

connection = nanpy.SerialManager(device='/dev/serial0')

aa = nanpy.ArduinoApi(connection=connection)
at = nanpy.arduinotree.ArduinoTree(connection=connection)

aa.pinMode(MORSE_PIN, aa.OUTPUT)
aa.digitalWrite(MORSE_PIN, aa.LOW)

print("Type 'QUIT' to exit the program")
print("Enter the text you want to send via morse code:")

inp = ""
while inp != "QUIT":
	inp = input("> ")
	if inp != "QUIT":
		sendText(inp)

aa.digitalWrite(MORSE_PIN, aa.LOW)
aa.pinMode(MORSE_PIN, aa.INPUT)
