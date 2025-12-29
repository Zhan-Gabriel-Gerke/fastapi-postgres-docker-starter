import pytest
from fastapi import status
from app.models import Todos
from sqlalchemy import select

@pytest.mark.asyncio
async def test_read_all_authenticated(authenticated_client, test_todo):
    response = await authenticated_client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday!', 'id': test_todo.id,
                                'priority': 5, 'owner_id': test_todo.owner_id}]


@pytest.mark.asyncio
async def test_read_one_authenticated(authenticated_client, test_todo):
    response = await authenticated_client.get(f"/todos/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday!', 'id': test_todo.id,
                                'priority': 5, 'owner_id': test_todo.owner_id}

@pytest.mark.asyncio
async def test_read_one_authenticated_not_found(authenticated_client):
    response = await authenticated_client.get("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}

@pytest.mark.asyncio
async def test_create_todo(authenticated_client, async_db):
    request_data={
        'title': 'New Todo!',
        'description':'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = await authenticated_client.post('/todos/todo', json=request_data)
    assert response.status_code == 201

    result = await async_db.execute(select(Todos).filter(Todos.title == request_data.get('title')))
    model = result.scalars().first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

@pytest.mark.asyncio
async def test_update_todo(authenticated_client, test_todo, async_db):
    request_data={
        'title':'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    response = await authenticated_client.put(f'/todos/todo/{test_todo.id}', json=request_data)
    assert response.status_code == 204
    
    result = await async_db.execute(select(Todos).filter(Todos.id == test_todo.id))
    model = result.scalars().first()
    assert model.title == 'Change the title of the todo already saved!'

@pytest.mark.asyncio
async def test_update_todo_not_found(authenticated_client):
    request_data={
        'title':'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    response = await authenticated_client.put('/todos/todo/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}

@pytest.mark.asyncio
async def test_delete_todo(authenticated_client, test_todo, async_db):
    response = await authenticated_client.delete(f'/todos/todo/{test_todo.id}')
    assert response.status_code == 204
    
    result = await async_db.execute(select(Todos).filter(Todos.id == test_todo.id))
    model = result.scalars().first()
    assert model is None

@pytest.mark.asyncio
async def test_delete_todo_not_found(authenticated_client):
    response = await authenticated_client.delete('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}