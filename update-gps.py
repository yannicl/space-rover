from gps3 import gps3
from datetime import datetime
import math
import json

def utc2gps(time_utc):

    leapseconds = 18 #fev 2024
    utc = datetime.strptime(time_utc, "%Y-%m-%dT%H:%M:%S.000Z")
    epoch = datetime.datetime.strptime("1980-01-07 00:00:00","%Y-%m-%d %H:%M:%S")
    diff = utc-epoch
    gpsWeek = diff.days/7
    secondsThroughDay = (utc.hour * 3600) + (utc.minute * 60) + utc.second
    if utc.isoweekday()== 7:
        weekday = 0
    else:
        weekday = utc.isoweekday()
    gpsSeconds = (weekday * 86400) + secondsThroughDay - leapseconds
    return (gpsWeek,gpsSeconds * 1000)

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            print(json.dumps(new_data))
            hdop = data_stream.SKY['hdop']
            vdop = data_stream.SKY['vdop']
            satellites_visible = len(data_stream.SKY['satellites'])
            id = 0
            ignore_fields = 32
            time_utc = data_stream.TPV['time']
            now = datetime.strptime(time_utc, "%Y-%m-%dT%H:%M:%S.000Z")
            timestamp = now.timestamp()
            (gps_week, gps_time) = utc2gps(time_utc)
            mode = data_stream.TPV['mode']
            lat = data_stream.TPV['lat'] * 1E7
            lon = data_stream.TPV['lon'] * 1E7
            alt = data_stream.TPV['alt']

            speed = data_stream.TPV['speed']
            track = data_stream.TPV['track']
            vn = speed * math.sin (track / 360 * 2 * math.pi)
            ve = speed * math.cos (track / 360 * 2 * math.pi)
            vd = 0
            speed_accuracy = 0
            vert_accuracy = data_stream.TPV['epv']
            horiz_accuracy = max(data_stream.TPV['epx'], data_stream.TPV['epy'])

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

            print(gps)