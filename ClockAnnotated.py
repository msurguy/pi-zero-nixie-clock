import time
from gpiozero import LED
from datetime import datetime
import random
import pytz

# Assign pins to control Anodes
anode1 = LED(22)
anode2 = LED(27)
anode3 = LED(18)
anode4 = LED(17)

# Assign pins to control Cathodes
cathode1_a = LED(26)
cathode1_b = LED(16)
cathode1_c = LED(20)
cathode1_d = LED(19)

cathode2_a = LED(13)
cathode2_b = LED(12)
cathode2_c = LED(6)
cathode2_d = LED(5)

# Create arrays for convenience
anodes = [anode1, anode2, anode3, anode4]
cathodeGroup_1 = [cathode1_a, cathode1_b, cathode1_c, cathode1_d]
cathodeGroup_2 = [cathode2_a, cathode2_b, cathode2_c, cathode2_d]

# Describe which cathodes correspond to numbers 0 - 9, array index represents the actual digit shown
cathodeInBinary = ['0000','1001','0001','1110','0110','1010','0010','1100','0100','1000']

try:
    # Function that turns pins on and off depending on the bit string
    def outputBits(destinationPins, bits = '1111'):
        for i, pin in enumerate(destinationPins):
            if bits[i] == '1':
                pin.on()
            else:
                pin.off()     

    # Given a string of bits and two numbers, turns on cathodes to show those numbers on tubes turned on via anode bit string
    # Usage: showDigits('0001', 2, 5) will show numbers 2 and 5 on 1nd and 3rd nixie tube
    def showDigits(anodeBits = '0000', firstDigit = 0, secondDigit = 0):
        
        # Determine cathode string corresponding to the numerical representation of the first digit
        if firstDigit >= 0:
            cathodesForFirstDigit = cathodeInBinary[firstDigit]
        else:
            cathodesForFirstDigit = '1111'

        # Determine cathode string corresponding to the numerical representation of the second digit
        if secondDigit >= 0:
            cathodesForSecondDigit = cathodeInBinary[secondDigit]
        else:
            cathodesForSecondDigit = '1111'

        # Iterate through cathode pins for each cathode group and turn on appropriate cathodes
        outputBits(cathodeGroup_1, cathodesForFirstDigit)
        outputBits(cathodeGroup_2, cathodesForSecondDigit)

        # Iterate through anode pins and turn on appropriate anodes
        outputBits(anodes, anodeBits)

        # Implement a small delay before turning the tubes off
        time.sleep(0.005)

        for anode in anodes:
            anode.off()

        # Setting all cathode outputs to 1 actually turns the bulbs off
        outputBits(cathodeGroup_1, '1111')
        outputBits(cathodeGroup_2, '1111')

        #implement a small delay before another cycle kicks in
        time.sleep(0.003)

    while True:
        # Get the local time
        now = datetime.now(pytz.timezone('US/Pacific'))
        clockDigits = [now.minute % 10, now.minute // 10, now.hour % 10, now.hour//10] 
        
        # Display digits on the nixie tubes
        showDigits('0001', clockDigits[3], clockDigits[0]) # Turns on digits on 1 and 3rd tube
        showDigits('0110', clockDigits[1], clockDigits[2]) # Turns on digits on 2 and 4th tube

except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    #anode1.off()
    print "\nExiting" # print value of counter  