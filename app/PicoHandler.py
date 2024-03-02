import serial
from MavlinkHandler import MavlinkHandler
import ujson

class PicoHandler:
    def __init__(self):
        self.ser = serial.Serial('/dev/pts/6', 115200, timeout=0)
        return
    
    def registerMavlinkHandler(self, mavlink: MavlinkHandler):
        self.mavlink = mavlink
    
    def heartbeat(self):
        msg = bytes("{\"type\":\"HEARTBEAT\"}", 'utf-8')
        self.ser.write(msg)

    def readAndHandle(self):
        line = self.ser.readline()
        if (line):
            self.handle(line)
    
    def handle(self, line):
        print(line)
        try:
            data = ujson.loads(line)
            print(data)
            if (data['type'] == "HIGHRES_IMU"):
                self.mavlink.sendImu(data)
            if (data.type == "BATTERY_STATUS"):
                self.mavlink.sendBatteryStatus(data)
        except Exception as inst:
            print(inst)
            pass
    