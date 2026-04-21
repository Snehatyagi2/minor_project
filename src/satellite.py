import random

def generate_satellite_grid(center_lat, center_lon, n_points=20):
    points = []

    # create a bounding box roughly ~25km around the center
    # 1 degree of latitude is ~111km, so 0.25 degrees is ~27km
    lat_min = center_lat - 0.25
    lat_max = center_lat + 0.25
    lon_min = center_lon - 0.25
    lon_max = center_lon + 0.25

    for _ in range(n_points):
        lat = random.uniform(lat_min, lat_max)
        lon = random.uniform(lon_min, lon_max)

        # simulate satellite NO2
        no2 = random.uniform(20, 120)

        points.append({
            "lat": lat,
            "lon": lon,
            "no2": no2
        })

    return points