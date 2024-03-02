import sys
import time
from pymavlink import mavutil

mav = mavutil.mavlink_connection('tcp:127.0.0.1:5760')

while True:
    mav.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_QUADROTOR,
                           mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    print(".", end="")
    sys.stdout.flush()
    time.sleep(1)