"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Set up client
        Act: Make GET request to /activities
        Assert: Verify response contains all 9 activities
        """
        # Arrange
        expected_activity_count = 9
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == expected_activity_count
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Basketball Team" in data

    def test_get_activities_response_structure(self, client):
        """
        Arrange: Define expected keys for activity object
        Act: Get activities and inspect first activity
        Assert: Verify activity has correct structure
        """
        # Arrange
        required_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        first_activity = activities_data["Chess Club"]
        
        # Assert
        assert response.status_code == 200
        assert set(first_activity.keys()) == required_keys
        assert isinstance(first_activity["participants"], list)
        assert isinstance(first_activity["max_participants"], int)
        assert isinstance(first_activity["description"], str)
        assert isinstance(first_activity["schedule"], str)

    def test_get_activities_participants_data(self, client):
        """
        Arrange: Provide expected participants for activities with existing signups
        Act: Fetch activities and check participants
        Assert: Verify participant data matches expected values
        """
        # Arrange
        expected_chess_club_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        expected_programming_participants = ["emma@mergington.edu", "sophia@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert activities_data["Chess Club"]["participants"] == expected_chess_club_participants
        assert activities_data["Programming Class"]["participants"] == expected_programming_participants
        assert activities_data["Basketball Team"]["participants"] == []
        assert activities_data["Soccer Club"]["participants"] == []

    def test_get_activities_max_participants(self, client):
        """
        Arrange: Define expected capacity for activities
        Act: Fetch activities
        Assert: Verify max_participants values are correct
        """
        # Arrange
        expected_capacities = {
            "Chess Club": 12,
            "Basketball Team": 15,
            "Soccer Club": 22,
            "Gym Class": 30
        }
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, expected_capacity in expected_capacities.items():
            assert activities_data[activity_name]["max_participants"] == expected_capacity
