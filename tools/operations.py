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
    # Don't add twice a mdb stop with exactly the same coordinates
    if not stops[(stops[LATITUDE] == latitude) & (stops[LONGITUDE] == longitude)].empty:
        raise ValueError(
            "A MDB Stop already exist with exactly the same coordinates "
            "as the given `latitude` and `longitude`. Impossible to add the stop."
        )
    # Add new stop
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
    # Attach referenced stop if the given MDB Stop ID exist and is not duplicated
    mdb_stop_index_series = stops[stops[ID] == mdb_stop_id].index
    if mdb_stop_index_series.size < 1:
        raise ValueError(
            "The given `mdb_stop_id` does not exist. Impossible to attach a referenced stop."
        )
    elif mdb_stop_index_series.size > 1:
        raise ValueError(
            "Several MDB Stop share the same `mdb_stop_id`. Please contact the administrator."
        )
    mdb_stop_index = mdb_stop_index_series[0]
    referenced_stops = ast.literal_eval(stops.at[mdb_stop_index, REFERENCED_STOPS])
    referenced_stops.append(
        {STOP_ID: ref_stop_id, DATASET_ID: ref_dataset_id, SOURCE_ID: ref_source_id}
    )
    stops.at[mdb_stop_index, REFERENCED_STOPS] = referenced_stops
    helpers.save_stops(stops)
    return stops


def detach_ref_stop(mdb_stop_id, ref_stop_id, ref_dataset_id, ref_source_id):
    """Detach a referenced stop from a MDB Stop."""
    stops = helpers.load_stops()
    # Detach referenced stop if the given MDB Stop ID exist and is not duplicated
    mdb_stop_index_series = stops[stops[ID] == mdb_stop_id].index
    if mdb_stop_index_series.size < 1:
        raise ValueError(
            "The given `mdb_stop_id` does not exist. Impossible to detach a referenced stop."
        )
    elif mdb_stop_index_series.size > 1:
        raise ValueError(
            "Several MDB Stop share the same `mdb_stop_id`. Please contact the administrator."
        )
    mdb_stop_index = mdb_stop_index_series[0]
    referenced_stops = ast.literal_eval(stops.at[mdb_stop_index, REFERENCED_STOPS])
    referenced_stops = [
        ref_stop
        for ref_stop in referenced_stops
        if ref_stop[STOP_ID] != ref_stop_id
        and ref_stop[DATASET_ID] != ref_dataset_id
        and ref_stop[SOURCE_ID] != ref_source_id
    ]
    stops.at[mdb_stop_index, REFERENCED_STOPS] = referenced_stops
    helpers.save_stops(stops)
    return stops


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
                [ref_stop for ref_stop in ref_stops if ref_stop[SOURCE_ID] == source_id]
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
                    if ref_stop[DATASET_ID] == dataset_id
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
                [ref_stop for ref_stop in ref_stops if ref_stop[STOP_ID] == stop_id]
            )
        )
    ]
