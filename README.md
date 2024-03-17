mavlink-routerd -e 127.0.0.1:14550 /dev/ttyACM0


picocom /dev/ttyACM0 --baud 115200 --omap crcrlf --echo


picocom /dev/ttyACM1 --baud 115200 --omap crcrlf --echo


mavlink-routerd /dev/ttyACM1


##
# PICO Pinout

