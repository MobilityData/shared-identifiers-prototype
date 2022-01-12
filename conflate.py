import argparse
import json
import gtfs_kit
from geopy.distance import distance
from tools.operations import (
    get_stops,
    get_stops_by_bounding_box,
    get_stops_by_stop_id,
    get_stops_by_source_id,
    get_stops_by_dataset_id,
    attach_ref_stop,
    add_stop,
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
    MDB_STOP_KEY,
    SOURCE_STOP_KEY,
    YES,
    NO,
    EMPTY_STRING,
)


GET_STOPS_FUNC = "get_stops_func"

STD_MAP = {GET_STOPS_FUNC: get_stops}

BOUNDING_BOX_MAP = {GET_STOPS_FUNC: get_stops_by_bounding_box}

SOURCE_ID_MAP = {GET_STOPS_FUNC: get_stops_by_source_id}

DATASET_ID_MAP = {GET_STOPS_FUNC: get_stops_by_dataset_id}

STOP_ID_MAP = {GET_STOPS_FUNC: get_stops_by_stop_id}

ATTACH_QUESTION = (
    "A match have been detected ({n_match}/{n_matches}). "
    "Your stop with `stop_name = {source_stop_name}` "
    "and `stop_id = {source_stop_id}` is matching "
    "the MDB Stop with `id = {mdb_stop_id}`. "
    "Do you want to attach your stop to this MDB stop? {yes}/{no}\n"
)

ADD_QUESTION = (
    "Your stop with `stop_name = {source_stop_name}` "
    "and `stop_id = {source_stop_id}` have been left unmatched ({n_unmatched}/{n_unmatched_stops}). "
    "Do you want to add a new MDB Stop and attach your stop to it? {yes}/{no}\n"
)


def ask(question):
    while True:
        query = input(question).lower()
        if query not in [YES, NO]:
            print(f"Please answer with {YES} (yes) or {NO} (no).")
        else:
            break
    return True if query == YES else False


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
        "-D",
        "--dataset-id",
        action="store",
        help="Stable dataset ID for the provided dataset.",
    )
    parser.add_argument(
        "-S",
        "--source-id",
        action="store",
        help="Stable source ID for the provided dataset.",
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
        "-p",
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

        # Transform the null (NaN) descriptions to the empty string.
        # According to the GTFS specification, a stop description is optional and can be null.
        dataset.stops[GTFS_STOP_DESC] = dataset.stops[GTFS_STOP_DESC].fillna(
            EMPTY_STRING
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

        # Maximum latitude delta. 1 latitude degree is 111 km in average.
        max_d_lat = threshold / 111.000 * (1 + epsilon)

        matches = []
        matches_indices = set()
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
                    matches.append(
                        {MDB_STOP_KEY: mdb_stop[ID], SOURCE_STOP_KEY: stop_info}
                    )
                    matches_indices.add(stop_index)

        # Step 3. For every matching stop, the developer add the shared identifier to the stop in the GTFS dataset
        # and use the attach operation to update the MDB stops so that it contains the information
        # about the stop using its reference.
        n_match = 0
        for match in matches:
            n_match += 1
            mbd_stop_id = str(match[MDB_STOP_KEY])
            source_stop_id = str(match[SOURCE_STOP_KEY][STOP_ID])
            source_stop_name = str(match[SOURCE_STOP_KEY][NAME])

            answer = ask(
                ATTACH_QUESTION.format(
                    n_match=n_match,
                    n_matches=len(matches),
                    source_stop_name=source_stop_name,
                    source_stop_id=source_stop_id,
                    mdb_stop_id=mbd_stop_id,
                    yes=YES,
                    no=NO,
                )
            )
            if answer is True:
                attach_ref_stop(
                    mdb_stop_id=mbd_stop_id,
                    ref_stop_id=source_stop_id,
                    ref_dataset_id=args.dataset_id,
                    ref_source_id=args.source_id,
                )

        # Step 4. For every stop left unmatched, the developer use the add operation to create a new MDB stop.
        matched_stops = stops.index.isin(list(matches_indices))
        unmatched_stops = stops[~matched_stops]
        n_unmatched = 0
        for index, unmatched_stop in unmatched_stops.iterrows():
            n_unmatched += 1
            source_stop_id = str(unmatched_stop[GTFS_STOP_ID])
            source_stop_name = str(unmatched_stop[GTFS_STOP_NAME])

            answer = ask(
                ADD_QUESTION.format(
                    n_unmatched=n_unmatched,
                    n_unmatched_stops=unmatched_stops.index.size,
                    source_stop_name=source_stop_name,
                    source_stop_id=source_stop_id,
                    yes=YES,
                    no=NO,
                )
            )
            if answer is True:
                add_stop(
                    name=source_stop_name,
                    description=str(unmatched_stop[GTFS_STOP_DESC])
                    if str(unmatched_stop[GTFS_STOP_DESC])
                    else source_stop_name,
                    latitude=float(unmatched_stop[GTFS_STOP_LAT]),
                    longitude=float(unmatched_stop[GTFS_STOP_LON]),
                    ref_stop_id=source_stop_id,
                    ref_dataset_id=args.dataset_id,
                    ref_source_id=args.source_id,
                )
