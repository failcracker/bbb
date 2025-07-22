from math import sqrt

def is_within_radius(lat1, lon1, lat2, lon2, radius_meter=100):
    # Euclidean distance (not geodesic, cukup untuk radius kecil)
    dx = (lat1 - lat2) * 111320  # approx meter per degree latitude
    dy = (lon1 - lon2) * 111320  # approx meter per degree longitude (at equator)
    distance = sqrt(dx ** 2 + dy ** 2)
    return distance <= radius_meter, distance
