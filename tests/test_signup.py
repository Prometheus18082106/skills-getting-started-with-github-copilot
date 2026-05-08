"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA (Arrange-Act-Assert) pattern
"""

import pytest
from urllib.parse import quote


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful_adds_participant(self, client):
        """
        Arrange: Prepare new email and activity name
        Act: Make POST request to signup
        Assert: Verify participant is added to activity
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "alex@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity_name in result["message"]

    def test_signup_successful_response_message(self, client):
        """
        Arrange: Set up signup request details
        Act: Sign up participant
        Assert: Verify success message format
        """
        # Arrange
        activity_name = "Soccer Club"
        email = "jordan@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["message"] == f"Signed up {email} for {activity_name}"

    def test_signup_activity_not_found_returns_404(self, client):
        """
        Arrange: Prepare non-existent activity name
        Act: Make POST request with invalid activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        invalid_activity = "Nonexistent Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{quote(invalid_activity)}/signup?email={quote(email)}"
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()

    def test_signup_duplicate_signup_returns_400(self, client):
        """
        Arrange: Attempt to signup same email twice for same activity
        Act: Make first signup request, then make duplicate request
        Assert: Second request returns 400 Bad Request error
        """
        # Arrange
        activity_name = "Art Club"
        email = "maya@mergington.edu"
        
        # Act - First signup
        first_response = client.post(
            f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
        )
        
        # Act - Duplicate signup
        duplicate_response = client.post(
            f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
        )
        
        # Assert
        assert first_response.status_code == 200
        assert duplicate_response.status_code == 400
        duplicate_result = duplicate_response.json()
        assert "detail" in duplicate_result
        assert "already signed up" in duplicate_result["detail"].lower()

    def test_signup_to_different_activities_allowed(self, client):
        """
        Arrange: Prepare email and multiple activity names
        Act: Sign up same email to different activities
        Assert: Both signups succeed
        """
        # Arrange
        email = "charlie@mergington.edu"
        activity_1 = "Drama Club"
        activity_2 = "Debate Club"
        
        # Act - Sign up to first activity
        response_1 = client.post(
            f"/activities/{quote(activity_1)}/signup?email={quote(email)}"
        )
        
        # Act - Sign up to second activity
        response_2 = client.post(
            f"/activities/{quote(activity_2)}/signup?email={quote(email)}"
        )
        
        # Assert
        assert response_1.status_code == 200
        assert response_2.status_code == 200
        assert email in response_1.json()["message"]
        assert email in response_2.json()["message"]

    def test_signup_multiple_users_same_activity(self, client):
        """
        Arrange: Prepare multiple emails for same activity
        Act: Sign up multiple different emails to same activity
        Assert: All signups succeed
        """
        # Arrange
        activity_name = "Science Club"
        emails = ["leo@mergington.edu", "ava@mergington.edu", "noah@mergington.edu"]
        
        # Act & Assert
        for email in emails:
            response = client.post(
                f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
            )
            assert response.status_code == 200
            assert email in response.json()["message"]

