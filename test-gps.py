# See https://gpsd.gitlab.io/gpsd/gpsd_json.html

POLL.time

TPV.mode # 0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
TPV.altMSL # Altitude (AMSL, not WGS84), in m (positive for up)
TPV.lat # Latitude (WGS84), in degrees * 1E7
TPV.lon # Longitude (WGS84), in degrees * 1E7

TPV.velN # GPS velocity in m/s in NORTH direction in earth-fixed NED frame
TPV.velE # GPS velocity in m/s in EAST direction in earth-fixed NED frame
TPV.velD # GPS velocity in m/s in DOWN direction in earth-fixed NED frame

SKY.hdop # GPS HDOP horizontal dilution of position in m
SKY.pdop # GPS VDOP vertical dilution of position in m
SKY.satellites.length # Number of satellites visible.

# GPS_INPUT_IGNORE_FLAGS
# [Enum]

# Value	Field Name	Description
# 1	GPS_INPUT_IGNORE_FLAG_ALT	ignore altitude field
# 2	GPS_INPUT_IGNORE_FLAG_HDOP	ignore hdop field
# 4	GPS_INPUT_IGNORE_FLAG_VDOP	ignore vdop field
# 8	GPS_INPUT_IGNORE_FLAG_VEL_HORIZ	ignore horizontal velocity field (vn and ve)
# 16	GPS_INPUT_IGNORE_FLAG_VEL_VERT	ignore vertical velocity field (vd)
# 32	GPS_INPUT_IGNORE_FLAG_SPEED_ACCURACY	ignore speed accuracy field
# 64	GPS_INPUT_IGNORE_FLAG_HORIZONTAL_ACCURACY	ignore horizontal accuracy field
# 128	GPS_INPUT_IGNORE_FLAG_VERTICAL_ACCURACY	ignore vertical accuracy field




# GPS_TYPE need to be MAV
while True:
    time.sleep(0.2)
    master.mav.gps_input_send(
        0,  # Timestamp (micros since boot or Unix epoch)
        0,  # ID of the GPS for multiple GPS inputs
        # Flags indicating which fields to ignore (see GPS_INPUT_IGNORE_FLAGS enum).
        # All other fields must be provided.
        8 | 16 | 32,
        0,  # GPS time (milliseconds from start of GPS week)
        0,  # GPS week number
        3,  # 0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
        0,  # Latitude (WGS84), in degrees * 1E7
        0,  # Longitude (WGS84), in degrees * 1E7
        0,  # Altitude (AMSL, not WGS84), in m (positive for up)
        1,  # GPS HDOP horizontal dilution of position in m
        1,  # GPS VDOP vertical dilution of position in m
        0,  # GPS velocity in m/s in NORTH direction in earth-fixed NED frame
        0,  # GPS velocity in m/s in EAST direction in earth-fixed NED frame
        0,  # GPS velocity in m/s in DOWN direction in earth-fixed NED frame
        0,  # GPS speed accuracy in m/s
        0,  # GPS horizontal accuracy in m
        0,  # GPS vertical accuracy in m
        7   # Number of satellites visible.
    )

#  self.master.mav.gps_input_send(
#                 self.data['time_usec'],
#                 self.data['gps_id'],
#                 self.data['ignore_flags'],
#                 self.data['time_week_ms'],
#                 self.data['time_week'],
#                 self.data['fix_type'],
#                 self.data['lat'],
#                 self.data['lon'],
#                 self.data['alt'],
#                 self.data['hdop'],
#                 self.data['vdop'],
#                 self.data['vn'],
#                 self.data['ve'],
#                 self.data['vd'],
#                 self.data['speed_accuracy'],
#                 self.data['horiz_accuracy'],
#                 self.data['vert_accuracy'],
#                 self.data['satellites_visible'])

