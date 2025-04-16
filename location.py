import folium

# Coordinates: (latitude, longitude)
location = [26.4499, 80.3319]  # Kanpur

map_obj = folium.Map(location=location, zoom_start=15)
folium.Marker(location, tooltip="You are here").add_to(map_obj)


map_obj.save("map.html")
