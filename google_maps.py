import googlemaps
GOOGLE_MAPS_API_KEY = "API KEY HERE"

def get_location_for_address(address:str):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)
    location_data = {
        "longitude": geocode_result.longitude,
        "latitude": geocode_result.latitude
    }
    return location_data