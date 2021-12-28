from one.operations import (
    get_stops,
    get_stops_by_stop_id,
    get_stops_by_source_id,
    get_stops_by_dataset_id,
    get_stops_by_bounding_box,
)
import unittest
from unittest.mock import patch


class GetStopsTestCase(unittest.TestCase):
    def setUp(self):
        self.test_stop = {
            "id": "mdb_stop_45_5017_N_73_5673_W",
            "name": "MDB Stop Example",
            "description": "This is the MDB Stop representing the XYZ shared stop",
            "latitude": 45.508888,
            "longitude": -73.561668,
            "referenced_stops": [
                {
                    "stop_id": "stop_id_from_a_source_dataset",
                    "dataset_id": "Q81",
                    "source_id": "Q80",
                },
                {
                    "stop_id": "stop_id_from_another_source_dataset",
                    "dataset_id": "Q265",
                    "source_id": "Q82",
                },
            ],
        }
        self.test_stops = [self.test_stop]

    @patch("one.operations.helpers")
    def test_get_stops(self, mock_helpers):
        mock_helpers.get_stops.return_value = self.test_stops

        under_test = get_stops()
        self.assertEqual(under_test, self.test_stops)

    @patch("one.operations.helpers")
    def test_get_stops_by_bounding_box(self, mock_helpers):
        mock_helpers.get_stops.return_value = self.test_stops

        test_max_latitude = 46
        test_min_latitude = 45
        test_max_longitude = -73
        test_min_longitude = -74
        under_test = get_stops_by_bounding_box(
            test_max_latitude, test_min_latitude, test_max_longitude, test_min_longitude
        )
        self.assertEqual(under_test, self.test_stops)

    @patch("one.operations.helpers")
    def test_get_no_stops_by_bounding_box(self, mock_helpers):
        mock_helpers.get_stops.return_value = self.test_stops

        test_stops = []
        test_max_latitude = 1
        test_min_latitude = 0
        test_max_longitude = 1
        test_min_longitude = 0
        under_test = get_stops_by_bounding_box(
            test_max_latitude, test_min_latitude, test_max_longitude, test_min_longitude
        )
        self.assertEqual(under_test, test_stops)

    @patch("one.operations.helpers")
    def test_get_stops_by_source_id(self, mock_helpers):
        mock_helpers.get_stops.return_value = self.test_stops

        test_source_id = "Q80"
        under_test = get_stops_by_source_id(test_source_id)
        self.assertEqual(under_test, self.test_stops)

    @patch("one.operations.helpers")
    def test_get_no_stops_by_source_id(self, mock_helpers):
        mock_helpers.get_stops.return_value = self.test_stops

        test_stops = []
        test_source_id = "some_invalid_source_id"
        under_test = get_stops_by_source_id(test_source_id)
        self.assertEqual(under_test, test_stops)

    @patch("one.operations.helpers")
    def test_get_stops_by_dataset_id(self, mock_helpers):
        mock_helpers.get_stops.return_value = self.test_stops

        test_dataset_id = "Q265"
        under_test = get_stops_by_dataset_id(test_dataset_id)
        self.assertEqual(under_test, self.test_stops)

    @patch("one.operations.helpers")
    def test_get_no_stops_by_dataset_id(self, mock_helpers):
        mock_helpers.get_stops.return_value = self.test_stops

        test_stops = []
        test_dataset_id = "some_invalid_dataset_id"
        under_test = get_stops_by_dataset_id(test_dataset_id)
        self.assertEqual(under_test, test_stops)

    @patch("one.operations.helpers")
    def test_get_stops_by_stop_id(self, mock_helpers):
        mock_helpers.get_stops.return_value = self.test_stops

        test_stop_id = "stop_id_from_a_source_dataset"
        under_test = get_stops_by_stop_id(test_stop_id)
        self.assertEqual(under_test, self.test_stops)

    @patch("one.operations.helpers")
    def test_get_no_stops_by_stop_id(self, mock_helpers):
        mock_helpers.get_stops.return_value = self.test_stops

        test_stops = []
        test_stop_id = "some_invalid_stop_id"
        under_test = get_stops_by_stop_id(test_stop_id)
        self.assertEqual(under_test, test_stops)
