import functools
import warnings
from wikibaseintegrator import wbi_core
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
    ID_PROPERTY,
    LATITUDE_PROPERTY,
    LONGITUDE_PROPERTY,
    REFERENCED_STOP_PROPERTY,
    DATASET_PROPERTY,
    SOURCE_PROPERTY,
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
