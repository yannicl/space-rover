import time
from ConfigSrv import ConfigSrv
from Rover import Rover
import ujson

#See https://docs.micropython.org/en/latest/library/pyb.USB_VCP.html#pyb.USB_VCP

# PC specific
import serial

ser = serial.Serial('/dev/pts/7', 115200, timeout=0)

srv = ConfigSrv()
i = 0
rover = Rover()

class WDT:

    def __init__(self) -> None:
        self.wdtTimer = 0
        self.failsafe = False
        pass
    def feed(self):
        self.wdtTimer = 0
    def wdtCtrl(self):
        self.wdtTimer = self.wdtTimer + 1
        if ((not self.failsafe) and (self.wdtTimer > int(srv.getValue("wdt_timeout_ms") / srv.getValue("baseline_rate_ms")))):
            self.handleFailSafe()
    def handleFailSafe(self):
        self.failsafe = True
        print("WARN:FailSafe activated")
    
wdt = WDT()

def handleLineFromRPi(line):
    try:
        l = ujson.load(line)
        match(l.type):
            case "RC_CHANNELS_SCALED":
                rover.handleCtrlCmd(l.chan1_scaled, l.chan2_scaled)
            case "HEARTBEAT":
                wdt.wdtFeed()
    except ValueError:
        pass




def sendImu():
    msg = {
        "type": "HIGHRES_IMU",
        "xacc": 0,
        "yacc": 0,
        "zacc": 0,
        "xgyro": 0,
        "ygyro": 0,
        "zgyro": 0,
        "xmag": 0,
        "ymag": 0,
        "zmag": 0,
        "temperature": 0
    }
    print(ujson.dumps(msg))
    ser.write(bytes(ujson.dumps(msg), "utf-8"))

def sendBatteryStatus():
    msg = {
        "type": "BATTERY_STATUS",
        "voltages": 0,
    }
    print(ujson.dumps(msg))

while True:
    baseline_rate_ms = srv.getValue("baseline_rate_ms")
    attitude_rate_ticks = int(srv.getValue("attitude_rate_ms") / baseline_rate_ms)
    power_rate_ticks = int(srv.getValue("power_rate_ms") / baseline_rate_ms)
    

    if (i % attitude_rate_ticks == 0):
        sendImu()

    if (i % power_rate_ticks == 0):
        sendBatteryStatus()

    # Communication with RPi
    line = ser.readline()
    if line:
        print(line)

    # WDT
    wdt.wdtCtrl()

    # Loop
    i = i + 1
    time.sleep(baseline_rate_ms / 1000)