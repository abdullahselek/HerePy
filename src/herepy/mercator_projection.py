#!/usr/bin/env python
"""Utilities for converting geographic coordinates to map tile indices."""

import math


class MercatorProjection:
    """
    Convert geographic positions to map tile coordinates.

    The Map and Vector Tile APIs use the normalized Mercator projection to map positions on the
    globe to a plane.

    """

    @staticmethod
    def get_column_row(latitude: float, longitude: float, zoom: int):
        """Return the tile column and row for the given coordinates and zoom."""
        lat_rad = latitude * math.pi / 180
        n = math.pow(2, zoom)
        x_tile = n * ((longitude + 180) / 360)
        y_tile = n * (1 - (math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi)) / 2
        return int(x_tile), int(y_tile)
