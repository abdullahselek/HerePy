import unittest

from herepy.platform import TourPlanningApi


class TourPlanningApiTest(unittest.TestCase):
    def setUp(self):
        api = TourPlanningApi("api_key")
        self._api = api

    def test_initiation(self):
        self.assertIsInstance(self._api, TourPlanningApi)
        self.assertEqual(self._api._api_key, "api_key")
        self.assertEqual(
            self._api._base_url,
            "https://tourplanning.hereapi.com/v3/",
        )
