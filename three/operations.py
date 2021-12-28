def add_source_stop():
    """Create a new MDB Source Stop."""
    raise NotImplemented


def update_source_stop():
    """Update a MDB Source Stop."""
    raise NotImplemented


def add_shared_stop():
    """Create a new MDB Shared Stop."""
    raise NotImplemented


def attach():
    """Attach a new referenced source stop to a MDB Shared Stop."""
    raise NotImplemented


def detach():
    """Detach a referenced source stop from a MDB Shared Stop.
    If the MDB Stop has no more referenced source stop attached to it, it is deleted."""
    raise NotImplemented


def get_stops():
    """Get all MDB Stops (Source and Shared)."""
    raise NotImplemented


def get_stops_by_bounding_box():
    """Get the MDB Stops (Source and Shared) included in the geographical bounding box."""
    raise NotImplemented


def get_stops_by_source_id():
    """Get the MDB Stops (Source and Shared) for the specified Source ID."""
    raise NotImplemented


def get_stops_by_dataset_version():
    """Get the MDB Stops for the specified Dataset version ID,
    i.e. the MDB stops being attached one or more referenced stops for the Dataset version ID."""
    raise NotImplemented


def get_stops_by_stop_id():
    """Get the MDB Stops (Source and Shared) for the specified Stop ID."""
    raise NotImplemented


def get_source_stops():
    """Get all MDB Source Stops."""
    raise NotImplemented


def get_source_stops_by_bounding_box():
    """Get the MDB Source Stops included in the geographical bounding box."""
    raise NotImplemented


def get_source_stops_by_source_id():
    """Get the MDB Source Stops for the specified Source ID."""
    raise NotImplemented


def get_source_stops_by_dataset_version():
    """Get the MDB Source Stops for the specified Dataset version ID."""
    raise NotImplemented


def get_source_stops_by_stop_id():
    """Get the MDB Source Stops for the specified Stop ID."""
    raise NotImplemented


def get_shared_stops():
    """Get all MDB Shared Stops."""
    raise NotImplemented


def get_shared_stops_by_bounding_box():
    """Get the MDB Shared Stops included in the geographical bounding box."""
    raise NotImplemented


def get_shared_stops_by_source_id():
    """Get the MDB Shared Stops for the specified Source ID,
    i.e. the MDB Stops being attached to one or more
    referenced MDB Source Stops for the Source ID."""
    raise NotImplemented


def get_shared_stops_by_dataset_version():
    """Get the MDB Shared Stops for the specified Dataset version ID,
    i.e. the MDB Shared Stops being attached one or more
    referenced MDB Source Stops for the Dataset version ID."""
    raise NotImplemented


def get_shared_stops_by_stop_id():
    """Get the MDB Shared Stops for the specified Stop ID,
    i.e. the MDB Shared Stops being attached one or more
    referenced MDB Source Stops identify by the specified Stop ID."""
    raise NotImplemented