{"class":"SKY","device":"/dev/ttyACM0","xdop":0.56,"ydop":0.67,"vdop":1.17,"tdop":0.71,"hdop":0.87,"gdop":1.63,"pdop":1.46,"satellites":[{"PRN":5,"el":62,"az":246,"ss":23,"used":true},{"PRN":6,"el":22,"az":98,"ss":25,"used":true},{"PRN":7,"el":3,"az":74,"ss":25,"used":false},{"PRN":9,"el":14,"az":38,"ss":19,"used":true},{"PRN":11,"el":56,"az":85,"ss":39,"used":true},{"PRN":12,"el":12,"az":221,"ss":18,"used":true},{"PRN":13,"el":21,"az":164,"ss":23,"used":true},{"PRN":15,"el":6,"az":195,"ss":29,"used":true},{"PRN":20,"el":75,"az":43,"ss":29,"used":true},{"PRN":25,"el":17,"az":253,"ss":24,"used":true},{"PRN":26,"el":0,"az":339,"ss":0,"used":false},{"PRN":29,"el":41,"az":307,"ss":39,"used":true}]}
{
   "class":"TPV",
   "device":"/dev/ttyACM0",
   "mode":3,
   "time":"2024-02-18T02:35:57.000Z",
   "ept":0.005,
   "lat":45.504687350,
   "lon":-73.692812833,
   "alt":41.411,
   "epx":8.372,
   "epy":10.035,
   "epv":26.680,
   "track":336.3045,
   "speed":0.027,
   "climb":-0.024,
   "eps":0.46,
   "epc":53.36
}


track & speed =>

# GPS velocity in m/s in NORTH direction in earth-fixed NED frame


# GPS velocity in m/s in EAST direction in earth-fixed NED frame


# speed_accuracy
eps

# vert_accuracy
epv

# horiz_accuracy
max(epx, epy)

# GPS velocity in m/s in DOWN direction in earth-fixed NED frame
 = 0
epc = 0


now = datetime.strptime("2024-02-18T02:35:57.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
timestamp = now.totimestamp()
id = 0
ignore_fields = 0
time_utc = data_stream.TPV['time']
gps_time_obj = GPSTime.from_datetime(now);
gps_time = gps_time_obj.time_of_week * 1000
gps_week = gps_time_obj.week_number
mode = data_stream.TPV['mode']
lat = data_stream.TPV['lat'] * 1E7
lon = data_stream.TPV['lon'] * 1E7
alt = data_stream.TPV['alt']
hdop = data_stream.SKY['hdop']
vdop = data_stream.SKY['vdop']
speed = data_stream.TPV['speed']
track = data_stream.TPV['track']
vn = speed * sin (track / 360 * 2 * pi)
ve = speed * cos (track / 360 * 2 * pi)
vd = 0
speed_accuracy = data_stream.TPV['eps']
vert_accuracy = data_stream.TPV['epv']
horiz_accuracy = max(data_stream.TPV['epx'], data_stream.TPV['epy'])
satellites_visible = SKY.satellites.length 




master.mav.gps_input_send(
        0,  # Timestamp (micros since boot or Unix epoch)
        0,  # ID of the GPS for multiple GPS inputs
        # Flags indicating which fields to ignore (see GPS_INPUT_IGNORE_FLAGS enum).
        # All other fields must be provided.
        8 | 16 | 32,
        0,  # GPS time (milliseconds from start of GPS week)
        0,  # GPS week number
        3,  # 0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
        0,  # Latitude (WGS84), in degrees * 1E7
        0,  # Longitude (WGS84), in degrees * 1E7
        0,  # Altitude (AMSL, not WGS84), in m (positive for up)
        1,  # GPS HDOP horizontal dilution of position in m
        1,  # GPS VDOP vertical dilution of position in m
        0,  # GPS velocity in m/s in NORTH direction in earth-fixed NED frame
        0,  # GPS velocity in m/s in EAST direction in earth-fixed NED frame
        0,  # GPS velocity in m/s in DOWN direction in earth-fixed NED frame
        0,  # GPS speed accuracy in m/s
        0,  # GPS horizontal accuracy in m
        0,  # GPS vertical accuracy in m
        7   # Number of satellites visible.
    )