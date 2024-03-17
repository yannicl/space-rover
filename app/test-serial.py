import serial
import time
import ujson

ser = serial.Serial('/dev/ttyACM0', 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)
while True:
    line = ser.readline()
    print(line)
    msg = {
        "type":"RC_CHANNELS_SCALED",
        "chan1_scaled":-15,
        "chan2_scaled":-15
    }
    #
    cmd = "handleLineFromRPi(\"" + ujson.dumps(msg).replace('"','\\\"') + "\")"
    print(cmd)
    ser.write(cmd.encode("utf-8"))
    ser.write( b'\x04' )
    line = ser.readline()
    print(line)
    line = ser.readline()
    print(line)
    time.sleep(0.5)