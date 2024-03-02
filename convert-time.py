from gps_time import GPSTime
from datetime import datetime
gps_time = GPSTime.from_datetime(datetime.strptime("2024-02-18T02:35:57.000Z", "%Y-%m-%dT%H:%M:%S.000Z"));
print(f"GPS Time: {gps_time}")
gps_time.week_number