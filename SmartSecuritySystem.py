class keypad:
    def __init__(self, rows = [11,13,15,29], columns = [31,33,35,37], keyLabel = [['1','2','3','A'],['4','5','6','B'],['7','8','9','C'],['*','0','#','D']], retChar = 'D'):
        self.rows = rows
        self.columns = columns 
        self.keyLabel = keyLabel
        self.retChar = retChar
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        for i in rows :
            GPIO.setup(i, GPIO.OUT)
        for j in columns :
            GPIO.setup(j, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

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

myKeypad = keypad()
password = myKeypad.readKeypad()
print(password)
GPIO.cleanup()