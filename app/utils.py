from geopy.distance import geodesic

landmarks = {
    "Delhi": {
        "metro": [
            (28.6139, 77.2090),
            (28.5562, 77.1000),
            (28.7041, 77.1025)
        ],
        "hospital": [
            (28.5672, 77.2100),
            (28.5355, 77.3910),
            (28.6692, 77.4538)
        ]
    },
    "Mumbai": {
        "metro": [
            (19.0760, 72.8777),
            (19.0330, 72.8420)
        ],
        "hospital": [
            (19.0596, 72.8295),
            (19.2183, 72.9781)
        ]
    },
    "Bangalore": {
        "metro": [
            (12.9716, 77.5946),
            (12.9352, 77.6245)
        ],
        "hospital": [
            (12.9279, 77.6271),
            (13.0350, 77.5970)
        ]
    }
}


def calculate_accessibility(city, lat, lon):

    if city not in landmarks:
        return 0.5

    min_distances = []

    for category in landmarks[city].values():
        dists = [
            geodesic((lat, lon), coord).km
            for coord in category
        ]
        min_distances.append(min(dists))

    avg_dist = sum(min_distances) / len(min_distances)

    score = 1 / (1 + avg_dist)

    return round(score, 3)