"""
Test suite for Mergington High School Activities API
Uses AAA (Arrange-Act-Assert) pattern for test structure
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_success(self):
        """Test that GET /activities returns 200 status code"""
        # Arrange
        # (No setup needed for this endpoint)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_required_fields(self):
        """Test that activities contain required fields"""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert len(activities) > 0
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            for field in required_fields:
                assert field in activity_data


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_for_valid_activity_returns_success(self):
        """Test successful signup for an existing activity"""
        # Arrange
        email = "test.student@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_for_nonexistent_activity_returns_404(self):
        """Test signup for non-existent activity returns 404"""
        # Arrange
        email = "test.student@mergington.edu"
        activity = "Nonexistent Club"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_duplicate_signup_returns_400(self):
        """Test that signing up twice returns 400 error"""
        # Arrange
        email = "duplicate.test@mergington.edu"
        activity = "Programming Class"

        # Act - First signup
        response1 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Act - Duplicate signup attempt
        response2 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_valid_participant_returns_success(self):
        """Test successful unregistration of a participant"""
        # Arrange
        email = "unregister.test@mergington.edu"
        activity = "Gym Class"
        # First, sign them up
        client.post(f"/activities/{activity}/signup?email={email}")

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_unregister_nonexistent_activity_returns_404(self):
        """Test unregister from non-existent activity returns 404"""
        # Arrange
        email = "test@mergington.edu"
        activity = "Nonexistent Club"

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_nonparticipant_returns_400(self):
        """Test unregister of non-registered student returns 400"""
        # Arrange
        email = "notregistered@mergington.edu"
        activity = "Debate Club"

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
