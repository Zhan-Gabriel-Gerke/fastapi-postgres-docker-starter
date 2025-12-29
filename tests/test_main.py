import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_return_healthy_check(client):
    response = await client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy", "database": "connected"}