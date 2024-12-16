import pytest
import json
from unittest.mock import MagicMock

from event_bus.publishers import publish_event


@pytest.fixture
def redis_client(mocker):
    """Mock Redis client"""
    mock_redis = mocker.Mock()
    mock_redis.publish = MagicMock(return_value=1)
    return mock_redis


def test_publish_event(redis_client):
    """Test of publish event"""
    channel = "user_registered"
    event_data = {"event": "user_registered", "data": {"user_id": 1}}

    # Publish event 
    publish_event(redis_client, channel, event_data)

    # Check, if the message was sent to the right channel
    redis_client.publish.assert_called_once_with(channel, json.dumps(event_data))