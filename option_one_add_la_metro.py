import argparse
import gtfs_kit
from one.operations import add

LA_METRO_DATASET_URL = "https://storage.googleapis.com/storage/v1/b/la-metro-rail-gtfs-q26378_archives_2021-12-26/o/111876f6d55200cf587a2c19602d0b6532d393ac.zip?alt=media"
LA_METRO_DATASET_ID = "Q22306"
LA_METRO_SOURCE_ID = "Q22305"

LOCATION_TYPE = "location_type"
STOP_NAME = "stop_name"
STOP_DESC = "stop_desc"
STOP_LAT = "stop_lat"
STOP_LON = "stop_lon"
STOP_ID = "stop_id"

STOP = 0
KM = "km"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Shared Identifiers Prototype - Option One: Add LA Metro Stops"
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
    args = parser.parse_args()

    dataset = gtfs_kit.read_feed(LA_METRO_DATASET_URL, dist_units=KM)

    if dataset.stops is not None and LOCATION_TYPE in dataset.stops.columns:
        # Transform the blank location types to 0
        # According to the GTFS specification, blank location type is a Stop
        dataset.stops[LOCATION_TYPE] = dataset.stops[LOCATION_TYPE].fillna(0)
        dataset.stops = dataset.stops

        # Remove NaN descriptions
        dataset.stops[STOP_DESC] = dataset.stops[STOP_DESC].fillna("")
        dataset.stops = dataset.stops

        # Stops
        stops = dataset.stops.loc[dataset.stops[LOCATION_TYPE] == STOP]
        for index, stop in stops.iterrows():
            add(
                name=str(stop[STOP_NAME]),
                description=str(stop[STOP_DESC]),
                latitude=float(stop[STOP_LAT]),
                longitude=float(stop[STOP_LON]),
                ref_stop_id=str(stop[STOP_ID]),
                ref_dataset_id=str(LA_METRO_DATASET_ID),
                ref_source_id=str(LA_METRO_SOURCE_ID),
                username=args.username,
                password=args.password,
            )
