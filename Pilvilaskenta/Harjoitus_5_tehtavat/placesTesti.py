api_key= "AIzaSyDEW_8VnRmXrKyr09s8EfEiJQdSVK1-1Cw"

import googlemaps
import var_dump as vd

gmaps = googlemaps.Client(key=api_key)

# Hakee Google maps:ista koordinaatit, radius on metreinä
result = gmaps.places_nearby(location=(66.503059, 25.726967), radius=500)

#vd.var_dump(result)

for place in result['results']:
    print(place['name'])
