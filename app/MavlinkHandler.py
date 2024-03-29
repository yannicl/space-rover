from pymavlink.dialects.v20.ardupilotmega import MAVLink_message
from ConfigSrv import ConfigSrv
from pymavlink import mavutil
import time

class MavlinkHandler:

    def __init__(self, confisrv: ConfigSrv):
        self.config = confisrv
        self.mav = mavutil.mavlink_connection('tcp:192.168.0.195:5760')

    def registerPicoHandler(self, picoHandler):
        self.picoHandler = picoHandler

    def handle(self, msg: MAVLink_message):
        print (msg.to_dict())
        if (msg.get_type() == "HEARTBEAT"):
            return
        elif(msg.get_type() == "PARAM_VALUE"):
            self.config.updateParam(msg.param_id, msg.param_value)
            return
        elif(msg.get_type() == "RC_CHANNELS_SCALED"):
            self.picoHandler.sendCtrlCmd(msg.chan1_scaled, msg.chan2_scaled)
            return

            
    def sendImu(self, data):
        # time_usec                 : Timestamp (UNIX Epoch time or time since system boot). The receiving end can infer timestamp format (since 1.1.1970 or since system boot) by checking for the magnitude of the number. [us] (type:uint64_t)
        # xacc                      : X acceleration [m/s/s] (type:float)
        # yacc                      : Y acceleration [m/s/s] (type:float)
        # zacc                      : Z acceleration [m/s/s] (type:float)
        # xgyro                     : Angular speed around X axis [rad/s] (type:float)
        # ygyro                     : Angular speed around Y axis [rad/s] (type:float)
        # zgyro                     : Angular speed around Z axis [rad/s] (type:float)
        # xmag                      : X Magnetic field [gauss] (type:float)
        # ymag                      : Y Magnetic field [gauss] (type:float)
        # zmag                      : Z Magnetic field [gauss] (type:float)
        # abs_pressure              : Absolute pressure [hPa] (type:float)
        # diff_pressure             : Differential pressure [hPa] (type:float)
        # pressure_alt              : Altitude calculated from pressure (type:float)
        # temperature               : Temperature [degC] (type:float)
        # fields_updated            : Bitmap for fields that have updated since last message, bit 0 = xacc, bit 12: temperature (type:uint16_t)
        # id                        : Id. Ids are numbered from 0 and map to IMUs numbered from 1 (e.g. IMU1 will have a message with id=0) (type:uint8_t)
        self.mav.mav.highres_imu_send(
            time_usec=int(time.time() * 1000000),
            xacc=data['xacc'],
            yacc=data['yacc'],
            zacc=data['zacc'],
            xgyro=data['xgyro'],
            ygyro=data['ygyro'],
            zgyro=data['zgyro'],
            xmag=data['xmag'],
            ymag=data['ymag'],
            zmag=data['zmag'],
            abs_pressure=0,
            diff_pressure=0,
            pressure_alt=0,
            fields_updated=0,
            temperature=data['temperature']
        )

    def sendBatteryStatus(self, data):
        v = data['voltages']
        r = int((v - (3 * 3.2)) / (3 * 4.2) * 100)
        self.mav.mav.battery_status_send(battery_remaining=r)

    def sendObstacleDistance(self, data):
        self.mav.mav.rangefinder_send(voltage=0, distance=[data['distances']])


if __name__ == '__main__':
    srv = ConfigSrv()
    handler = MavlinkHandler(srv)
    msg = MAVLink_message(1, "PARAM_VALUE")
    msg.param_id = "SURFACE_DEPTH"
    msg.param_value = "-2"
    handler.handle(msg)
        
