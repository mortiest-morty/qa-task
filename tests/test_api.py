import os
import uuid

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

API_URL = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


@pytest.mark.skipif(
    not all(
        [
            GITHUB_USERNAME,
            GITHUB_TOKEN,
            GITHUB_REPOSITORY,
        ]
    ),
    reason="GitHub environment variables are not configured",
)
def test_create_verify_delete_repository():
    repository_name = f"{GITHUB_REPOSITORY}-{uuid.uuid4().hex[:8]}"
    repository_url = (
        f"{API_URL}/repos/{GITHUB_USERNAME}/{repository_name}"
    )

    created = False

    try:
        create_response = requests.post(
            f"{API_URL}/user/repos",
            headers=HEADERS,
            json={
                "name": repository_name,
                "description": "Temporary repository for QA test task",
                "private": False,
                "auto_init": False,
            },
            timeout=30,
        )

        assert create_response.status_code == 201, (
            f"Repository creation failed: "
            f"{create_response.status_code} {create_response.text}"
        )
        created = True

        list_response = requests.get(
            f"{API_URL}/user/repos",
            headers=HEADERS,
            params={
                "per_page": 100,
                "type": "owner",
            },
            timeout=30,
        )

        assert list_response.status_code == 200, (
            f"Repository list request failed: "
            f"{list_response.status_code} {list_response.text}"
        )

        repositories = list_response.json()
        repository_names = {
            repository["name"] for repository in repositories
        }

        assert repository_name in repository_names

        get_response = requests.get(
            repository_url,
            headers=HEADERS,
            timeout=30,
        )

        assert get_response.status_code == 200
        assert get_response.json()["private"] is False

    finally:
        if created:
            delete_response = requests.delete(
                repository_url,
                headers=HEADERS,
                timeout=30,
            )

            assert delete_response.status_code == 204, (
                f"Repository deletion failed: "
                f"{delete_response.status_code} "
                f"{delete_response.text}"
            )