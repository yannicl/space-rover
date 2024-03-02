import sched, time
from ConfigSrv import ConfigSrv
from PicoHandler import PicoHandler
from MavlinkHandler import MavlinkHandler

class Tasks:

    HIGH_PRIORITY = 1
    NORMAL_PRIORITY = 5
    LOW_PRIORITY = 10

    def __init__(self, confisrv: ConfigSrv):
        self.config = confisrv
        self.s = sched.scheduler(time.monotonic, time.sleep)
        self.sendGpsData()

    def registerPicoHandler(self, h : PicoHandler):
        self.picoHandler = h
        self.sendHeartbeatToPico()
        self.picoHandlerRead()

    def sendGpsData(self):
        self.s.enter(float(self.config.getValue("gps_rate_ms")) / 1000, self.NORMAL_PRIORITY, self.sendGpsData)
        print("SEND GPS")

    def sendHeartbeatToPico(self):
        self.s.enter(float(self.config.getValue("pico_hearbeat_rate_ms")) / 1000, self.NORMAL_PRIORITY, self.sendHeartbeatToPico)
        self.picoHandler.heartbeat()

    def picoHandlerRead(self):
        self.s.enter(100 / 1000, self.NORMAL_PRIORITY, self.picoHandlerRead)
        self.picoHandler.readAndHandle()
        

    def run(self, blocking=True):
        self.s.run(blocking)

if __name__ == '__main__':
    srv = ConfigSrv()
    tasks = Tasks(srv)
    ph = PicoHandler()
    ph.registerMavlinkHandler(MavlinkHandler(srv))
    tasks.registerPicoHandler(ph)
    tasks.run()


# send gps every 15s

# send modbus request

# https://micropython-modbus.readthedocs.io/en/latest/EXAMPLES.html



