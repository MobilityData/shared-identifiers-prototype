def add():
    """Create a new MDB Stop and attach its first referenced stop."""
    raise NotImplemented


def attach():
    """Attach a new referenced stop to a MDB Stop."""
    raise NotImplemented


def detach():
    """Detach a referenced stop from a MDB Stop.
    If the MDB Stop has no more referenced stop attached to it, it is deleted."""
    raise NotImplemented


def get_stops():
    """Get all MDB Stops."""
    raise NotImplemented


def get_stops_by_bounding_box():
    """Get the MDB Stops included in the geographical bounding box."""
    raise NotImplemented


def get_stops_by_source_id():
    """Get the MDB Stops for the specified Source ID,
    i.e. the MDB stops being attached to one or more referenced stops for the Source ID."""
    raise NotImplemented


def get_stops_by_dataset_version():
    """Get the MDB Stops for the specified Dataset version ID,
    i.e. the MDB stops being attached one or more referenced stops for the Dataset version ID."""
    raise NotImplemented


def get_stops_by_stop_id():
    """Get the MDB Stops for the specified Stop ID,
    i.e. the MDB stops being attached one or more referenced stops identify by the specified Stop ID."""
    raise NotImplemented
