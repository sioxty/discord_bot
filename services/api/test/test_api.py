import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app import app

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as ac:
        yield ac

@pytest.mark.asyncio
async def test_get_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_get_items(client: AsyncClient):
    user_id = 1
    response = await client.get(f"/users/{user_id}/playlists/")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id}

@pytest.mark.asyncio
async def test_add_user(client: AsyncClient):
    data = {
        "user_id": 1,
        "favorite_tracks": [],
        "playlists": []
    }
    response = await client.post("/users/add", json=data)
    assert response.status_code == 200
    assert response.json() == data

@pytest.mark.asyncio
async def test_add_user_full(client: AsyncClient):
    data = {
        "user_id": 1,
        "favorite_tracks": [],
        "playlists": [
            
        ]
    }
    response = await client.post("/users/add", json=data)
    assert response.status_code == 200
    assert response.json() == data


    response = await client.post("/users/add", json=data)