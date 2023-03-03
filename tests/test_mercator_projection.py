#!/usr/bin/env python

import unittest

from herepy import MercatorProjection


class MercatorProjectionTest(unittest.TestCase):
    def test_get_column_row(self):
        column, row = MercatorProjection.get_column_row(
            latitude=52.525439, longitude=13.38727, zoom=12
        )
        self.assertEqual(column, 2200)
        self.assertEqual(row, 1343)
