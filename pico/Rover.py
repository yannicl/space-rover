import neopixel
from machine import Pin, PWM

# Motors
# GPIO 10, 11, 12 + GPIO 19

class Rover:

    def __init__(self) -> None:
        self.n = neopixel.NeoPixel(Pin(3), 4)
        self.failsafe = False
        self.motorAF = PWM(Pin(8), freq=50)
        self.motorAR = PWM(Pin(10), freq=50)
        return
    
    def handleCtrlCmd(self, leftPwr: int, rightPwr: int):
        if (leftPwr >= 0) :
            c1 = (leftPwr, 0, 0)
            self.motorAF.duty_u16(leftPwr << 8)
            self.motorAR.duty_u16(0)
        else:
            c1 = (0, -1 * leftPwr, 0)
            self.motorAF.duty_u16(0)
            self.motorAR.duty_u16(-1 * leftPwr << 8)
        if (rightPwr >= 0) :
            c2 = (rightPwr, 0, 0)
        else:
            c2 = (0, -1 * rightPwr, 0)
        self.n[0] = c1
        self.n[1] = c2
        self.n.write()

    def isFailsafeEngaged(self):
        return self.failsafe

    def engageFailsafe(self):
        self.failsafe = True

    def disengageFailsafe(self):
        self.failsafe = False

    
        
