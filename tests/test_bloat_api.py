import sys
import os

# Dynamically add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app  # Import your FastAPI app
from utils import fetch_releases, get_release_assets, compute_deltas



client = TestClient(app)

# Mock GitHub API response for releases
MOCK_RELEASES = [
    {
        "tag_name": "v2.8.3",
        "assets": [{"name": "apache_airflow-2.8.3.tar.gz", "size": 12354500}],
    },
    {
        "tag_name": "v2.8.4",
        "assets": [{"name": "apache_airflow-2.8.4.tar.gz", "size": 12354405}],
    },
    {
        "tag_name": "v2.9.0",
        "assets": [{"name": "apache_airflow-2.9.0.tar.gz", "size": 12377995}],
    },
]

@pytest.fixture
def mock_fetch_releases():
    """Mock GitHub API call to fetch releases."""
    with patch("utils.fetch_releases", return_value=MOCK_RELEASES):
        yield

@pytest.fixture
def mock_get_release_assets():
    """Mock function to return release asset sizes."""
    mock_data = {
        "2.8.3": 12354500,
        "2.8.4": 12354405,
        "2.9.0": 12377995,
    }
    
    with patch("apis.bloat_controller.get_release_assets", return_value=mock_data) as mock_func:
        print(f"🚀 Mocking get_release_assets: {mock_data}")
        yield mock_func

@pytest.mark.usefixtures("mock_fetch_releases", "mock_get_release_assets")
def test_bloat_endpoint():
    """Test the /bloat API endpoint."""
    response = client.get("/api/v1/apache/airflow/bloat?start=2.8.3&end=2.9.0")
    assert response.status_code == 200
    data = response.json()
    
    assert "deltas" in data
    assert len(data["deltas"]) > 0
    assert data["deltas"][0]["previous_tag"] == "2.8.3"
    assert data["deltas"][0]["tag"] == "2.8.4"
    assert data["deltas"][0]["delta"] == pytest.approx(0.9999923104941, rel=1e-10)

@pytest.mark.usefixtures("mock_fetch_releases", "mock_get_release_assets")
def test_invalid_version():
    """Test API with an invalid version."""
    response = client.get("/api/v1/apache/airflow/bloat?start=2.8.5&end=2.9.0")
    assert response.status_code == 400
    assert "Invalid start or end version" in response.json()["detail"]


def test_fetch_releases():
    """Unit test for fetch_releases (mocking API call)."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_RELEASES

        releases = fetch_releases("apache", "airflow")
        assert len(releases) == 3
        assert releases[0]["tag_name"] == "v2.8.3"


def test_get_release_assets():
    """Unit test for get_release_assets."""
    result = get_release_assets(MOCK_RELEASES)
    assert result == {
        "2.8.3": 12354500,
        "2.8.4": 12354405,
        "2.9.0": 12377995,
    }


def test_compute_deltas():
    """Unit test for compute_deltas function."""
    version_map = {
        "2.8.3": 12354500,
        "2.8.4": 12354405,
        "2.9.0": 12377995,
    }

    result = compute_deltas(version_map, "2.8.3", "2.9.0")
    assert len(result["deltas"]) == 2
    assert result["deltas"][0]["previous_tag"] == "2.8.3"
    assert result["deltas"][0]["tag"] == "2.8.4"
    assert result["deltas"][0]["delta"] == pytest.approx(0.9999923104941, rel=1e-10)
