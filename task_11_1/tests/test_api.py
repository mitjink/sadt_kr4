import pytest
from app.main import fake_db

class TestCreateUser:
    def test_create_user_success(self, client):
        user_data = {
            "username": "alice",
            "age": 25,
            "email": "alice@example.com"
        }
        
        response = client.post("/users", json=user_data)
        
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["username"] == "alice"
        assert data["age"] == 25
        assert data["email"] == "alice@example.com"
    
    def test_create_user_duplicate_username(self, client):
        
        client.post("/users", json={
            "username": "bob",
            "age": 30,
            "email": "bob@example.com"
        })

        response = client.post("/users", json={
            "username": "bob", 
            "age": 25,
            "email": "bob2@example.com"
        })
        
        assert response.status_code == 400
        assert "already taken" in response.json()["detail"]
    
    def test_create_user_invalid_age(self, client):
        
        response = client.post("/users", json={
            "username": "charlie",
            "age": 16,
            "email": "charlie@example.com"
        })

        assert response.status_code == 422

class TestGetUser:
    
    def test_get_user_success(self, client):
        create_response = client.post("/users", json={
            "username": "dave",
            "age": 28,
            "email": "dave@example.com"
        })
        user_id = create_response.json()["id"]
        response = client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "dave"
    
    def test_get_user_not_found(self, client):
        
        response = client.get("/users/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_get_user_invalid_id_type(self, client):
        
        response = client.get("/users/abc")

        assert response.status_code == 422

class TestDeleteUser:
    def test_delete_user_success(self, client):
        create_response = client.post("/users", json={
            "username": "eve",
            "age": 22,
            "email": "eve@example.com"
        })
        user_id = create_response.json()["id"]
        
        response = client.delete(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "User deleted successfully"
        assert data["deleted_id"] == user_id
        
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self, client):
        
        response = client.delete("/users/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_delete_twice_same_user(self, client):
        create_response = client.post("/users", json={
            "username": "frank",
            "age": 35,
            "email": "frank@example.com"
        })
        user_id = create_response.json()["id"]
        response1 = client.delete(f"/users/{user_id}")
        assert response1.status_code == 200
        
        response2 = client.delete(f"/users/{user_id}")
        assert response2.status_code == 404

class TestGetAllUsers:
    def test_get_all_users_empty(self, client):
        
        response = client.get("/users")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_users_with_data(self, client):
        
        client.post("/users", json={"username": "user1", "age": 20, "email": "user1@ex.com"})
        client.post("/users", json={"username": "user2", "age": 30, "email": "user2@ex.com"})
        
        response = client.get("/users")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["username"] == "user1"
        assert data[1]["username"] == "user2"