import pytest
from httpx import Client


@pytest.fixture
def client():
    """Test client for testing API."""
    http_client = Client(base_url="http://localhost:8001")
    yield http_client
    http_client.close()
