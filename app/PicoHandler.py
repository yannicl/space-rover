import serial
from MavlinkHandler import MavlinkHandler
import ujson

class PicoHandler:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)
        return
    
    def registerMavlinkHandler(self, mavlink: MavlinkHandler):
        self.mavlink = mavlink
        self.mavlink.registerPicoHandler(self)
    
    def sendHeartbeat(self):
        msg = bytes("{\"type\":\"HEARTBEAT\"}", 'utf-8')
        self.sendGenericMessage(msg)

    def sendCtrlCmd(self, motorA, motorB):
        msg = {
            "type":"RC_CHANNELS_SCALED",
            "chan1_scaled":motorA,
            "chan2_scaled":motorB
        }
        self.sendGenericMessage(msg)
        
    def sendGenericMessage(self, msg):
        global ser
        cmd = "handleLineFromRPi(\"" + ujson.dumps(msg).replace('"','\\\"') + "\")"
        self.sendGenericCommands(cmd)
        ser.write(cmd.encode("utf-8"))
        ser.write( b'\x04' )

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
            if (data.typ == "OBSTACLE_DISTANCE"):
                self.mavlink.sendObstacleDistance(data)
        except Exception as inst:
            print(inst)
            pass
    