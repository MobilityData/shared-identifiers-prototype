from helpers import get_stops, parse_stop
import unittest
from unittest.mock import patch


class GetStopsTestCase(unittest.TestCase):
    @patch("helpers.parse_stop")
    @patch("helpers.wbi_core")
    def test_get_stops(self, mock_wbi_core, mock_parse_stop):
        mock_wbi_core.ItemEngine.return_value.get_json_representation.side_effect = [
            {
                "claims": {
                    "P15": [{"mainsnak": {"datavalue": {"value": {"id": "Q22309"}}}}]
                }
            },
            {"labels": {"en": {"value": "MDB Stop Example"}}},
        ]
        mock_parse_stop.return_value = {"name": "MDB Stop Example"}

        test_catalog_id = "some_catalog_id"
        test_stops = [{"name": "MDB Stop Example"}]
        under_test = get_stops(test_catalog_id)

        self.assertEqual(under_test, test_stops)


class ParseStopTestCase(unittest.TestCase):
    def setUp(self):
        self.test_item_id = "Q22309"

    def test_parse_empty_stop(self):
        stop_json = {}
        under_test = parse_stop(stop_json, self.test_item_id)
        self.assertEqual(under_test, {"item_id": "Q22309"})

    def test_parse_partial_stop(self):
        stop_json = {
            "labels": {"en": {"value": "MDB Stop Example"}},
            "descriptions": {
                "en": {"value": "This is the MDB Stop representing the XYZ shared stop"}
            },
            "claims": {
                "P20": [{"mainsnak": {"datavalue": {"value": {"id": "Q22307"}}}}],
                "P90": [
                    {
                        "mainsnak": {
                            "datavalue": {"value": "mdb_stop_45_5017_N_73_5673_W"}
                        }
                    }
                ],
                "P92": [{"mainsnak": {"datavalue": {"value": "45.508888"}}}],
                "P93": [{"mainsnak": {"datavalue": {"value": "-73.561668"}}}],
                "P65": [{"mainsnak": {"datavalue": {"value": {"id": "Q22308"}}}}],
            },
        }
        under_test = parse_stop(stop_json, self.test_item_id)
        test_stop = {
            "item_id": "Q22309",
            "id": "mdb_stop_45_5017_N_73_5673_W",
            "name": "MDB Stop Example",
            "description": "This is the MDB Stop representing the XYZ shared stop",
            "latitude": 45.508888,
            "longitude": -73.561668,
        }
        self.assertEqual(under_test, test_stop)

    def test_parse_stop(self):
        stop_json = {
            "labels": {"en": {"value": "MDB Stop Example"}},
            "descriptions": {
                "en": {"value": "This is the MDB Stop representing the XYZ shared stop"}
            },
            "claims": {
                "P20": [{"mainsnak": {"datavalue": {"value": {"id": "Q22307"}}}}],
                "P90": [
                    {
                        "mainsnak": {
                            "datavalue": {"value": "mdb_stop_45_5017_N_73_5673_W"}
                        }
                    }
                ],
                "P92": [{"mainsnak": {"datavalue": {"value": "45.508888"}}}],
                "P93": [{"mainsnak": {"datavalue": {"value": "-73.561668"}}}],
                "P94": [
                    {
                        "mainsnak": {
                            "datavalue": {"value": "stop_id_from_a_source_dataset"}
                        },
                        "qualifiers": {
                            "P64": [{"datavalue": {"value": {"id": "Q81"}}}],
                            "P48": [{"datavalue": {"value": {"id": "Q80"}}}],
                        },
                    },
                    {
                        "mainsnak": {
                            "datavalue": {
                                "value": "stop_id_from_another_source_dataset"
                            }
                        },
                        "qualifiers": {
                            "P64": [{"datavalue": {"value": {"id": "Q265"}}}],
                            "P48": [{"datavalue": {"value": {"id": "Q82"}}}],
                        },
                    },
                ],
                "P65": [{"mainsnak": {"datavalue": {"value": {"id": "Q22308"}}}}],
            },
        }
        under_test = parse_stop(stop_json, self.test_item_id)
        test_stop = {
            "item_id": "Q22309",
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
        self.assertEqual(under_test, test_stop)

    def test_parse_stop_with_additional_field(self):
        stop_json = {
            "labels": {"en": {"value": "MDB Stop Example"}},
            "descriptions": {
                "en": {"value": "This is the MDB Stop representing the XYZ shared stop"}
            },
            "claims": {
                "P20": [{"mainsnak": {"datavalue": {"value": {"id": "Q22307"}}}}],
                "P90": [
                    {
                        "mainsnak": {
                            "datavalue": {"value": "mdb_stop_45_5017_N_73_5673_W"}
                        }
                    }
                ],
                "P92": [{"mainsnak": {"datavalue": {"value": "45.508888"}}}],
                "P93": [{"mainsnak": {"datavalue": {"value": "-73.561668"}}}],
                "P94": [
                    {
                        "mainsnak": {
                            "datavalue": {"value": "stop_id_from_a_source_dataset"}
                        },
                        "qualifiers": {
                            "P64": [{"datavalue": {"value": {"id": "Q81"}}}],
                            "P48": [{"datavalue": {"value": {"id": "Q80"}}}],
                        },
                    },
                    {
                        "mainsnak": {
                            "datavalue": {
                                "value": "stop_id_from_another_source_dataset"
                            }
                        },
                        "qualifiers": {
                            "P64": [{"datavalue": {"value": {"id": "Q265"}}}],
                            "P48": [{"datavalue": {"value": {"id": "Q82"}}}],
                        },
                    },
                ],
                "P65": [{"mainsnak": {"datavalue": {"value": {"id": "Q22308"}}}}],
            },
            "some_field": "some_value",
            "another_field": "some_other_value",
        }
        under_test = parse_stop(stop_json, self.test_item_id)
        test_stop = {
            "item_id": "Q22309",
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
        self.assertEqual(under_test, test_stop)
