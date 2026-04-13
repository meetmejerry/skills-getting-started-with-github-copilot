import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    """Test retrieving all activities"""
    # Arrange
    # No special setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success():
    """Test successful signup for an activity"""
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Programming Class/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]

    # Verify the participant was added
    response2 = client.get("/activities")
    data = response2.json()
    assert email in data["Programming Class"]["participants"]


def test_signup_activity_not_found():
    """Test signup for non-existent activity"""
    # Arrange
    email = "test@mergington.edu"

    # Act
    response = client.post("/activities/NonExistent Activity/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_signup_duplicate_activity():
    """Test that a student cannot sign up for multiple activities"""
    # Arrange
    email = "duplicate@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})  # First signup

    # Act
    response = client.post("/activities/Programming Class/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up for an activity" in result["detail"]


def test_unregister_success():
    """Test successful unregistration from an activity"""
    # Arrange
    email = "unregister@mergington.edu"
    client.post("/activities/Gym Class/signup", params={"email": email})  # Sign up first

    # Act
    response = client.delete(f"/activities/Gym Class/participants/{email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]

    # Verify removed
    response2 = client.get("/activities")
    data = response2.json()
    assert email not in data["Gym Class"]["participants"]


def test_unregister_activity_not_found():
    """Test unregister from non-existent activity"""
    # Arrange
    # No setup

    # Act
    response = client.delete("/activities/NonExistent Activity/participants/test@mergington.edu")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_unregister_participant_not_found():
    """Test unregister non-existent participant"""
    # Arrange
    # No setup

    # Act
    response = client.delete("/activities/Chess Club/participants/nonexistent@mergington.edu")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Participant not found" in result["detail"]


def test_root_redirect():
    """Test root endpoint redirects to static index"""
    # Arrange
    # No setup

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200  # TestClient follows redirects
    assert "Mergington High School" in response.text
