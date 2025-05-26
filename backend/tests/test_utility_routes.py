import pytest
import json

def test_get_timezones(client):
    """Test the /api/timezones endpoint."""
    response = client.get('/api/timezones')

    assert response.status_code == 200
    assert response.content_type == 'application/json'

    timezones = json.loads(response.data)

    assert isinstance(timezones, list)
    assert len(timezones) > 0  # List should not be empty

    # Check for presence of common timezones
    common_timezones_to_check = ['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo']
    for tz in common_timezones_to_check:
        assert tz in timezones, f"{tz} not found in timezone list"

    # Check if the list is sorted
    assert timezones == sorted(timezones), "Timezone list is not sorted alphabetically"

    # Optional: Check a few specific known timezones to ensure they are IANA format
    # This is somewhat redundant if zoneinfo.available_timezones() is trusted,
    # but can catch unexpected formatting issues.
    assert 'Etc/GMT+1' in timezones # Example of an Etc timezone
    assert 'Pacific/Honolulu' in timezones # Example of a Pacific timezone
    assert 'Australia/Sydney' in timezones # Example of an Australian timezone
