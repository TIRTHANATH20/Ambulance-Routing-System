from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Function to geocode address using LocationIQ API
def geocode(address):
    url = "https://us1.locationiq.com/v1/search.php"
    params = {
        'key': 'pk.9681dcd568ec89f0aaf254f5e26bffb2',  # Replace with your LocationIQ API key
        'q': address,
        'format': 'json'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            return None
    except Exception as e:
        print(f"Geocoding Error: {e}")
        return None

# Function to query hospitals using Overpass API
def query_hospitals(lat, lon, radius=5000):
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      way["amenity"="hospital"](around:{radius},{lat},{lon});
      relation["amenity"="hospital"](around:{radius},{lat},{lon});
    );
    out center;
    """
    try:
        response = requests.post(overpass_url, data=query)
        data = response.json()
        hospitals = []
        for element in data['elements']:
            if 'tags' in element and ('name' in element['tags']):
                name = element['tags']['name']
                if 'lat' in element and 'lon' in element:
                    hosp_lat = element['lat']
                    hosp_lon = element['lon']
                else:
                    hosp_lat = element['center']['lat']
                    hosp_lon = element['center']['lon']
                hospitals.append((name, hosp_lat, hosp_lon))
        return hospitals
    except Exception as e:
        print(f"Overpass API Error: {e}")
        return []

# Function to get route information and distance using OSRM API
def get_route_info(start, end):
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson&steps=true"
        response = requests.get(url)
        data = response.json()
        if data['code'] == 'Ok':
            route = data['routes'][0]
            distance = route['legs'][0]['distance'] / 1000  # Convert meters to kilometers
            duration = route['legs'][0]['duration'] / 60  # Convert seconds to minutes
            geometry = route['geometry']['coordinates']
            return distance, duration, geometry
        else:
            return None
    except Exception as e:
        print(f"Routing Error: {e}")
        return None

# Home route to render the map
@app.route('/')
def index():
    return render_template('index.html')

# API route to get nearest hospital and route with distance and time
@app.route('/find_hospital', methods=['POST'])
def find_hospital():
    src_address = request.form['src_address']
    src_coords = geocode(src_address)
    
    if not src_coords:
        return jsonify({'error': 'Invalid Address'})
    
    hospitals = query_hospitals(src_coords[0], src_coords[1])
    
    if not hospitals:
        return jsonify({'error': 'No nearby hospitals found'})
    
    # Find nearest hospital
    nearest_hospital = min(hospitals, key=lambda x: (x[1] - src_coords[0])**2 + (x[2] - src_coords[1])**2)
    
    # Get route geometry, distance, and duration to the nearest hospital
    distance, duration, route_geometry = get_route_info(src_coords, (nearest_hospital[1], nearest_hospital[2]))
    
    if not route_geometry:
        return jsonify({'error': 'Unable to get route information'})

    return jsonify({
        'src_coords': src_coords,
        'nearest_hospital': {
            'name': nearest_hospital[0],
            'lat': nearest_hospital[1],
            'lon': nearest_hospital[2]
        },
        'distance': distance,
        'duration': duration,
        'route_geometry': route_geometry
    })

if __name__ == "__main__":
    app.run(debug=True)
