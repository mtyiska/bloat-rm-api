# apis/bloat_controller.py
from fastapi import APIRouter, HTTPException, Path, Query, Header
from pydantic import BaseModel
from typing import List
from utils import fetch_releases, get_release_assets, compute_deltas


router = APIRouter()

class Delta(BaseModel):
    previous_tag: str
    tag: str
    delta: float

class BloatResponse(BaseModel):
    deltas: List[Delta]


# API Endpoint
@router.get("/{owner}/{repo}/bloat", response_model=BloatResponse)
def get_bloat(
    owner: str = Path(..., description="GitHub owner", example="apache"),
    repo: str = Path(..., description="GitHub repository", example="airflow"),
    start: str = Query("2.8.3", description="Start version", example="2.8.3"),
    end: str = Query("2.9.2", description="End version", example="2.9.2"),
    github_token: str = Header(None, description="Optional GitHub token")
):
    """
    Fetch release sizes and compute bloat between start and end versions.
    Users can provide a GitHub token in the request header for increased rate limits.
    """

    releases = fetch_releases(owner, repo, github_token)
    version_map = get_release_assets(releases)

    # Ensure version comparison works correctly (strip 'v' only if present)
    start_version = start.lstrip("v") if start.startswith("v") else start
    end_version = end.lstrip("v") if end.startswith("v") else end

    # Ensures that start and end versions exist in the available releases.
    available_versions = [v.lstrip("v") for v in version_map.keys()]

    if start_version not in available_versions or end_version not in available_versions:
        raise HTTPException(status_code=400, detail=f"Invalid start or end version. Available versions: {list(version_map.keys())}")

    return compute_deltas(version_map, start_version, end_version)
