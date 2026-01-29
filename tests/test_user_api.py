import pytest

@pytest.mark.asyncio
async def test_create_user_api(client):
    response = await client.post(
        '/v1/user',
        json={
            "name":"Santosh",
            "email":"santosh@gmail.com",
            "password":"admin"
        }
    )

    assert response.status_code == 200
    data = response.json()                          # In httpx: response.json() is synchronous
    assert data['email'] == "santosh@gmail.com"
