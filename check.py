''''import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame not received from camera")
        break

    cv2.imshow("Test Camera Feed", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()'''

import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print(" Say something...")
    audio = r.listen(source)
    print(" Got it! Recognizing...")

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except Exception as e:
    print("Error:", e)

