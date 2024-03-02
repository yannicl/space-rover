# currently : 18sec

def localtogps(timestring,timeformat,leapseconds,localoffset=0):
    import datetime
    epoch = datetime.datetime.strptime("1980-01-07 00:00:00","%Y-%m-%d %H:%M:%S")
    local = datetime.datetime.strptime(timestring,timeformat)
    utc = local - datetime.timedelta(hours=localoffset)
    diff = utc-epoch
    gpsWeek = diff.days/7
    secondsThroughDay = (utc.hour * 3600) + (utc.minute * 60) + utc.second
    if utc.isoweekday()== 7:
        weekday = 0
    else:
        weekday = utc.isoweekday()
    gpsSeconds = (weekday * 86400) + secondsThroughDay - leapseconds
    return (gpsWeek,gpsSeconds)