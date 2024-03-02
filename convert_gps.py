from gps3 import gps3
from gps_time import GPSTime
from datetime import datetime
import math

data_stream = gps3.DataStream()

sky = "{\"class\":\"SKY\",\"device\":\"/dev/ttyACM0\",\"xdop\":0.56,\"ydop\":0.67,\"vdop\":1.16,\"tdop\":0.70,\"hdop\":0.87,\"gdop\":1.61,\"pdop\":1.45,\"satellites\":[{\"PRN\":5,\"el\":63,\"az\":247,\"ss\":30,\"used\":true},{\"PRN\":6,\"el\":21,\"az\":99,\"ss\":25,\"used\":true},{\"PRN\":7,\"el\":3,\"az\":73,\"ss\":26,\"used\":false},{\"PRN\":9,\"el\":13,\"az\":38,\"ss\":15,\"used\":true},{\"PRN\":11,\"el\":55,\"az\":86,\"ss\":38,\"used\":true},{\"PRN\":12,\"el\":11,\"az\":221,\"ss\":23,\"used\":true},{\"PRN\":13,\"el\":22,\"az\":163,\"ss\":31,\"used\":true},{\"PRN\":15,\"el\":7,\"az\":195,\"ss\":31,\"used\":true},{\"PRN\":20,\"el\":74,\"az\":44,\"ss\":25,\"used\":true},{\"PRN\":25,\"el\":16,\"az\":252,\"ss\":30,\"used\":true},{\"PRN\":26,\"el\":0,\"az\":338,\"ss\":0,\"used\":false},{\"PRN\":29,\"el\":42,\"az\":306,\"ss\":40,\"used\":true}]}\n"
tpv = "{\"class\":\"TPV\",\"device\":\"/dev/ttyACM0\",\"mode\":3,\"time\":\"2024-02-18T02:35:56.000Z\",\"ept\":0.005,\"lat\":45.504686500,\"lon\":-73.692812500,\"alt\":41.500,\"epx\":8.372,\"epy\":10.035,\"epv\":26.680,\"track\":0.0000,\"speed\":0.015,\"climb\":0.000}\n"

data_stream.unpack(sky)

hdop = data_stream.SKY['hdop']
vdop = data_stream.SKY['vdop']
satellites_visible = len(data_stream.SKY['satellites'])

data_stream.unpack(tpv)

now = datetime.strptime("2024-02-18T02:35:57.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
timestamp = now.timestamp()
id = 0
ignore_fields = 32
time_utc = data_stream.TPV['time']
gps_time_obj = GPSTime.from_datetime(now);
gps_time = gps_time_obj.time_of_week * 1000
gps_week = gps_time_obj.week_number
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