class keypad:
    def __init__(self, rows = [11,13,15,29], columns = [31,33,35,37], keyLabel = [['1','2','3','A'],['4','5','6','B'],['7','8','9','C'],['*','0','#','D']], retChar = 'D'):
        self.rows = rows
        self.columns = columns 
        self.keyLabel = keyLabel
        self.retChar = retChar
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        for i in rows :
            GPIO.setup(i, GPIO.OUT)         # Configure Row Pins as Output pins
        for j in columns :
            GPIO.setup(j, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)        # Configure Column Pins as Input pins

    def readKeypad(self) :
        noPress = True
        noPressOld = True
        String = ''
        while True : 
            noPress = True
            for i in [0,1,2,3] :
                for j in [0,1,2,3]:
                    GPIO.output(self.rows[i], GPIO.HIGH)
                    butVal = GPIO.input(self.columns[j])
                    GPIO.output(self.rows[i], GPIO.LOW)
                    if butVal == 1:
                        myChar = keyLabel[rows[i]][columns[j]]
                        if myChar == retChar :
                            return String
                        noPress = False
                    if butVal==1 and noPress==False and noPressOld == True :
                        String = String + myChar
            noPressOld = noPress

import RPi.GPIO as GPIO
from time import sleep
import threading 

import LCD1602  
LCD1602.init(0x27,1)                    # LCD1602 uses I2C Protocol       

myPad = keypad()
password = '1234'                       #Password set to 1234 for initial use 
myString = ''

# BACKGROUND THREAD
# TASK : Keep reading input from Keypad
def readKP() :
    global myString
    while myString != '*' :             # Use * character to exit the program
        myString = myPad.readKeypad()
        sleep(0.2)

readThread = threading.Thread(target = readKP)
readThread.daemon = True                # Daemon helps kill the thread once the program is terminated 
readThread.start()


# MAIN THREAD 
# TASK : Initialize 3 Modes of Operation 
while myString != '*':
    CMD = myString                      # myString is a global variable and can change it's value at any instant
    if CMD == 'A' + password:           # Mode : ARMED 
        LCD1602.write(0,0,'ARMED !!')
    
    if CMD == 'B' + password:           # Mode : Unarmed 
        LCD1602.write(0,0,'UnArmed !!')

    if CMD == 'C' + password:           # Mode : Change Password
        LCD1602.write(0,0,'Password ?')
        while CMD == 'C' + password:
            pass
        password = myString 
        LCD1602.write(0,0,'Password is :')
        LCD1602.write(0,1,password)
        sleep(5)

sleep(0.2)
GPIO.cleanup()
print('GPIO Pins cleared !!')


