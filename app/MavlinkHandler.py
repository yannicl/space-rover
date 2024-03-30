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

    # this is not yet called
    def handle(self, msg: MAVLink_message):
        print (msg.to_dict())
        if (msg.get_type() == "HEARTBEAT"):
            return
        elif(msg.get_type() == "PARAM_VALUE"):
            self.config.updateParam(msg.param_id, msg.param_value)
            return
        elif(msg.get_type() == "RC_CHANNELS_SCALED"):
            if (self.picoHandler is not None):
                self.picoHandler.sendCtrlCmd(msg.chan1_scaled, msg.chan2_scaled)
            return
        
    def listen(self):
        while True:
            msg = self.mav.recv_match(blocking=True)
            if (msg) :
                self.handle(msg)

            
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
        # battery cell goes from 3.2 to 4.2v
        r = int((v - (3 * 3.2)) / (3) * 100)
        """
        Battery information

        id                        : Battery ID (type:uint8_t)
        battery_function          : Function of the battery (type:uint8_t, values:MAV_BATTERY_FUNCTION)
        type                      : Type (chemistry) of the battery (type:uint8_t, values:MAV_BATTERY_TYPE)
        temperature               : Temperature of the battery. INT16_MAX for unknown temperature. [cdegC] (type:int16_t)
        voltages                  : Battery voltage of cells 1 to 10 (see voltages_ext for cells 11-14). Cells in this field above the valid cell count for this battery should have the UINT16_MAX value. If individual cell voltages are unknown or not measured for this battery, then the overall battery voltage should be filled in cell 0, with all others set to UINT16_MAX. If the voltage of the battery is greater than (UINT16_MAX - 1), then cell 0 should be set to (UINT16_MAX - 1), and cell 1 to the remaining voltage. This can be extended to multiple cells if the total voltage is greater than 2 * (UINT16_MAX - 1). [mV] (type:uint16_t)
        current_battery           : Battery current, -1: autopilot does not measure the current [cA] (type:int16_t)
        current_consumed          : Consumed charge, -1: autopilot does not provide consumption estimate [mAh] (type:int32_t)
        energy_consumed           : Consumed energy, -1: autopilot does not provide energy consumption estimate [hJ] (type:int32_t)
        battery_remaining         : Remaining battery energy. Values: [0-100], -1: autopilot does not estimate the remaining battery. [%] (type:int8_t)

        """
        self.mav.mav.battery_status_send(id=1,battery_function=1, type=1, temperature=32767, voltages=[int(v * 1000), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], current_battery=-1, current_consumed=-1, energy_consumed=-1, battery_remaining=r)

    def sendObstacleDistance(self, data):
        self.mav.mav.rangefinder_send(voltage=0.0, distance=data['distances'])


if __name__ == '__main__':
    srv = ConfigSrv()
    handler = MavlinkHandler(srv)
    msg = MAVLink_message(1, "PARAM_VALUE")
    msg.param_id = "SURFACE_DEPTH"
    msg.param_value = "-2"
    handler.handle(msg)
        
