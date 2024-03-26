from pynput import keyboard
import serial
import time
import ujson

ser = serial.Serial('/dev/ttyACM0', 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)

FORWARD = 100
REVERSE = -100
STOP = 0

motorA = STOP
motorB = STOP

def on_press(key):
    global motorA, motorB
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        if key.char == 'a' :
            motorA = FORWARD
            motorB = REVERSE
        if key.char == 'd' :
            motorA = REVERSE
            motorB = FORWARD
        if key.char == 'w' :
            motorA = FORWARD
            motorB = FORWARD
        if key.char == 's' :
            motorA = REVERSE
            motorB = REVERSE
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    global motorA, motorB
    print('{0} released'.format(
        key))
    motorA = STOP
    motorB = STOP
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    line = ser.readline()
    print(line)
    msg = {
        "type":"RC_CHANNELS_SCALED",
        "chan1_scaled":motorA,
        "chan2_scaled":motorB
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