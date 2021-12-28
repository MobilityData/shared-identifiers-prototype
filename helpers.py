import functools
import warnings
from wikibaseintegrator import wbi_core, wbi_login
from wikibaseintegrator.wbi_config import config as wbi_config
from contants import (
    MEDIAWIKI_API_URL,
    SPARQL_ENDPOINT_URL,
    WIKIBASE_URL,
    API_URL,
    SPARQL_BIGDATA_URL,
    SVC_URL,
    STOP_PROPERTY,
    CLAIMS,
    MAINSNAK,
    DATAVALUE,
    VALUE,
    ID,
    EN,
    LABELS,
    QUALIFIERS,
    DESCRIPTIONS,
    APPEND,
    ID_PROPERTY,
    LATITUDE_PROPERTY,
    LONGITUDE_PROPERTY,
    REFERENCED_STOP_PROPERTY,
    DATASET_PROPERTY,
    SOURCE_PROPERTY,
    INSTANCE_OF_PROPERTY,
    ID_KEY,
    NAME_KEY,
    DESCRIPTION_KEY,
    LATITUDE_KEY,
    LONGITUDE_KEY,
    STOP_ID_KEY,
    DATASET_ID_KEY,
    SOURCE_ID_KEY,
    REFERENCED_STOPS_KEY,
)


