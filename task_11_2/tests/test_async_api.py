import pytest
from faker import Faker
fake = Faker()

class TestCreateUser:
    
    @pytest.mark.anyio
    async def test_create_user_success(self, client, faker_instance):
        user_data = {
            "username": faker_instance.user_name(), 
            "age": faker_instance.random_int(min=18, max=99),
            "email": faker_instance.email() 
        }
        
        response = await client.post("/users", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["age"] == user_data["age"]
        assert data["email"] == user_data["email"]
        assert "id" in data
    
    @pytest.mark.anyio
    async def test_create_user_duplicate(self, client):
        fixed_username = fake.user_name()
        
        user1 = {
            "username": fixed_username,
            "age": 25,
            "email": fake.email()
        }
        await client.post("/users", json=user1)
        
        user2 = {
            "username": fixed_username,
            "age": 30,
            "email": fake.email()
        }
        response = await client.post("/users", json=user2)
        
        assert response.status_code == 400
        assert "already taken" in response.json()["detail"]
    
    @pytest.mark.anyio
    async def test_create_user_invalid_age(self, client):
        user_data = {
            "username": fake.user_name(),
            "age": 16,
            "email": fake.email()
        }
        
        response = await client.post("/users", json=user_data)
        assert response.status_code == 422

class TestGetUser:
    @pytest.mark.anyio
    async def test_get_user_success(self, client):
        create_response = await client.post("/users", json={
            "username": fake.user_name(),
            "age": 30,
            "email": fake.email()
        })
        user_id = create_response.json()["id"]
        
        response = await client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
    
    @pytest.mark.anyio
    async def test_get_user_not_found(self, client):
        response = await client.get("/users/99999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    @pytest.mark.anyio
    async def test_get_user_invalid_id_type(self, client):
        response = await client.get("/users/abc")
        
        assert response.status_code == 422

class TestDeleteUser:
    
    @pytest.mark.anyio
    async def test_delete_user_success(self, client):

        create_response = await client.post("/users", json={
            "username": fake.user_name(),
            "age": 25,
            "email": fake.email()
        })
        user_id = create_response.json()["id"]
        
        response = await client.delete(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "User deleted"
        assert data["deleted_id"] == user_id
        
        get_response = await client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
    
    @pytest.mark.anyio
    async def test_delete_user_not_found(self, client):
        response = await client.delete("/users/99999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

class TestParameterized:
    
    @pytest.mark.anyio
    @pytest.mark.parametrize("age,expected_status", [
        (18, 201),
        (19, 201),
        (17, 422),
        (25, 201), 
        (99, 201), 
        (-5, 422), 
    ])
    async def test_different_ages(self, client, age, expected_status):
        user_data = {
            "username": fake.user_name(),
            "age": age,
            "email": fake.email()
        }
        
        response = await client.post("/users", json=user_data)
        assert response.status_code == expected_status

class TestGetAllUsers:
    
    @pytest.mark.anyio
    async def test_get_all_users_empty(self, client):
        
        response = await client.get("/users")
        
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.anyio
    async def test_get_all_users_with_data(self, client):
        created_ids = []
        for _ in range(3):
            resp = await client.post("/users", json={
                "username": fake.user_name(),
                "age": fake.random_int(min=18, max=99),
                "email": fake.email()
            })
            created_ids.append(resp.json()["id"])
        
        response = await client.get("/users")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        returned_ids = [user["id"] for user in data]
        for user_id in created_ids:
            assert user_id in returned_ids