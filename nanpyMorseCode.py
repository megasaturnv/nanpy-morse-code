#!/usr/bin/python3
import time, nanpy, nanpy.arduinotree

try:
    import readline
except:
    pass #readline not available

DEBUG_MODE=True
FAKE_AN_ARDUINO_MODE=False
MORSE_PIN=13
ARDUINO_SERIAL_DEVICE='/dev/serial0'
UNIT_TIME=0.1 #Time of a unit, in seconds
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
	if DEBUG_MODE:
		print('.', end='')
	aa.digitalWrite(MORSE_PIN, aa.HIGH)
	time.sleep(UNIT_TIME)
	aa.digitalWrite(MORSE_PIN, aa.LOW)
	time.sleep(UNIT_TIME)

def sendDash():
	if DEBUG_MODE:
		print('-', end='')
	aa.digitalWrite(MORSE_PIN, aa.HIGH)
	time.sleep(3 * UNIT_TIME)
	aa.digitalWrite(MORSE_PIN, aa.LOW)
	time.sleep(UNIT_TIME)

def sendLetterSpace():
	if DEBUG_MODE:
		print(' ', end='')
	aa.digitalWrite(MORSE_PIN, aa.LOW)
	time.sleep(2 * UNIT_TIME) # 3-1 * UNIT_TIME because 1 unit time after every . or -

def sendWordSpace():
	if DEBUG_MODE:
		print('/', end='')
	aa.digitalWrite(MORSE_PIN, aa.LOW)
	time.sleep(6 * UNIT_TIME) # 7-1 * UNIT_TIME because 1 unit time after every . or -

def sendMorse(morse):
	if not FAKE_AN_ARDUINO_MODE:
		for m in morse:
			if m == ".":
				sendDot()
			elif m == "-":
				sendDash()
			elif m == "/":
				sendWordSpace()
			elif m == " ":
				sendLetterSpace()

if not FAKE_AN_ARDUINO_MODE:
	connection = nanpy.SerialManager(device=ARDUINO_SERIAL_DEVICE)

	aa = nanpy.ArduinoApi(connection=connection)
	at = nanpy.arduinotree.ArduinoTree(connection=connection)

	aa.pinMode(MORSE_PIN, aa.OUTPUT)
	aa.digitalWrite(MORSE_PIN, aa.LOW)

print("Type 'QUIT' to exit the program")
print("Enter the text you want to send via morse code:")

if DEBUG_MODE:
	print("Info: Program in DEBUG_MODE")
if	FAKE_AN_ARDUINO_MODE:
	print("Info: Program in FAKE_AN_ARDUINO_MODE")

inp = ""
while inp != "QUIT":
	inp = input("> ")
	if inp != "QUIT":
		sendMorse(textToMorse(inp))

if not FAKE_AN_ARDUINO_MODE:
	aa.digitalWrite(MORSE_PIN, aa.LOW)
	aa.pinMode(MORSE_PIN, aa.INPUT)
