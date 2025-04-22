# src/fetch_data.py
import asyncio
from typing import List, Dict, Any
import aiohttp
from bs4 import BeautifulSoup
import json

from config import config
from constants.data_retrieval import data_retrieval_constants as constants
from utils.array_utils import filter_object_array


async def get_idc_collections() -> List[Dict[str, Any]]:
    """
    Retrieves image collection data from the IDC API and filters for collections relevant to ICDC.
    """
    async with aiohttp.ClientSession() as session:
        try:
            url = (
                f"{constants.IDC_API_BASE_URL}{constants.IDC_API_COLLECTIONS_ENDPOINT}"
            )
            async with session.get(url) as response:
                if not response.ok:
                    raise ValueError(
                        f"IDC collection request failed ({response.status}): {response.reason}"
                    )
                data = await response.json()
                return filter_object_array(
                    data["collections"], "collection_id", "icdc_"
                )
        except Exception as error:
            print(f"Error fetching IDC collections: {str(error)}")
            raise ValueError(f"IDC internal server error: {str(error)}")


async def get_tcia_collections() -> List[str]:
    """
    Retrieves image collection data from the TCIA API and filters for collection IDs relevant to ICDC.
    """
    async with aiohttp.ClientSession() as session:
        try:
            url = f"{constants.TCIA_API_BASE_URL}{constants.TCIA_API_COLLECTIONS_ENDPOINT}"
            async with session.get(url) as response:
                if not response.ok:
                    raise ValueError(
                        f"TCIA collection request failed ({response.status}): {response.reason}"
                    )
                data = await response.json()
                filtered_data = filter_object_array(data, "Collection", "ICDC-")
                return [obj["Collection"] for obj in filtered_data]
        except Exception as error:
            print(f"Error fetching TCIA collections: {str(error)}")
            raise ValueError(f"TCIA internal server error: {str(error)}")


async def get_tcia_collection_data(collection_id: str) -> Dict[str, Any]:
    """
    Retrieves data from TCIA API for a specific TCIA image collection.
    """
    async with aiohttp.ClientSession() as session:
        try:
            url = f"{constants.TCIA_API_BASE_URL}{constants.TCIA_API_SERIES_ENDPOINT}{collection_id}"
            async with session.get(url) as response:
                if not response.ok:
                    raise ValueError(
                        f"TCIA collection request failed ({response.status}): {response.reason}"
                    )
                return await response.json()
        except Exception as error:
            print(f"Error fetching TCIA collection data: {str(error)}")
            raise ValueError(f"TCIA internal server error: {str(error)}")


async def get_icdc_study_data() -> List[Dict[str, Any]]:
    """
    Retrieves study data from the ICDC backend via a GraphQL query.
    """
    async with aiohttp.ClientSession() as session:
        try:
            query = """
            {
                studiesByProgram {
                    clinical_study_designation
                    numberOfImageCollections
                    numberOfCRDCNodes
                }
            }
            """
            async with session.post(
                constants.BENTO_BACKEND_GRAPHQL_URI, json={"query": query}
            ) as response:
                if not response.ok:
                    raise ValueError(
                        f"ICDC studies request failed ({response.status}): {response.reason}"
                    )
                response_json = await response.json()
                if not response_json.get("data", {}).get("studiesByProgram"):
                    raise ValueError("ICDC response missing required data")
                return response_json["data"]["studiesByProgram"]
        except Exception as error:
            print(f"Error fetching ICDC study data: {str(error)}")
            raise ValueError(f"ICDC internal server error: {str(error)}")


async def get_tcia_collections_data(tcia_collections: List[str]) -> Dict[str, Any]:
    """
    Iterates a list of TCIA collection names and gets corresponding metadata for each collection.
    """
    tasks = [get_tcia_collection_data(collection) for collection in tcia_collections]
    results = await asyncio.gather(*tasks)
    return dict(zip(tcia_collections, results))
