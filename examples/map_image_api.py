#!/usr/bin/env python

from herepy import MapImageApi

map_image_api = MapImageApi(api_key="api_key")

# Returns image with a bounding box
map_image = map_image_api.get_mapimage(
    top_left=[52.8, 11.37309],
    bottom_right=[52.31, 13.2],
    zoom=16,
)
print(map_image)

# Get map image for given coordinates
map_image = map_image_api.get_mapimage(
    coordinates=[28.371425, 77.387695],
    uncertainty="5m",
)
print(map_image)

# Get map image for given coordinates, uncertainty and map scheme
map_image = map_image_api.get_mapimage(
    coordinates=[28.371425, 77.387695], uncertainty="5m", map_scheme=3
)
print(map_image)

# Get a dotless map image for given coordinates and uncertainty
map_image = map_image_api.get_mapimage(
    coordinates=[28.371425, 77.387695], uncertainty="5m", nodot=True
)
print(map_image)

# Get an image showing position with coordinates, city name, image height
map_image = map_image_api.get_mapimage(
    coordinates=[60.17675, 24.929974],
    city_name="Helsinki",
    image_height=400,
    show_position=True,
    zoom=15,
)
print(map_image)

# Get an image showing with coordinates and country name
map_image = map_image_api.get_mapimage(
    coordinates=[60.17675, 24.929974], country_name="Finland", zoom=15
)
print(map_image)

# Get an image showing with coordinates, country name and center
map_image = map_image_api.get_mapimage(
    coordinates=[60.17675, 24.929974],
    country_name="Finland",
    center=[60.17, 24.90],
    zoom=15,
)
print(map_image)

# Get an image showing using encoded geo coordinates
map_image = map_image_api.get_mapimage(encoded_geo_coordinate="QeL4rkKaxoA", zoom=10)
print(map_image)

# Get labeled map image using coordinates
map_image = map_image_api.get_mapimage(
    coordinates=[28.371425, 77.387695],
    label_language="ger",
    second_label_language="tur",
)
print(map_image)
