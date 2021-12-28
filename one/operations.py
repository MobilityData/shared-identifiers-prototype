import helpers
from contants import (
    CATALOG_OF_MDB_STOPS_ID,
    MDB_STOP_ITEM_ID,
    REFERENCED_STOPS_KEY,
    STOP_ID_KEY,
    DATASET_ID_KEY,
    SOURCE_ID_KEY,
    LATITUDE_KEY,
    LONGITUDE_KEY,
    MDB_STOP_ID_PREFIX,
)


def add(
    name,
    description,
    latitude,
    longitude,
    ref_stop_id,
    ref_dataset_id,
    ref_source_id,
    username,
    password,
):
    """Create a new MDB Stop and attach its first referenced stop."""
    return helpers.add_stop(
        catalog_id=CATALOG_OF_MDB_STOPS_ID,
        instance_of=MDB_STOP_ITEM_ID,
        mdb_stop_id=helpers.generate_id(MDB_STOP_ID_PREFIX, latitude, longitude),
        name=name,
        description=description,
        latitude=latitude,
        longitude=longitude,
        ref_stop_id=ref_stop_id,
        ref_dataset_id=ref_dataset_id,
        ref_source_id=ref_source_id,
        username=username,
        password=password,
    )


def attach(mdb_stop_id, ref_stop_id, ref_dataset_id, ref_source_id, username, password):
    """Attach a new referenced stop to a MDB Stop."""
    return helpers.attach(
        mdb_stop_id=mdb_stop_id,
        ref_stop_id=ref_stop_id,
        ref_dataset_id=ref_dataset_id,
        ref_source_id=ref_source_id,
        username=username,
        password=password,
    )


def detach(ref_stop_id, ref_dataset_id, ref_source_id, username, password):
    """Detach a referenced stop from a MDB Stop.
    If the MDB Stop has no more referenced stop attached to it, it is deleted."""
    raise NotImplemented


def get_stops():
    """Get all MDB Stops."""
    return helpers.get_stops(CATALOG_OF_MDB_STOPS_ID)


def get_stops_by_bounding_box(max_latitude, min_latitude, max_longitude, min_longitude):
    """Get the MDB Stops included in the geographical bounding box."""
    return [
        stop
        for stop in helpers.get_stops(CATALOG_OF_MDB_STOPS_ID)
        if max_latitude >= stop[LATITUDE_KEY] >= min_latitude
        and max_longitude >= stop[LONGITUDE_KEY] >= min_longitude
    ]


def get_stops_by_source_id(source_id):
    """Get the MDB Stops for the specified Source ID,
    i.e. the MDB stops being attached to one or more referenced stops for the Source ID."""
    return [
        stop
        for stop in helpers.get_stops(CATALOG_OF_MDB_STOPS_ID)
        if any(
            referenced_stop
            for referenced_stop in stop.get(REFERENCED_STOPS_KEY, [])
            if referenced_stop[SOURCE_ID_KEY] == source_id
        )
    ]


def get_stops_by_dataset_id(dataset_id):
    """Get the MDB Stops for the specified Dataset version ID,
    i.e. the MDB stops being attached one or more referenced stops for the Dataset version ID."""
    return [
        stop
        for stop in helpers.get_stops(CATALOG_OF_MDB_STOPS_ID)
        if any(
            referenced_stop
            for referenced_stop in stop.get(REFERENCED_STOPS_KEY, [])
            if referenced_stop[DATASET_ID_KEY] == dataset_id
        )
    ]


def get_stops_by_stop_id(stop_id):
    """Get the MDB Stops for the specified Stop ID,
    i.e. the MDB stops being attached one or more referenced stops identify by the specified Stop ID."""
    return [
        stop
        for stop in helpers.get_stops(CATALOG_OF_MDB_STOPS_ID)
        if any(
            referenced_stop
            for referenced_stop in stop.get(REFERENCED_STOPS_KEY, [])
            if referenced_stop[STOP_ID_KEY] == stop_id
        )
    ]
