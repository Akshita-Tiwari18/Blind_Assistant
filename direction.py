import openrouteservice
from openrouteservice import convert
from geopy.geocoders import Nominatim

# Get coordinates
geolocator = Nominatim(user_agent="blind_assistant")
start = geolocator.geocode("Kanpur Central")  # Replace with current location
end = geolocator.geocode("Gopal Nagar")

client = openrouteservice.Client(key='YOUR_API_KEY')  # replace with your ORS API key

coords = ((start.longitude, start.latitude), (end.longitude, end.latitude))

route = client.directions(coords)
steps = route['routes'][0]['segments'][0]['steps']

for step in steps:
    instruction = step['instruction']
    print(instruction)
