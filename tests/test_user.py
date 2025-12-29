import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_return_user(user_client, test_user):
    response = await user_client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codingwithrobytest'
    assert response.json()['email'] == 'codingwithrobytest@email.com'
    assert response.json()['first_name'] == 'Eric'
    assert response.json()['last_name'] == 'Roby'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-1111'


@pytest.mark.asyncio
async def test_change_password_success(user_client, test_user):
    response = await user_client.put("/users/password", json={"password": "testpassword",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_change_password_invalid_current_password(user_client, test_user):
    response = await user_client.put("/users/password", json={"password": "wrong_password",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}


@pytest.mark.asyncio
async def test_change_phone_number_success(user_client, test_user):
    response = await user_client.put("/users/phone_number", json={"password": "testpassword",
                                                       "new_phone_number": "(222)-222-2222"})
    assert response.status_code == status.HTTP_204_NO_CONTENT