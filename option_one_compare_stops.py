import argparse
import json
import gtfs_kit
from geopy.distance import distance
from one.operations import (
    get_stops,
    get_stops_by_bounding_box,
    get_stops_by_stop_id,
    get_stops_by_source_id,
    get_stops_by_dataset_id,
    add,
    attach,
)
from contants import (
    ITEM_ID_KEY,
    NAME_KEY,
    DESCRIPTION_KEY,
    LATITUDE_KEY,
    LONGITUDE_KEY,
    STOP_ID_KEY,
    DATASET_ID_KEY,
    SOURCE_ID_KEY,
)

BIG_BLUE_BUS_DATASET_URL = "https://storage.googleapis.com/storage/v1/b/big-blue-bus-gtfs-q38419_archives_2021-12-07/o/71c984db15d56ea951b7f8e05881b1ffed415f03.zip?alt=media"
BIG_BLUE_BUS_DATASET_ID = "Q22304"
BIG_BLUE_BUS_SOURCE_ID = "Q1856"

LOCATION_TYPE = "location_type"
STOP_NAME = "stop_name"
STOP_DESC = "stop_desc"
STOP_LAT = "stop_lat"
STOP_LON = "stop_lon"
STOP_ID = "stop_id"

STOP = 0
KM = "km"

GET_STOPS_FUNC = "get_stops_func"

STD_MAP = {GET_STOPS_FUNC: get_stops}

BOUNDING_BOX_MAP = {GET_STOPS_FUNC: get_stops_by_bounding_box}

SOURCE_ID_MAP = {GET_STOPS_FUNC: get_stops_by_source_id}

DATASET_ID_MAP = {GET_STOPS_FUNC: get_stops_by_dataset_id}

STOP_ID_MAP = {GET_STOPS_FUNC: get_stops_by_stop_id}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Shared Identifiers Prototype - Option One: Compare stops"
    )
    parser.add_argument(
        "-u",
        "--username",
        action="store",
        help="Username",
    )
    parser.add_argument(
        "-p",
        "--password",
        action="store",
        help="Password",
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
        help="Radius threshold to compare the stops. Default: 0.005 km.",
    )
    args = parser.parse_args()

    # Step 1. The developer gets the MDB Stops using the filter that interest them, eg. by bounding box.
    mode_map = locals()[f"{args.get_stops_mode.upper()}_MAP"]
    kwargs = json.loads(args.get_stops_parameters)
    mdb_stops = mode_map[GET_STOPS_FUNC](**kwargs)

    # Step 2. The developer compares their Source stops to the fetched MDB Stops.
    dataset = gtfs_kit.read_feed(BIG_BLUE_BUS_DATASET_URL, dist_units=KM)

    if dataset.stops is not None and LOCATION_TYPE in dataset.stops.columns:
        # Transform the blank location types to 0
        # According to the GTFS specification, blank location type is a Stop
        dataset.stops[LOCATION_TYPE] = dataset.stops[LOCATION_TYPE].fillna(0)
        dataset.stops = dataset.stops

        # Stops
        stops = dataset.stops.loc[dataset.stops[LOCATION_TYPE] == STOP]

        # Comparing stops
        # Define the radius threshold
        threshold = float(args.threshold)  # Default 0.005km = 5m.

        # Define the error margin
        epsilon = 0.05

        # Maximum latitude delta. 1 latitude degree is in average
        max_d_lat = threshold / 111.000 * (1 + epsilon)

        matches = []
        matching_indices = set()
        for mdb_stop in mdb_stops:
            mdb_lat = mdb_stop[LATITUDE_KEY]
            mdb_lon = mdb_stop[LONGITUDE_KEY]

            # Selecting the stops with the latitudes included in the mdb_stop radius according to the threshold
            comparable_stops = stops[
                stops[STOP_LAT].between(mdb_lat - max_d_lat, mdb_lat + max_d_lat)
            ]

            for index, stop in comparable_stops.iterrows():
                mdb_coords = (mdb_lat, mdb_lon)
                stop_coords = (stop[STOP_LAT], stop[STOP_LON])

                if distance(mdb_coords, stop_coords) <= threshold:
                    stop_info = {
                        NAME_KEY: str(stop[STOP_NAME]),
                        DESCRIPTION_KEY: str(stop[STOP_DESC]),
                        LATITUDE_KEY: float(stop[STOP_LAT]),
                        LONGITUDE_KEY: float(stop[STOP_LON]),
                        STOP_ID_KEY: str(stop[STOP_ID]),
                        DATASET_ID_KEY: str(BIG_BLUE_BUS_DATASET_ID),
                        SOURCE_ID_KEY: str(BIG_BLUE_BUS_SOURCE_ID),
                    }
                    matches.append({"mdb_stop": mdb_stop, "stop": stop_info})
                    matching_indices.add(index)

        for match in matches:
            print(match)

        # Step 3. For every matching stop, the developer add the shared identifier to the stop in the GTFS dataset
        # and use the attach operation to update the MDB stops so that it contains the information
        # about the stop using its reference.

        # TODO if you want to attach the matched stops in the database
        # for mdb_stop, stop in matches:
        #     attach(
        #         mdb_stop_item_id=mdb_stop[ITEM_ID_KEY],
        #         ref_stop_id=str(stop[STOP_ID]),
        #         ref_dataset_id=str(BIG_BLUE_BUS_DATASET_ID),
        #         ref_source_id=str(BIG_BLUE_BUS_SOURCE_ID),
        #         username=args.username,
        #         password=args.password,
        #     )

        # Step 4. For every stop left unmatched, the developer use the add operation to create a new MDB stop.

        # TODO if you want to add the unmatched stops in the database
        # matched_stops = stops.index.isin(list(matching_indices))
        # unmatched_stops = stops[~matched_stops]
        # for index, unmatched_stop in unmatched_stops.iterrows():
        #     add(
        #         name=str(unmatched_stop[STOP_NAME]),
        #         description=str(unmatched_stop[STOP_DESC]),
        #         latitude=float(unmatched_stop[STOP_LAT]),
        #         longitude=float(unmatched_stop[STOP_LON]),
        #         ref_stop_id=str(unmatched_stop[STOP_ID]),
        #         ref_dataset_id=str(BIG_BLUE_BUS_DATASET_ID),
        #         ref_source_id=str(BIG_BLUE_BUS_SOURCE_ID),
        #         username=args.username,
        #         password=args.password,
        #     )
