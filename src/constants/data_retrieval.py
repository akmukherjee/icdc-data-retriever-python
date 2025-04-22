# src/constants/data_retrieval.py
from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class DataRetrievalConstants:
    IDC_API_BASE_URL: Final = "https://api.imaging.datacommons.cancer.gov/v1"
    IDC_COLLECTION_BASE_URL: Final = (
        "https://portal.imaging.datacommons.cancer.gov/explore/filters/?collection_id="
    )
    IDC_API_COLLECTIONS_ENDPOINT: Final = "/collections"
    TCIA_API_BASE_URL: Final = "https://services.cancerimagingarchive.net/services/v4"
    TCIA_COLLECTION_BASE_URL: Final = (
        "https://nbia.cancerimagingarchive.net/nbia-search/?MinNumberOfStudiesCriteria=1&CollectionCriteria="
    )
    TCIA_API_COLLECTIONS_ENDPOINT: Final = "/TCIA/query/getCollectionValues"
    TCIA_API_SERIES_ENDPOINT: Final = "/TCIA/query/getSeries?Collection="
    BENTO_BACKEND_GRAPHQL_URI: Final = "https://caninecommons.cancer.gov/v1/graphql/"


data_retrieval_constants = DataRetrievalConstants()
