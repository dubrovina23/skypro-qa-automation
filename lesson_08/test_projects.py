import os
from uuid import UUID, uuid4

import pytest
import requests


PROJECTS = "https://ru.yougile.com/api-v2/projects"
TIMEOUT = 15


@pytest.fixture
def session():
    with requests.Session() as client:
        yield client


@pytest.fixture
def authorized(session):
    token = os.getenv("YOUGILE_TOKEN")
    if not token:
        pytest.skip("Set YOUGILE_TOKEN to run authenticated tests")
    session.headers["Authorization"] = f"Bearer {token}"
    return session


@pytest.fixture
def create_project(authorized, request):
    def create(title):
        response = authorized.post(
            PROJECTS, json={"title": title}, timeout=TIMEOUT
        )
        response.raise_for_status()
        project_id = str(UUID(response.json()["id"]))

        def remove():
            result = authorized.put(
                f"{PROJECTS}/{project_id}",
                json={"deleted": True},
                timeout=TIMEOUT,
            )
            assert result.status_code == 200, result.text

        request.addfinalizer(remove)
        assert response.status_code == 201, response.text
        return project_id

    return create


def read_project(client, project_id):
    response = client.get(f"{PROJECTS}/{project_id}", timeout=TIMEOUT)
    assert response.status_code == 200, response.text
    return response.json()


def test_create_project(authorized, create_project):
    title = f"Lesson 08 create {uuid4()}"
    project_id = create_project(title)
    project = read_project(authorized, project_id)
    assert project["id"] == project_id
    assert project["title"] == title


def test_update_project(authorized, create_project):
    project_id = create_project(f"Lesson 08 original {uuid4()}")
    title = f"Lesson 08 updated {uuid4()}"
    response = authorized.put(
        f"{PROJECTS}/{project_id}", json={"title": title}, timeout=TIMEOUT
    )
    assert response.status_code == 200, response.text
    assert response.json()["id"] == project_id
    assert read_project(authorized, project_id)["title"] == title


def test_get_project(authorized, create_project):
    title = f"Lesson 08 get {uuid4()}"
    project_id = create_project(title)
    project = read_project(authorized, project_id)
    assert project["id"] == project_id
    assert project["title"] == title


@pytest.mark.parametrize("method", ["POST", "PUT", "GET"])
def test_project_requires_authorization(session, method):
    url = PROJECTS if method == "POST" else f"{PROJECTS}/{uuid4()}"
    payload = None if method == "GET" else {"title": f"Lesson 08 {uuid4()}"}
    response = session.request(method, url, json=payload, timeout=TIMEOUT)
    assert response.status_code == 401, response.text
    assert response.json()["message"] == "Unauthorized"
