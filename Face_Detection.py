import cv2
import serial

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Open serial port REMINDER that ports differ between Mac, PC, and Linux
ser = serial.Serial('/dev/ttyUSB0', 115200)
#Append newline characters and send serial data
def sendData(data):
    data += "\r\n"
    ser.write(data.encode())


# To capture video from webcam. 
cap = cv2.VideoCapture(0)
# To use a video file as input 
# cap = cv2.VideoCapture('filename.mp4')
while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around each face
    #also find the biggest rectangle because thats probably the person
    biggest = 0
    bigcenter = 0
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        if((w * h) > biggest):
            biggest = w * h
            bigcenter = x + (w/2)

    #If the person is too far off center send packet to turn monitor
    center = cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2
    if(biggest > 30000):
        if((bigcenter - center) < -200):
            sendData("R")
            # print(str(bigcenter) + ' ' + str(center) )
            # print("TURNRIGHT")
        if((bigcenter - center) > 200):
            sendData("L")
            # print(str(bigcenter) + ' ' + str(center) )
            # print("TURNLEFT")    

    # Display
    cv2.imshow('img', cv2.flip(img, 1))
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
# Release the VideoCapture object
cap.release()
# Close the serial port
ser.close()