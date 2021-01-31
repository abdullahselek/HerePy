#!/usr/bin/env python

from herepy import (
    MapTileApi,
    MapTileApiType,
    BaseMapTileResourceType,
    TrafficMapTileResourceType,
)

map_tile_api = MapTileApi(api_key="api_key")

# Returns a map tile
map_tile = map_tile_api.get_maptile(latitude=52.525439, longitude=13.38727, zoom=12)
print(map_tile)

# Returns map tile of traffic Map Tile API
map_tile = map_tile_api.get_maptile(
    latitude=52.525439,
    longitude=13.38727,
    zoom=12,
    api_type=MapTileApiType.traffic,
    resource_type=TrafficMapTileResourceType.flowlabeltile,
)
print(map_tile)

# Returns a map tile of Aerial API using different parameters
map_tile = map_tile_api.get_maptile(
    latitude=52.525439,
    longitude=13.38727,
    zoom=12,
    api_type=MapTileApiType.aerial,
    scheme="terrain.day",
    size=256,
    tile_format="png",
)
print(map_tile)

# ppi specifies 320 ppi which corresponds with Hi-Res.
map_tile = map_tile_api.get_maptile(
    latitude=52.525439,
    longitude=13.38727,
    zoom=12,
    api_type=MapTileApiType.base,
    resource_type=BaseMapTileResourceType.basetile,
    scheme="normal.day",
    size=256,
    tile_format="png8",
    query_parameters={"ppi": 320},
)
print(map_tile)
