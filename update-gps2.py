from gps3.agps3threaded import AGPS3mechanism
from pymavlink import mavutil


from datetime import datetime
import math
from time import sleep

def utc2gps(time_utc):

    leapseconds = 18 #fev 2024
    utc = datetime.strptime(time_utc, "%Y-%m-%dT%H:%M:%S")
    epoch = datetime.strptime("1980-01-07 00:00:00","%Y-%m-%d %H:%M:%S")
    diff = utc-epoch
    gpsWeek = math.floor(diff.days/7)
    secondsThroughDay = (utc.hour * 3600) + (utc.minute * 60) + utc.second
    if utc.isoweekday()== 7:
        weekday = 0
    else:
        weekday = utc.isoweekday()
    gpsSeconds = (weekday * 86400) + secondsThroughDay - leapseconds
    return (gpsWeek,gpsSeconds * 1000)

agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default '()' 0.2 two tenths of a second
mav = mavutil.mavlink_connection('tcp:127.0.0.1:5760')

sleep(5)

while True:  # All data is available via instantiated thread data stream attribute.
    
    ignore_fields = mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_SPEED_ACCURACY
    hdop = agps_thread.data_stream.hdop
    if (hdop == 'n/a'):
        ignore_fields |= mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_HDOP
        hdop = 0
    vdop = agps_thread.data_stream.vdop
    if (vdop == 'n/a'):
        ignore_fields |= mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VDOP
        vdop = 0
    satellites_visible = len(agps_thread.data_stream.satellites)
    id = 0
    time_utc = agps_thread.data_stream.time[:-5]
    now = datetime.strptime(time_utc, "%Y-%m-%dT%H:%M:%S")
    timestamp = round(now.timestamp())
    (gps_week, gps_time) = utc2gps(time_utc)
    mode = agps_thread.data_stream.mode
    lat = round(agps_thread.data_stream.lat * 1E7)
    lon = round(agps_thread.data_stream.lon * 1E7)
    alt = round(agps_thread.data_stream.alt)

    speed = round(agps_thread.data_stream.speed)
    track = round(agps_thread.data_stream.track)
    vn = round(speed * math.sin (track / 360 * 2 * math.pi))
    ve = round(speed * math.cos (track / 360 * 2 * math.pi))
    vd = 0
    speed_accuracy = 0
    vert_accuracy = round(agps_thread.data_stream.epv)
    horiz_accuracy = round(max(agps_thread.data_stream.epx, agps_thread.data_stream.epy))

    gps = {
        "time_usec" : timestamp,
        "gps_id" : id,
        "ignore_flags" : ignore_fields,
        "time_week_ms" : gps_time,
        "time_week" : gps_week,
        "fix_type" : mode,
        "lat" : lat,
        "lon" : lon,
        "alt" : alt,
        "hdop" : hdop,
        "vdop" : vdop,
        "vn" : vn,
        "ve" : ve,
        "vd" : vd,
        "speed_accuracy" : speed_accuracy,
        "horiz_accuracy" : horiz_accuracy,
        "vert_accuracy" : vert_accuracy,
        "satellites_visible" : satellites_visible
    }
    print('---------------------')
    print(gps)
    print('---------------------')
    mav.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GROUND_ROVER,
                           mavutil.mavlink.MAV_AUTOPILOT_GENERIC_WAYPOINTS_ONLY, 
                           mavutil.mavlink.MAV_MODE_FLAG_MANUAL_INPUT_ENABLED, 
                           0, 
                           mavutil.mavlink.MAV_STATE_STANDBY)
    mav.mav.gps_input_send(
        timestamp,  # Timestamp (micros since boot or Unix epoch)
        id,  # ID of the GPS for multiple GPS inputs
        # Flags indicating which fields to ignore (see GPS_INPUT_IGNORE_FLAGS enum).
        # All other fields must be provided.
        ignore_fields,
        gps_time,  # GPS time (milliseconds from start of GPS week)
        gps_week,  # GPS week number
        mode,  # 0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
        lat,  # Latitude (WGS84), in degrees * 1E7
        lon,  # Longitude (WGS84), in degrees * 1E7
        alt,  # Altitude (AMSL, not WGS84), in m (positive for up)
        hdop,  # GPS HDOP horizontal dilution of position in m
        vdop,  # GPS VDOP vertical dilution of position in m
        vn,  # GPS velocity in m/s in NORTH direction in earth-fixed NED frame
        ve,  # GPS velocity in m/s in EAST direction in earth-fixed NED frame
        vd,  # GPS velocity in m/s in DOWN direction in earth-fixed NED frame
        speed_accuracy,  # GPS speed accuracy in m/s
        horiz_accuracy,  # GPS horizontal accuracy in m
        vert_accuracy,  # GPS vertical accuracy in m
        satellites_visible   # Number of satellites visible.
    )
    sleep(1)