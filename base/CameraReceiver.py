import io
import socket
import struct
from PIL import Image
import cv2
import numpy

class CameraReceiver:

    def __init__(self) -> None:
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8000))
        self.server_socket.listen(0)

    def listen(self):
        # Accept a single connection and make a file-like object out of it
        connection = self.server_socket.accept()[0].makefile('rb')
        try:
            while True:
                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                image_stream.seek(0)
                image = Image.open(image_stream)
                #print('Image is %dx%d' % image.size)
                #image.verify()
                #print('Image is verified')
                #image.show('picamera')
                numpy_array = numpy.array(image)
                #print(numpy_array.shape)
                frame = cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)
                cv2.imshow('picamera', frame)
                cv2.waitKey(1)

        finally:
            connection.close()
            self.server_socket.close()