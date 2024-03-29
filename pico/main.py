import time
from ConfigSrv import ConfigSrv
from Rover import Rover
import ujson
from machine import I2C, Pin
from mpu9250 import MPU9250
import VL53L0X
from ina219 import INA219
import logging

srv = ConfigSrv()
i = 0
rover = Rover()

i2c = I2C(1, scl=Pin(27), sda=Pin(26))
try:
    sensor = MPU9250(i2c)
except:
    print("[WARN] MPU sensor disabled")

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c)

SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS, i2c, log_level=logging.INFO)
ina.configure()

class WDT:

    def __init__(self, rover: Rover) -> None:
        self.wdtTimer = 0
        self.rover = rover
        pass
    def feed(self):
        self.wdtTimer = 0
    def wdtCtrl(self):
        self.wdtTimer = self.wdtTimer + 1
        if ((not self.rover.isFailsafeEngaged()) and (self.wdtTimer > int(srv.getValue("wdt_timeout_ms") / srv.getValue("baseline_rate_ms")))):
            self.handleFailSafe()
    def handleFailSafe(self):
        self.rover.engageFailsafe()
    
wdt = WDT(rover)

def handleLineFromRPi(line):
    global wdt
    try:
        l = ujson.loads(line)
        if(l['type'] == "RC_CHANNELS_SCALED"):
            rover.handleCtrlCmd(l['chan1_scaled'], l['chan2_scaled'])
        if(l['type'] == "HEARTBEAT"):
            wdt.feed()
    except ValueError:
        pass

def sendImu():
    global sensor
    if sensor:
        acc = sensor.acceleration
        gyro = sensor.gyro
        mag = sensor.magnetic
        msg = {
            "type": "HIGHRES_IMU",
            "xacc": acc[0],
            "yacc": acc[1],
            "zacc": acc[2],
            "xgyro": gyro[0],
            "ygyro": gyro[1],
            "zgyro": gyro[2],
            "xmag": mag[0],
            "ymag": mag[1],
            "zmag": mag[2],
            "temperature": sensor.temperature
        }
        print(ujson.dumps(msg))

def sendDistance() :
    global tof
    tof.start()
    MAV_DISTANCE_SENSOR_LASER = 0
    MAV_FRAME_BODY_FRD = 12
    msg = {
        "type" : "OBSTACLE_DISTANCE",
        "frame" : MAV_FRAME_BODY_FRD,
        "sensor_type" : MAV_DISTANCE_SENSOR_LASER,
        "distances" : tof.read() / 10
    }
    print(ujson.dumps(msg))

def sendBatteryStatus():
    global ina
    msg = {
        "type": "BATTERY_STATUS",
        "voltages": ina.voltage(),
    }
    #print("Bus Voltage: %.3f V" % ina.voltage())
    #print("Current: %.3f mA" % ina.current())
    #print("Power: %.3f mW" % ina.power())
    print(ujson.dumps(msg))

def sendHeartbeat():
    global rover
    # MAV_STATE_STANDBY - 3
    # MAV_STATE_ACTIVE - 4
    # MAV_STATE_CRITICAL - 5
    if (rover.isFailsafeEngaged()):
        status = 5
    else:
        status = 4
    msg = {
        "type": "HEARTBEAT",
        "autopilot" : 0, # MAV_AUTOPILOT_GENERIC
        "base_mode" : 64, # MAV_MODE_FLAG_MANUAL_INPUT_ENABLED
        "system_status" : status
    }
    print(ujson.dumps(msg))

def mainLoop(timer):
    global i
    baseline_rate_ms = srv.getValue("baseline_rate_ms")
    attitude_rate_ticks = int(srv.getValue("attitude_rate_ms") / baseline_rate_ms)
    power_rate_ticks = int(srv.getValue("power_rate_ms") / baseline_rate_ms)
    heartbeat_rate_ticks = int(srv.getValue("heartbeat_rate_ms")/ baseline_rate_ms)
    distance_rate_ticks = int(srv.getValue("distance_rate_ms")/ baseline_rate_ms)
    

    if (i % attitude_rate_ticks == 0):
        sendImu()

    if (i % power_rate_ticks == 0):
        sendBatteryStatus()

    if (i % heartbeat_rate_ticks == 0):
        sendHeartbeat()
    
    if (i % distance_rate_ticks == 0):
        sendDistance()

    # WDT
    wdt.wdtCtrl()

    # Loop
    i = i + 1

from machine import Timer

tim = Timer(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print("init"))
tim.init(period=100, mode=Timer.PERIODIC, callback=mainLoop)

