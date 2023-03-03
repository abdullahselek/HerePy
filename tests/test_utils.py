#!/usr/bin/env python

import os
import unittest

import herepy
from herepy.utils import Utils


class UtilsTest(unittest.TestCase):
    def test_encodeparameters(self):
        data = None
        encodedParameters = Utils.encode_parameters(data)
        self.assertEqual(encodedParameters, None)
        data = {"searchtext": "200 S Mathilda Sunnyvale CA"}
        encodedParameters = Utils.encode_parameters(data)
        self.assertTrue(encodedParameters)
        data = {"searchtext": "200 S Mathilda Sunnyvale CA", "gen": "8"}
        encodedParameters = Utils.encode_parameters(data)
        self.assertTrue(encodedParameters)

    def test_buildurl(self):
        data = {
            "searchtext": "200 S Mathilda Sunnyvale CA",
            "app_id": "app_id",
            "app_code": "app_code",
        }
        url = Utils.build_url(
            "https://geocoder.cit.api.here.com/6.2/geocode.json", data
        )
        self.assertTrue(url)
