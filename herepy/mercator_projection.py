#!/usr/bin/env python

import math


class MercatorProjection(object):
    """The Map and Vetor Tile API serves map tiles obtained by mapping points on the
    surface of a sphere (the globe) to points on a plane, using the normalized Mercator projection.

    This class helps to create column and row values to be used in requests.
    """

    @staticmethod
    def get_column_row(latitude: float, longitude: float, zoom: int):
        lat_rad = latitude * math.pi / 180
        n = math.pow(2, zoom)
        x_tile = n * ((longitude + 180) / 360)
        y_tile = (
            n
            * (1 - (math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi))
            / 2
        )
        return int(x_tile), int(y_tile)
