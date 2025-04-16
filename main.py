import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound

# Camera access
cap = cv2.VideoCapture(0)

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("voice.mp3")
    playsound("voice.mp3")
    os.remove("voice.mp3")


def listen_and_alert():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            result = r.recognize_google(audio)
            print("You said:", result)

            if "horn" in result.lower() or "traffic" in result.lower():
                playsound("alert.mp3")
                speak("Please wait. Traffic detected ahead.")
            else:
                speak("No traffic detected.")

        except sr.UnknownValueError:
            print("Could not understand the audio.")
            speak("Sorry, I did not understand.")

        except sr.RequestError as e:
            print("Internet error:", e)
            speak("Please check your internet connection.")

        except Exception as e:
            import traceback
            print(" Error occurred:")
            traceback.print_exc()
            speak("An error occurred. Please try again.")

class MainApp(App):
    def build(self):
        self.img = Image()
        layout = BoxLayout(orientation='vertical')
        btn = Button(text='🎙️ Tap to Listen', font_size=24, on_press=lambda x: listen_and_alert())
        layout.add_widget(self.img)
        layout.add_widget(btn)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return layout

    def update(self, dt):
        ret, frame = cap.read()
        if ret:
            # Flip image for selfie view
            buf = cv2.flip(frame, 0).tobytes()
            img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = img_texture

if __name__ == "__main__":
    MainApp().run()






# Load Haar cascades
human_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
car_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_car.xml')

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("detected.mp3")
    playsound("detected.mp3")
    os.remove("detected.mp3")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    humans = human_cascade.detectMultiScale(gray, 1.1, 4)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for (x, y, w, h) in humans:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        speak("Human detected")

    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        speak("Car detected")

    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
