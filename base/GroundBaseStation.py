from pymavlink import mavutil
import csv

class GroundBaseStation:
    def __init__(self) -> None:
        self.mav = mavutil.mavlink_connection('tcp:127.0.0.1:5760')
        pass

    def listen(self):
        with open('imu.csv', 'w', newline='') as csvfile:
            fieldnames = ['time_usec', 'xacc', 'yacc']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            while True:
                msg = self.mav.recv_match(blocking=True)
                if (msg) :
                    print(msg)
                    writer.writerow(msg.to_dict())


if __name__ == '__main__':
    gbs = GroundBaseStation()
    gbs.listen()