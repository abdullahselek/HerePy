#!/usr/bin/env python

from herepy import VectorTileApi, VectorMapTileLayer

vector_tile_api = VectorTileApi(api_key="api_key")

# Returns a tile using base layer and other default parameters
vector_tile = vector_tile_api.get_vectortile(
    latitude=52.525439, longitude=13.38727, zoom=12
)
print(vector_tile)

# Returns tile using core layer with other default parameters
vector_tile = vector_tile_api.get_vectortile(
    latitude=52.525439, longitude=13.38727, zoom=12, layer=VectorMapTileLayer.core
)
print(vector_tile)
