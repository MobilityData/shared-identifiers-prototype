from unittest import TestCase
from unittest.mock import patch
import os
from tools.operations import *

BASE_DIR = os.path.dirname(__file__)


class TestStopsOperations(TestCase):
    def setUp(self):
        self.test_stops_csv = f"{BASE_DIR}/resources/test_stops.csv"
        self.test_index = "index"
        self.columns = [ID, NAME, DESCRIPTION, LATITUDE, LONGITUDE, REFERENCED_STOPS]

    @patch("tools.operations.helpers")
    def test_get_stops(self, mock_helpers):
        mock_helpers.load_stops.return_value = pd.read_csv(
            self.test_stops_csv, delimiter=";", index_col=self.test_index
        )
        under_test = get_stops()
        mock_helpers.load_stops.assert_called_once()
        self.assertEqual(under_test.columns.tolist(), self.columns)
        self.assertEqual(len(under_test.index), 2)

    @patch("tools.operations.helpers")
    def test_get_stops_by_bounding_box(self, mock_helpers):
        mock_helpers.load_stops.return_value = pd.read_csv(
            self.test_stops_csv, delimiter=";", index_col=self.test_index
        )

        max_latitude = 35.000000
        min_latitude = 34.000000
        max_longitude = -118.000000
        min_longitude = -119.000000

        under_test = get_stops_by_bounding_box(
            max_latitude, min_latitude, max_longitude, min_longitude
        )
        mock_helpers.load_stops.assert_called_once()
        self.assertEqual(under_test.columns.tolist(), self.columns)
        self.assertEqual(len(under_test.index), 2)

        max_latitude = 34.040000
        min_latitude = 34.000000
        max_longitude = -118.000000
        min_longitude = -119.000000

        under_test = get_stops_by_bounding_box(
            max_latitude, min_latitude, max_longitude, min_longitude
        )
        self.assertEqual(len(under_test.index), 1)

        max_latitude = 34.010000
        min_latitude = 34.000000
        max_longitude = -118.000000
        min_longitude = -119.000000

        under_test = get_stops_by_bounding_box(
            max_latitude, min_latitude, max_longitude, min_longitude
        )
        self.assertEqual(len(under_test.index), 0)

    @patch("tools.operations.helpers")
    def test_get_stops_by_source_id(self, mock_helpers):
        mock_helpers.load_stops.return_value = pd.read_csv(
            self.test_stops_csv, delimiter=";", index_col=self.test_index
        )

        source_id = "source_1"

        under_test = get_stops_by_source_id(source_id)
        mock_helpers.load_stops.assert_called_once()
        self.assertEqual(under_test.columns.tolist(), self.columns)
        self.assertEqual(len(under_test.index), 1)

        source_id = "source_2"

        under_test = get_stops_by_source_id(source_id)
        self.assertEqual(len(under_test.index), 1)

        source_id = "source_3"

        under_test = get_stops_by_source_id(source_id)
        self.assertEqual(len(under_test.index), 0)

    @patch("tools.operations.helpers")
    def test_get_stops_by_dataset_id(self, mock_helpers):
        mock_helpers.load_stops.return_value = pd.read_csv(
            self.test_stops_csv, delimiter=";", index_col=self.test_index
        )

        dataset_id = "dataset_1"

        under_test = get_stops_by_dataset_id(dataset_id)
        mock_helpers.load_stops.assert_called_once()
        self.assertEqual(under_test.columns.tolist(), self.columns)
        self.assertEqual(len(under_test.index), 1)

        dataset_id = "dataset_2"

        under_test = get_stops_by_dataset_id(dataset_id)
        self.assertEqual(len(under_test.index), 1)

        dataset_id = "dataset_3"

        under_test = get_stops_by_dataset_id(dataset_id)
        self.assertEqual(len(under_test.index), 0)

    @patch("tools.operations.helpers")
    def test_get_stops_by_stop_id(self, mock_helpers):
        mock_helpers.load_stops.return_value = pd.read_csv(
            self.test_stops_csv, delimiter=";", index_col=self.test_index
        )

        stop_id = "stop_1"

        under_test = get_stops_by_stop_id(stop_id)
        mock_helpers.load_stops.assert_called_once()
        self.assertEqual(under_test.columns.tolist(), self.columns)
        self.assertEqual(len(under_test.index), 1)

        stop_id = "stop_2"

        under_test = get_stops_by_stop_id(stop_id)
        self.assertEqual(len(under_test.index), 1)

        stop_id = "stop_3"

        under_test = get_stops_by_stop_id(stop_id)
        self.assertEqual(len(under_test.index), 0)

    @patch("tools.operations.helpers")
    def test_add_stop_operation(self, mock_helpers):
        mock_helpers.load_stops.return_value = pd.read_csv(
            self.test_stops_csv, delimiter=";", index_col=self.test_index
        )

        test_new_stop_index = 2
        test_name = "test_name"
        test_description = "test_description"
        test_latitude = 34.000000
        test_longitude = -118.000000
        test_ref_stop_id = "test_stop_id"
        test_ref_dataset_id = "test_dataset_id"
        test_ref_source_id = "test_source_id"

        under_test = add_stop(
            name=test_name,
            description=test_description,
            latitude=test_latitude,
            longitude=test_longitude,
            ref_stop_id=test_ref_stop_id,
            ref_dataset_id=test_ref_dataset_id,
            ref_source_id=test_ref_source_id,
        )
        self.assertEqual(len(under_test.index), 3)
        self.assertEqual(under_test.at[test_new_stop_index, NAME], test_name)
        self.assertEqual(
            under_test.at[test_new_stop_index, DESCRIPTION], test_description
        )
        self.assertEqual(under_test.at[test_new_stop_index, LATITUDE], test_latitude)
        self.assertEqual(under_test.at[test_new_stop_index, LONGITUDE], test_longitude)
        self.assertEqual(
            under_test.at[test_new_stop_index, REFERENCED_STOPS],
            [
                {
                    STOP_ID: test_ref_stop_id,
                    DATASET_ID: test_ref_dataset_id,
                    SOURCE_ID: test_ref_source_id,
                }
            ],
        )
        mock_helpers.save_stops.assert_called_with(under_test)
