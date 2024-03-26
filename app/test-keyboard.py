from pynput import keyboard
import serial
import time
import ujson

ser = serial.Serial('/dev/ttyACM0', 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)

FORWARD = 100
REVERSE = -100
STOP = 0

def sendCommands(motorA, motorB):
    global ser
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

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        if key.char == 'd' :
            motorA = FORWARD
            motorB = REVERSE
            sendCommands(motorA, motorB)
        if key.char == 'a' :
            motorA = REVERSE
            motorB = FORWARD
            sendCommands(motorA, motorB)
        if key.char == 'w' :
            motorA = FORWARD
            motorB = FORWARD
            sendCommands(motorA, motorB)
        if key.char == 's' :
            motorA = REVERSE
            motorB = REVERSE
            sendCommands(motorA, motorB)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    motorA = STOP
    motorB = STOP
    sendCommands(motorA, motorB)
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

sendCommands(STOP, STOP)

while True:
    line = ser.readline()
    print(line)
    time.sleep(0.1)