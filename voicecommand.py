import speech_recognition as sr

def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak your destination:")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Call the function and get the voice input
destination_command = get_voice_command()
print("Final destination command:", destination_command)
