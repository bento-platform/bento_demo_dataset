# see here for guidelines on coordinate precision: https://xkcd.com/2170/

BIOSAMPLE_LOCATIONS = [
    {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [-73.6034936, 45.4732202]},
        "properties": {"label": "MUHC"},
    },
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [-73.5674, 45.5019],
        },
        "properties": {
            "label": "Montreal",
            "city": "Montreal",
            "country": "Canada",
            "ISO3166alpha3": "CAN",
            "precision": "city",
            "location_extra_property": 4321,
        },
    },
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [-73.6251, 45.5031],
        },
        "properties": {
            "label": "CHU Sainte-Justine",
            "city": "Montreal",
            "country": "Canada",
            "ISO3166alpha3": "CAN",
        },
    },
]
