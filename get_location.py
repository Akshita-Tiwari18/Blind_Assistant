# voice_navigation_assistant.py

import speech_recognition as sr
from geopy.geocoders import Nominatim
import openrouteservice
import pyttsx3

# Initialize Services
recognizer = sr.Recognizer()
geolocator = Nominatim(user_agent="blind_assistant_app")
tts_engine = pyttsx3.init()
ors_client = openrouteservice.Client(key='YOUR_OPENROUTESERVICE_API_KEY')  # 🔑 Replace with your actual key

# 1️Voice Input to Get Destination
def get_destination_by_voice():
    with sr.Microphone() as source:
        print(" Please speak your destination:")
        tts_engine.say("Please speak your destination")
        tts_engine.runAndWait()
        audio = recognizer.listen(source)

    try:
        destination = recognizer.recognize_google(audio)
        print(f" You said: {destination}")
        return destination
    except sr.UnknownValueError:
        print(" Could not understand audio.")
        tts_engine.say("Sorry, I didn't understand.")
        tts_engine.runAndWait()
        return None
    except sr.RequestError as e:
        print(f" API error: {e}")
        return None

# 2️⃣ Convert Place Name to Coordinates
def get_coordinates(place_name):
    try:
        location = geolocator.geocode(place_name + ", Delhi")  # You can change city
        if location:
            return (location.longitude, location.latitude)  # openrouteservice uses (lon, lat)
        else:
            return None
    except Exception as e:
        print(f" Geocoding failed: {e}")
        return None

# 3️⃣ Get Route and Speak Directions
def speak_route_directions(source_coords, destination_coords):
    try:
        route = ors_client.directions(
            coordinates=[source_coords, destination_coords],
            profile='foot-walking',
            format='geojson'
        )
        steps = route['features'][0]['properties']['segments'][0]['steps']
        
        print("\n Starting Directions:\n")
        for step in steps:
            instruction = step['instruction']
            print("➡️", instruction)
            tts_engine.say(instruction)
            tts_engine.runAndWait()
    except Exception as e:
        print(f"Error getting directions: {e}")
        tts_engine.say("Unable to get directions")
        tts_engine.runAndWait()

# 4️⃣ Main Flow
def main():
    destination = get_destination_by_voice()
    if not destination:
        return

    destination_coords = get_coordinates(destination)
    if not destination_coords:
        print("Destination not found.")
        tts_engine.say("Destination not found. Try again.")
        tts_engine.runAndWait()
        return

    # Use fixed current location for now (India Gate)
    source_coords = (77.2295, 28.6129)  # (longitude, latitude)

    print(f"\n Routing from India Gate to {destination}...")
    speak_route_directions(source_coords, destination_coords)

# Run the app
if __name__ == "__main__":
    main()
