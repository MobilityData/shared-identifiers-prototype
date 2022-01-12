import argparse
import json
import gtfs_kit
import sys
from geopy.distance import distance
from tools.operations import (
    get_stops,
    get_stops_by_bounding_box,
    get_stops_by_stop_id,
    get_stops_by_source_id,
    get_stops_by_dataset_id,
)
from constants import (
    ID,
    NAME,
    DESCRIPTION,
    LATITUDE,
    LONGITUDE,
    STOP_ID,
    KM,
    GTFS_LOCATION_TYPE,
    GTFS_LOCATION_TYPE_STOP,
    GTFS_STOP_LAT,
    GTFS_STOP_LON,
    GTFS_STOP_NAME,
    GTFS_STOP_DESC,
    GTFS_STOP_ID,
)


GET_STOPS_FUNC = "get_stops_func"

STD_MAP = {GET_STOPS_FUNC: get_stops}

BOUNDING_BOX_MAP = {GET_STOPS_FUNC: get_stops_by_bounding_box}

SOURCE_ID_MAP = {GET_STOPS_FUNC: get_stops_by_source_id}

DATASET_ID_MAP = {GET_STOPS_FUNC: get_stops_by_dataset_id}

STOP_ID_MAP = {GET_STOPS_FUNC: get_stops_by_stop_id}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Shared Identifiers Prototype: Conflating script."
    )
    parser.add_argument(
        "-d",
        "--dataset",
        action="store",
        help="Dataset path or url.",
    )
    parser.add_argument(
        "-m",
        "--get-stops-mode",
        action="store",
        choices=["std", "bounding_box", "source_id", "dataset_id", "stop_id"],
        default="std",
        help="Get Stops mode.",
    )
    parser.add_argument(
        "-P",
        "--get-stops-parameters",
        action="store",
        default="{}",
        help="""Get Stops parameters. This must be a JSON string, where the keys reflect the parameters from the "
             "get_stops function you are using. Eg. If using get_stops_by_bounding_box, the JSON should be like"
             "{"max_latitude": 46, "min_latitude": 45, "max_longitude": -73, "min_longitude": -74}""",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        action="store",
        default="0.005",
        help="Radius threshold to compare the stops, a.k.a the conflating distance. Default: 0.005 km.",
    )
    args = parser.parse_args()

    # Step 1. The developer gets the MDB Stops using the filter that interest them, eg. by bounding box.
    mode_map = locals()[f"{args.get_stops_mode.upper()}_MAP"]
    kwargs = json.loads(args.get_stops_parameters)
    mdb_stops = mode_map[GET_STOPS_FUNC](**kwargs)

    # Step 2. The developer compares their Source stops to the fetched MDB Stops.
    dataset = gtfs_kit.read_feed(args.dataset, dist_units=KM)

    if dataset.stops is not None and GTFS_LOCATION_TYPE in dataset.stops.columns:
        # Transform the blank location types to 0.
        # According to the GTFS specification, blank location type is a Stop.
        dataset.stops[GTFS_LOCATION_TYPE] = dataset.stops[GTFS_LOCATION_TYPE].fillna(
            GTFS_LOCATION_TYPE_STOP
        )
        dataset.stops = dataset.stops

        # Stops.
        stops = dataset.stops.loc[
            dataset.stops[GTFS_LOCATION_TYPE] == GTFS_LOCATION_TYPE_STOP
        ]

        # Comparing stops.
        # Define the radius threshold.
        threshold = float(args.threshold)  # Default 0.005km = 5m.

        # Define the error margin.
        epsilon = 0.05

        # Maximum latitude delta. 1 latitude degree is in average.
        max_d_lat = threshold / 111.000 * (1 + epsilon)

        matches = []
        for mdb_stop_index, mdb_stop in mdb_stops.iterrows():
            mdb_lat = mdb_stop[LATITUDE]
            mdb_lon = mdb_stop[LONGITUDE]

            # Selecting the stops for which the latitude is located in the radius of the conflating distance.
            comparable_stops = stops[
                stops[GTFS_STOP_LAT].between(mdb_lat - max_d_lat, mdb_lat + max_d_lat)
            ]

            for stop_index, stop in comparable_stops.iterrows():
                mdb_coords = (mdb_lat, mdb_lon)
                stop_coords = (stop[GTFS_STOP_LAT], stop[GTFS_STOP_LON])

                if distance(mdb_coords, stop_coords) <= threshold:
                    stop_info = {
                        NAME: str(stop[GTFS_STOP_NAME]),
                        DESCRIPTION: str(stop[GTFS_STOP_DESC])
                        if str(stop[GTFS_STOP_DESC])
                        else str(stop[GTFS_STOP_NAME]),
                        LATITUDE: float(stop[GTFS_STOP_LAT]),
                        LONGITUDE: float(stop[GTFS_STOP_LON]),
                        STOP_ID: str(stop[GTFS_STOP_ID]),
                    }
                    matches.append({"mdb_stop": mdb_stop[ID], "stop": stop_info})

        sys.stdout.write(f"{matches}\n")
        sys.stdout.flush()
        sys.exit(0)
