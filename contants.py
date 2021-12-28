# STAGING ITEMS
CATALOG_OF_MDB_STOPS_ID = "Q22308"
MDB_STOP_ITEM_ID = "Q22307"

MDB_STOP_ID_PREFIX = "mdb_stop"

# STAGING PROPERTIES
STOP_PROPERTY = "P15"
INSTANCE_OF_PROPERTY = "P20"
ID_PROPERTY = "P90"
LATITUDE_PROPERTY = "P92"
LONGITUDE_PROPERTY = "P93"
REFERENCED_STOP_PROPERTY = "P94"
DATASET_PROPERTY = "P64"
SOURCE_PROPERTY = "P48"
CATALOG_PROPERTY = "P65"

# API
CLAIMS = "claims"
MAINSNAK = "mainsnak"
DATAVALUE = "datavalue"
VALUE = "value"
ID = "id"
LABELS = "labels"
EN = "en"
QUALIFIERS = "qualifiers"
DESCRIPTIONS = "descriptions"
APPEND = "APPEND"

# STOP KEYS
ITEM_ID_KEY = "item_id"  # Refers to the Wikibase item ID
ID_KEY = "id"  # Refers to the MDB ID
NAME_KEY = "name"
DESCRIPTION_KEY = "description"
LATITUDE_KEY = "latitude"
LONGITUDE_KEY = "longitude"
STOP_ID_KEY = "stop_id"
DATASET_ID_KEY = "dataset_id"
SOURCE_ID_KEY = "source_id"
REFERENCED_STOPS_KEY = "referenced_stops"

# WIKIBASE INTEGRATOR
MEDIAWIKI_API_URL = "MEDIAWIKI_API_URL"
SPARQL_ENDPOINT_URL = "SPARQL_ENDPOINT_URL"
WIKIBASE_URL = "WIKIBASE_URL"

# STAGING URLS
SPARQL_URL = (
    "http://staging.mobilitydatabase.org:8282//proxy/wdqs/bigdata/namespace/wdq/sparql"
)
SPARQL_BIGDATA_URL = "http://staging.mobilitydatabase.org:8989/bigdata/sparql"
API_URL = "http://staging.mobilitydatabase.org/w/api.php"
SVC_URL = "http://wikibase.svc"
