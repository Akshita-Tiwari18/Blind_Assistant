from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myapp")
location = geolocator.geocode("Kanpur,India")

if location:
    print("Latitude:", location.latitude)
    print("Longitude:", location.longitude)
else:
    print("Location not found. Please check the name or try again later.")
