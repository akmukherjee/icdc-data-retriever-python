# tests/test_fetch_data.py
import pytest
from aioresponses import aioresponses
from src.fetch_data import (
    get_idc_collections,
    get_tcia_collections,
    get_icdc_study_data,
    get_tcia_collections_data,
)
from src.constants.data_retrieval import data_retrieval_constants as constants
from src.config import config
from dotenv import load_dotenv
import os

# Load test environment variables
load_dotenv(".env.test")
os.environ["BENTO_BACKEND_GRAPHQL_URI"] = "https://caninecommons.cancer.gov/v1/graphql"


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_get_idc_collections(mock_aioresponse):
    # Mock data
    mock_response = {
        "collections": [
            {"collection_id": "icdc_test1", "name": "Test 1"},
            {"collection_id": "other_test", "name": "Test 2"},
            {"collection_id": "icdc_test2", "name": "Test 3"},
        ]
    }

    # Setup mock
    url = f"{constants.IDC_API_BASE_URL}{constants.IDC_API_COLLECTIONS_ENDPOINT}"
    mock_aioresponse.get(url, payload=mock_response)

    # Execute
    result = await get_idc_collections()

    # Assert
    assert len(result) == 2
    assert all(c["collection_id"].startswith("icdc_") for c in result)


@pytest.mark.asyncio
async def test_get_tcia_collections(mock_aioresponse):
    # Mock data
    mock_response = [
        {"Collection": "ICDC-TEST1"},
        {"Collection": "OTHER-TEST"},
        {"Collection": "ICDC-TEST2"},
    ]

    # Setup mock
    url = f"{constants.TCIA_API_BASE_URL}{constants.TCIA_API_COLLECTIONS_ENDPOINT}"
    mock_aioresponse.get(url, payload=mock_response)

    # Execute
    result = await get_tcia_collections()

    # Assert
    assert len(result) == 2
    assert all(collection.startswith("ICDC-") for collection in result)


@pytest.mark.asyncio
async def test_get_icdc_study_data():
    try:
        # Execute
        result = await get_icdc_study_data()

        # Assert
        assert len(result) > 0
        assert "clinical_study_designation" in result[0]
        assert "numberOfImageCollections" in result[0]
        assert "numberOfCRDCNodes" in result[0]
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        print(f"GraphQL URI: {config.BENTO_BACKEND_GRAPHQL_URI}")
        raise


@pytest.mark.asyncio
async def test_get_tcia_collections_data(mock_aioresponse):
    collection_id = "ICDC-TEST"
    mock_response = {"series": [{"SeriesInstanceUID": "1.2.3", "Modality": "CT"}]}

    # Setup mock
    url = f"{constants.TCIA_API_BASE_URL}{constants.TCIA_API_SERIES_ENDPOINT}{collection_id}"
    mock_aioresponse.get(url, payload=mock_response)

    # Execute
    result = await get_tcia_collections_data(collection_id)

    # Assert
    assert "series" in result
    assert len(result["series"]) == 1
