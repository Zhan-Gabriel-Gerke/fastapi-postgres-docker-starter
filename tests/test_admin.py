import pytest
from fastapi import status
from app.models import Todos
from sqlalchemy import select

@pytest.mark.asyncio
async def test_admin_read_all_authenticated(admin_client, test_todo):
    response = await admin_client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday!', 'id': test_todo.id,
                                'priority': 5, 'owner_id': test_todo.owner_id}]

@pytest.mark.asyncio
async def test_admin_delete_todo(admin_client, test_todo, async_db):
    response = await admin_client.delete(f"/admin/todo/{test_todo.id}")
    assert response.status_code == 204

    result = await async_db.execute(select(Todos).filter(Todos.id == test_todo.id))
    model = result.scalars().first()
    assert model is None

@pytest.mark.asyncio
async def test_admin_delete_todo_not_found(admin_client):
    response = await admin_client.delete("/admin/todo/9999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}