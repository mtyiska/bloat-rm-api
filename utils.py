# utils.py

from fastapi import  HTTPException
import requests
import re
import semantic_version
from config.settings import settings

# Function to fetch GitHub releases
def fetch_releases(owner: str, repo: str, github_token: str = None):
    url = f"{settings.GITHUB_API_BASE}/{owner}/{repo}/releases"
    headers = {"Accept": "application/vnd.github.v3+json"}

    if github_token:
        headers["Authorization"] = f"token {github_token}"

    try:
        response = requests.get(url, headers=headers)

        # Check if API call was successful
        if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
            raise HTTPException(status_code=429, detail="GitHub rate limit exceeded. Provide a GitHub token.")

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"GitHub API error: {response.json()}")

        return response.json()

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch releases: {str(e)}")


def get_tarball_size(url):
    """Fetch the size of a tarball by making a HEAD request."""
    try:
        response = requests.head(url, timeout=5)  # Add timeout to avoid hanging
        response.raise_for_status()  # Raise exception for non-200 responses
        size = response.headers.get("Content-Length", None)

        if size is None:
            raise HTTPException(status_code=500, detail=f"Failed to determine tarball size: {url}")

        return int(size)

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tarball size: {str(e)}")



def get_release_assets(releases):
    version_map = {}
    pattern = re.compile(r"apache[-_]airflow-(\d+\.\d+\.\d+).tar.gz")

    for release in releases:
        tag = release.get("tag_name", "").lstrip("v")  # Normalize by removing 'v'
        assets = release.get("assets", [])
        tarball_url = release.get("tarball_url", "")

        found_size = False

        for asset in assets:
            match = pattern.search(asset["name"])
            if match:
                version_map[tag] = asset["size"]
                found_size = True

        if not found_size and tarball_url:
            version_map[tag] = get_tarball_size(tarball_url)

    print(f"📊 Final Version Map: {version_map}")
    return version_map



def is_valid_semver(version):
    """Checks if a version string conforms to semantic versioning."""
    try:
        semantic_version.Version(version)  # Attempt to parse it
        return True
    except ValueError:
        return False

def compute_deltas(version_map, start_version, end_version):
    """
    Compute deltas in version sizes between start_version and end_version.
    Filters out invalid versions (e.g., helm-chart versions).
    """
    # Filter only valid semantic versions
    valid_versions = [v for v in version_map.keys() if is_valid_semver(v)]
    
    # Convert versions to SemanticVersion and sort them
    sorted_versions = sorted(valid_versions, key=lambda v: semantic_version.Version(v))
    
    # Ensure start and end versions exist in the filtered list
    if start_version not in sorted_versions or end_version not in sorted_versions:
        raise HTTPException(status_code=400, detail=f"Invalid start or end version. Available versions: {sorted_versions}")

    filtered_versions = [v for v in sorted_versions if v >= start_version and v <= end_version]

    if not filtered_versions or len(filtered_versions) < 2:
        return {"message": "No deltas found between the selected versions.", "deltas": []}

    deltas = []
    # Iterate over the sorted versions, starting from the second one
    for i in range(1, len(filtered_versions)):  
        prev_tag = filtered_versions[i - 1]  
        curr_tag = filtered_versions[i]     

        prev_size = version_map[prev_tag]
        curr_size = version_map[curr_tag] 

        # Compute the size change ratio (delta). Handle divide by 0 check.
        delta = curr_size / prev_size if prev_size else 1.0
        
        deltas.append({
            "previous_tag": prev_tag, 
            "tag": curr_tag,          
            "delta": round(delta, 10)  
        })


    return {"deltas": deltas}


