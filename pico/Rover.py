import neopixel
from machine import Pin, PWM

# Motors
# GPIO 10, 11, 12 + GPIO 19

class Rover:

    def __init__(self) -> None:
        self.n = neopixel.NeoPixel(Pin(3), 4)
        self.failsafe = False
        self.motorRF = PWM(Pin(11), freq=50, duty_u16=0)
        self.motorRR = PWM(Pin(8), freq=50, duty_u16=0)
        self.motorLF = PWM(Pin(12), freq=50, duty_u16=0)
        self.motorLR = PWM(Pin(10), freq=50, duty_u16=0)
        return
    
    def handleCtrlCmd(self, leftPwr: int, rightPwr: int):
        if (leftPwr >= 0) :
            c1 = (leftPwr, 0, 0)
            self.motorLR.duty_u16(0)
            self.motorLF.duty_u16(leftPwr << 8)
        else:
            c1 = (0, -1 * leftPwr, 0)
            self.motorLF.duty_u16(0)
            self.motorLR.duty_u16((-1 * leftPwr) << 8)
        if (rightPwr >= 0) :
            c2 = (rightPwr, 0, 0)
            self.motorRR.duty_u16(0)
            self.motorRF.duty_u16(rightPwr << 8)
        else:
            c2 = (0, -1 * rightPwr, 0)
            self.motorRF.duty_u16(0)
            self.motorRR.duty_u16((-1 * rightPwr) << 8)
        self.n[0] = c1
        self.n[1] = c2
        self.n.write()

    def isFailsafeEngaged(self):
        return self.failsafe

    def engageFailsafe(self):
        self.failsafe = True

    def disengageFailsafe(self):
        self.failsafe = False

    
        
