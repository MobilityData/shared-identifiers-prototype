import pandas as pd
import ast
import tools.helpers as helpers
from constants import (
    ID,
    NAME,
    DESCRIPTION,
    LATITUDE,
    LONGITUDE,
    REFERENCED_STOPS,
    SOURCE_ID,
    DATASET_ID,
    STOP_ID,
    MDB_STOP_ID_PREFIX,
)


def add_stop(
    name, description, latitude, longitude, ref_stop_id, ref_dataset_id, ref_source_id
):
    """Create a new MDB Stop and attach its first referenced stop."""
    stops = helpers.load_stops()
    new_stop = pd.DataFrame(
        [
            [
                helpers.generate_id(MDB_STOP_ID_PREFIX, latitude, longitude),
                name,
                description,
                latitude,
                longitude,
                [
                    {
                        STOP_ID: ref_stop_id,
                        DATASET_ID: ref_dataset_id,
                        SOURCE_ID: ref_source_id,
                    }
                ],
            ]
        ],
        columns=[ID, NAME, DESCRIPTION, LATITUDE, LONGITUDE, REFERENCED_STOPS],
    )
    stops = pd.concat([stops, new_stop], ignore_index=True)
    helpers.save_stops(stops)
    return stops


def attach_ref_stop(mdb_stop_id, ref_stop_id, ref_dataset_id, ref_source_id):
    """Attach a new referenced stop to a MDB Stop."""
    stops = helpers.load_stops()
    referenced_stops = stops.loc[stops.ID == mdb_stop_id, REFERENCED_STOPS]
    referenced_stops.append(
        {STOP_ID: ref_stop_id, DATASET_ID: ref_dataset_id, SOURCE_ID: ref_source_id}
    )
    stops.loc[stops.ID == mdb_stop_id, REFERENCED_STOPS] = referenced_stops
    helpers.save_stops(stops)
    return stops


def detach_ref_stop(mdb_stop_id, ref_stop_id, ref_dataset_id, ref_source_id):
    """Detach a referenced stop from a MDB Stop.
    If the MDB Stop has no more referenced stop attached to it, it is deleted."""
    raise NotImplemented


def get_stops():
    """Get all MDB Stops."""
    return helpers.load_stops()


def get_stops_by_bounding_box(max_latitude, min_latitude, max_longitude, min_longitude):
    """Get the MDB Stops included in the geographical bounding box."""
    stops = helpers.load_stops()
    return stops.loc[
        (max_latitude >= stops[LATITUDE])
        & (stops[LATITUDE] >= min_latitude)
        & (max_longitude >= stops[LONGITUDE])
        & (stops[LONGITUDE] >= min_longitude)
    ]


def get_stops_by_source_id(source_id):
    """Get the MDB Stops for the specified Source ID,
    i.e. the MDB stops being attached to one or more referenced stops for the Source ID."""
    stops = helpers.load_stops()
    return stops.loc[
        stops[REFERENCED_STOPS]
        .apply(ast.literal_eval)
        .apply(
            lambda ref_stops: any(
                [
                    ref_stop
                    for ref_stop in ref_stops
                    if ref_stop.get(SOURCE_ID) == source_id
                ]
            )
        )
    ]


def get_stops_by_dataset_id(dataset_id):
    """Get the MDB Stops for the specified Dataset version ID,
    i.e. the MDB stops being attached one or more referenced stops for the Dataset version ID."""
    stops = helpers.load_stops()
    return stops.loc[
        stops[REFERENCED_STOPS]
        .apply(ast.literal_eval)
        .apply(
            lambda ref_stops: any(
                [
                    ref_stop
                    for ref_stop in ref_stops
                    if ref_stop.get(DATASET_ID) == dataset_id
                ]
            )
        )
    ]


def get_stops_by_stop_id(stop_id):
    """Get the MDB Stops for the specified Stop ID,
    i.e. the MDB stops being attached one or more referenced stops identify by the specified Stop ID."""
    stops = helpers.load_stops()
    return stops.loc[
        stops[REFERENCED_STOPS]
        .apply(ast.literal_eval)
        .apply(
            lambda ref_stops: any(
                [ref_stop for ref_stop in ref_stops if ref_stop.get(STOP_ID) == stop_id]
            )
        )
    ]
