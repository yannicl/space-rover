https://ardupilot.org/copter/docs/parameters.html


Virtual serial port

socat -d -d pty,raw,echo=0 pty,raw,echo=0


socat -d -d pty,rawer,echo=0,link=/dev/pts/7 pty,rawer,echo=0,link=/dev/pts/8