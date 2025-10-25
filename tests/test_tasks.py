# tests/test_tasks.py
import pytest
from fastapi.testclient import TestClient
from app.models import User
from app.database import get_db
from sqlalchemy.orm import Session

BASE_URL = "http://test"


async def register_and_login(client: TestClient, email: str, password: str, db: Session):
    # Register
    response = client.post(
        f"{BASE_URL}/users",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200, f"Registration failed: {response.text}"
    print(f"Registration response: {response.json()}")

    # Verify user in database
    user = db.query(User).filter(User.email == email).first()
    assert user is not None, f"User {email} not found in database after registration"
    print(
        f"User in DB: email={user.email}, hashed_password={user.hashed_password}")

    # Login
    response = client.post(
        f"{BASE_URL}/login",
        data={"username": email, "password": password}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    print(f"Login response: {response.text}")
    token = response.json()["access_token"]
    return f"Bearer {token}"


@pytest.mark.asyncio
async def test_full_task_flow(client: TestClient, db: Session):
    email = "testuser@example.com"
    password = "testpass123"
    token = await register_and_login(client, email, password, db)
    headers = {"Authorization": token}

    # === 1. Create Task ===
    task_data = {"title": "Test Task", "description": "Write tests"}
    response = client.post(f"{BASE_URL}/tasks",
                           json=task_data, headers=headers)
    assert response.status_code == 200, f"Create task failed: {response.text}"
    created_task = response.json()
    task_id = created_task["id"]

    # === 2. Get All Tasks ===
    response = client.get(f"{BASE_URL}/tasks", headers=headers)
    assert response.status_code == 200, f"Get tasks failed: {response.text}"
    tasks = response.json()
    assert len(tasks) == 1

    # === 3. Update Task ===
    update_data = {"completed": True}
    response = client.put(f"{BASE_URL}/tasks/{task_id}",
                          json=update_data, headers=headers)
    assert response.status_code == 200, f"Update task failed: {response.text}"
    assert response.json()["completed"] is True

    # === 4. Delete Task ===
    response = client.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    assert response.status_code == 200, f"Delete task failed: {response.text}"
    assert response.json()["message"] == "Task deleted successfully"

    # === 5. Task Should Be Gone (404) ===
    response = client.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    assert response.status_code == 404, f"Task should not exist: {response.text}"


@pytest.mark.asyncio
async def test_unauthorized_access(client: TestClient):
    response = client.get(f"{BASE_URL}/tasks")
    assert response.status_code == 401, f"Unauthorized access (get) failed: {response.text}"

    response = client.post(f"{BASE_URL}/tasks", json={"title": "No Auth"})
    assert response.status_code == 401, f"Unauthorized access (post) failed: {response.text}"
