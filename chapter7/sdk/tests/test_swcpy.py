import pytest
from swcpy import SWCClient
from swcpy import SWCConfig
from swcpy.schemas import League, Team, Player, Performance
from io import BytesIO
import pyarrow.parquet as pq
import pandas as pd

def test_health_check():
    """Tests health check from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    response = client.get_health_check()
    assert response.status_code == 200
    assert response.json() == {"message" : "API health check successful"}

def test_list_leagues():
    """Tests get leagues from SDK"""
    config = SWCConfig(swc_base_url="http://0.0.0.0:8000", backoff=False)
    client = SWCClient(config)
    leagues_response = client.list_leagues()
    # Assert the endopoint returned a list object
    assert isinstance(leagues_response, list)
    # Assert each item in the list is an instance of a Pydantic League object
    for league in leagues_response:
        assert isinstance(league, League)
    # Assert that 5 League objects are returned
    assert len(leagues_response) == 5

def test_