def configure(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wbi_config[MEDIAWIKI_API_URL] = API_URL
        wbi_config[SPARQL_ENDPOINT_URL] = SPARQL_BIGDATA_URL
        wbi_config[WIKIBASE_URL] = SVC_URL
        suppress_wbi_core_props_warning()
        value = func(*args, **kwargs)
        return value

    return wrapper


def suppress_wbi_core_props_warning():
    return warnings.filterwarnings("ignore", category=UserWarning)


@configure
def add_stop(
    catalog_id,
    instance_of,
    mdb_stop_id,
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
    stop_data = []

    # Instance Of property
    stop_data.append(
        wbi_core.ItemID(
            value=instance_of,
            prop_nr=INSTANCE_OF_PROPERTY,
        )
    )

    # Latitude property
    if latitude is not None:
        stop_data.append(
            wbi_core.String(
                value=str(latitude),
                prop_nr=LATITUDE_PROPERTY,
            )
        )

    # Longitude property
    if longitude is not None:
        stop_data.append(
            wbi_core.String(
                value=str(longitude),
                prop_nr=LONGITUDE_PROPERTY,
            )
        )

    # ID property
    if mdb_stop_id is not None:
        stop_data.append(
            wbi_core.String(
                value=mdb_stop_id,
                prop_nr=ID_PROPERTY,
            )
        )

    # Referenced stop qualifiers
    ref_qualifiers = []
    if ref_dataset_id:
        ref_qualifiers.append(
            wbi_core.ItemID(
                value=ref_dataset_id,
                prop_nr=DATASET_PROPERTY,
                is_qualifier=True,
            )
        )

    if ref_source_id:
        ref_qualifiers.append(
            wbi_core.ItemID(
                value=ref_source_id,
                prop_nr=SOURCE_PROPERTY,
                is_qualifier=True,
            )
        )

    # Referenced stop property
    if ref_stop_id:
        stop_data.append(
            wbi_core.String(
                value=ref_stop_id,
                prop_nr=REFERENCED_STOP_PROPERTY,
                qualifiers=ref_qualifiers,
            )
        )

    # Create the stop entity using the provided data
    stop_entity = wbi_core.ItemEngine(
        data=stop_data,
    )

    # Add the name and description
    if name:
        stop_entity.set_label(name, EN)
    if description:
        stop_entity.set_description(description, EN)

    if not username:
        raise ValueError("The username must be provided.")
    if not password:
        raise ValueError("The password must be provided.")
    login_instance = wbi_login.Login(user=username, pwd=password, use_clientlogin=True)

    # Create the stop entity on the database
    stop_entity_id = stop_entity.write(login_instance)

    # Create the stop property with the stop entity id and property
    stop_prop = wbi_core.ItemID(
        value=stop_entity_id,
        prop_nr=STOP_PROPERTY,
        if_exists=APPEND,
    )
    catalog_data = [stop_prop]

    # Update the catalog
    catalog_entity = wbi_core.ItemEngine(item_id=catalog_id)
    catalog_entity.update(catalog_data)
    catalog_entity_id = catalog_entity.write(login_instance)

    return stop_entity_id, catalog_entity_id


@configure
def attach(mdb_stop_id, ref_stop_id, ref_dataset_id, ref_source_id, username, password):
    # Referenced stop qualifiers
    ref_qualifiers = []
    if not ref_dataset_id:
        raise ValueError("The Referenced dataset id must be provided.")
    ref_qualifiers.append(
        wbi_core.ItemID(
            value=ref_dataset_id,
            prop_nr=DATASET_PROPERTY,
            is_qualifier=True,
        )
    )

    if not ref_source_id:
        raise ValueError("The Referenced source id must be provided.")
    ref_qualifiers.append(
        wbi_core.ItemID(
            value=ref_source_id,
            prop_nr=SOURCE_PROPERTY,
            is_qualifier=True,
        )
    )

    # Create the Referenced stop property with the ref stop entity id and ref qualifiers
    if not ref_stop_id:
        raise ValueError("The Referenced stop id must be provided.")
    ref_stop_prop = wbi_core.String(
        value=ref_stop_id,
        prop_nr=REFERENCED_STOP_PROPERTY,
        qualifiers=ref_qualifiers,
        if_exists=APPEND,
    )
    stop_data = [ref_stop_prop]

    if not username:
        raise ValueError("The username must be provided.")
    if not password:
        raise ValueError("The password must be provided.")
    login_instance = wbi_login.Login(user=username, pwd=password, use_clientlogin=True)

    # Attach the referenced stop to the mdb stop
    stop_entity = wbi_core.ItemEngine(item_id=mdb_stop_id)
    stop_entity.update(stop_data)
    stop_entity_id = stop_entity.write(login_instance)

    return stop_entity_id


@configure
def get_stops(catalog_id):
    stops = []
    catalog_item = wbi_core.ItemEngine(item_id=catalog_id)
    catalog_json = catalog_item.get_json_representation()
    if STOP_PROPERTY in catalog_json[CLAIMS]:
        stop_ids = [
            stop[MAINSNAK][DATAVALUE][VALUE][ID]
            for stop in catalog_json[CLAIMS][STOP_PROPERTY]
        ]
        for stop_id in stop_ids:
            stop_item = wbi_core.ItemEngine(item_id=stop_id)
            stop_json = stop_item.get_json_representation()
            stop = parse_stop(stop_json)
            stops.append(stop)
    return stops


def parse_stop(stop_json):
    stop = {}

    stop_mdb_id_values = stop_json.get(CLAIMS, {}).get(ID_PROPERTY, [])
    if stop_mdb_id_values:
        stop_mdb_id = stop_mdb_id_values[0][MAINSNAK][DATAVALUE][VALUE]
        if stop_mdb_id:
            stop[ID_KEY] = stop_mdb_id

    stop_name = stop_json.get(LABELS, {}).get(EN, {}).get(VALUE)
    if stop_name:
        stop[NAME_KEY] = stop_name

    stop_description = stop_json.get(DESCRIPTIONS, {}).get(EN, {}).get(VALUE)
    if stop_description:
        stop[DESCRIPTION_KEY] = stop_description

    stop_latitude_values = stop_json.get(CLAIMS, {}).get(LATITUDE_PROPERTY, [])
    if stop_latitude_values:
        stop_latitude = stop_latitude_values[0][MAINSNAK][DATAVALUE][VALUE]
        if stop_latitude:
            stop[LATITUDE_KEY] = float(stop_latitude)

    stop_longitude_values = stop_json.get(CLAIMS, {}).get(LONGITUDE_PROPERTY, [])
    if stop_longitude_values:
        stop_longitude = stop_longitude_values[0][MAINSNAK][DATAVALUE][VALUE]
        if stop_longitude:
            stop[LONGITUDE_KEY] = float(stop_longitude)

    stop_referenced_stops_values = stop_json.get(CLAIMS, {}).get(
        REFERENCED_STOP_PROPERTY, []
    )
    if stop_referenced_stops_values:
        referenced_stops = []
        for stop_referenced_stops_value in stop_referenced_stops_values:
            referenced_stop = {
                STOP_ID_KEY: stop_referenced_stops_value[MAINSNAK][DATAVALUE][VALUE]
            }
            referenced_stop_qualifiers = stop_referenced_stops_value[QUALIFIERS]
            if DATASET_PROPERTY in referenced_stop_qualifiers:
                referenced_stop[DATASET_ID_KEY] = referenced_stop_qualifiers[
                    DATASET_PROPERTY
                ][0][DATAVALUE][VALUE][ID]
            if SOURCE_PROPERTY in referenced_stop_qualifiers:
                referenced_stop[SOURCE_ID_KEY] = referenced_stop_qualifiers[
                    SOURCE_PROPERTY
                ][0][DATAVALUE][VALUE][ID]
            referenced_stops.append(referenced_stop)
        if referenced_stops:
            stop[REFERENCED_STOPS_KEY] = referenced_stops

    return stop


def generate_id(prefix, latitude, longitude):
    latitude_str = format_coordinate(latitude)
    latitude_direction = "N" if latitude >= 0 else "S"
    longitude_str = format_coordinate(longitude)
    longitude_direction = "E" if latitude >= 0 else "W"
    return f"{prefix}_{latitude_str}_{latitude_direction}_{longitude_str}_{longitude_direction}"


def format_coordinate(coordinate):
    coordinate_str = format(coordinate, ".6f")
    coordinate_str = coordinate_str.replace(".", "_")
    coordinate_str = coordinate_str.replace("-", "")
    return coordinate_str
