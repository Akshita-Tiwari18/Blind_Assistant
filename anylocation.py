from geopy.geocoders import Nominatim
import speech_recognition as sr

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your destination...")
        audio = r.listen(source)

    try:
        result = r.recognize_google(audio)
        return result
    except:
        return None

# Geocoder initialize
geolocator = Nominatim(user_agent="blind_assistant_app")

destination = get_voice_input()

if destination:
    print("You said:", destination)
    location = geolocator.geocode(destination)

    if location:
        print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
    else:
        print(" Location not found. Try a more specific place name.")
else:
    print("Could not understand your voice.")
