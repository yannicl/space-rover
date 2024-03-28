from pymavlink import mavutil
from pynput import keyboard
from threading import Thread
from CameraReceiver import CameraReceiver

FORWARD = 100
REVERSE = -100
STOP = 0

class GroundBaseStation:
    def __init__(self) -> None:
        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

        self.mav = mavutil.mavlink_connection('tcp:127.0.0.1:5760')
        self.cr = CameraReceiver()
        t1 = Thread(target=self.cr.listen)
        t1.start()
        

    def sendCommands(self, motorA, motorB):
        self.mav.mav.rc_channels_scaled_send(
            time_boot_ms=0,
            port=0,  
            chan1_scaled=motorA, 
            chan2_scaled=motorB, 
            chan3_scaled=0,
            chan4_scaled=0,
            chan5_scaled=0,
            chan6_scaled=0,
            chan7_scaled=0,
            chan8_scaled=0,
            rssi=0)

    def listen(self):
        while True:
            msg = self.mav.recv_match(blocking=True)
            if (msg) :
                print(msg)
    
    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
            if key.char == 'd' :
                motorA = FORWARD
                motorB = REVERSE
                self.sendCommands(motorA, motorB)
            if key.char == 'a' :
                motorA = REVERSE
                motorB = FORWARD
                self.sendCommands(motorA, motorB)
            if key.char == 'w' :
                motorA = FORWARD
                motorB = FORWARD
                self.sendCommands(motorA, motorB)
            if key.char == 's' :
                motorA = REVERSE
                motorB = REVERSE
                self.sendCommands(motorA, motorB)
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(self, key):
        print('{0} released'.format(
            key))
        motorA = STOP
        motorB = STOP
        self.sendCommands(motorA, motorB)
        if key == keyboard.Key.esc:
            # Stop listener
            return False




if __name__ == '__main__':
    gbs = GroundBaseStation()
    gbs.listen()