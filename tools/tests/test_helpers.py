from unittest import TestCase
from unittest.mock import patch
import os
from tools.helpers import load_stops, save_stops

BASE_DIR = os.path.dirname(__file__)


class TestStopHelpers(TestCase):
    @patch("tools.helpers.pd")
    @patch("tools.helpers.STOPS_CSV", f"{BASE_DIR}/resources/test_stops.csv")
    def test_load_stops(self, mock_pd):
        mock_pd.read_csv.return_value = "test_stops"
        under_test = load_stops()
        self.assertEqual(under_test, "test_stops")
        mock_pd.read_csv.assert_called_once()

    @patch("tools.helpers.pd")
    @patch("tools.helpers.STOPS_CSV", f"{BASE_DIR}/resources/test_stops.csv")
    def test_save_stops(self, mock_pd):
        mock_stops = mock_pd.DataFrame()
        under_test = save_stops(mock_stops)
        self.assertEqual(under_test, mock_stops)
        mock_stops.to_csv.assert_called_once()
