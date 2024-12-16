import pytest
import json
import redis
import os
from django.conf import settings

@pytest.fixture
def redis_client():
    """Fixture for Redis connection"""
    # client = settings.REDIS_CLIENT
    client = redis.StrictRedis(
        host=os.environ.get("REDIS_HOST"),
        port=os.environ.get("REDIS_PORT"),
        password=os.environ.get("REDIS_PASSWORD"),
        decode_responses=True,
    )
    
    #Clear the redis before testing
    client.flushdb()
    yield client
    client.close()

@pytest.fixture
def pubsub(redis_client):
    """Fixture for Redis subscribers"""
    pubsub = redis_client.pubsub()
    yield pubsub
    pubsub.close()


def test_publish_message(redis_client):
    """Test for successful message publishing in to Redis channel"""
    channel = "test_channel"
    message = {"event":"test_event", "data":"Test message"}

    #Publish message
    result = redis_client.publish(channel, json.dumps(message))
    
    #Check if the message is published
    assert result == 0


def test_subscribe_and_receive_message(redis_client, pubsub):
    """Test for subscribe and receive message"""
    channel = "test_channel"
    message = {"event":"test_event", "data":"Test message"}

    #Subscribe to the channel
    pubsub.subscribe(channel)

    #Publish a message
    redis_client.publish(channel, json.dumps(message))

    #Check if the message was received
    for msg in pubsub.listen():
        if msg['type'] == 'message':
            receive_message = json.loads(msg['data'])
            assert receive_message['event'] == 'test_event'
            assert receive_message['data'] == 'Test message'
            break


def test_receive_multiple_messages(redis_client, pubsub):
    """Test for subscribe and receive message"""
    channel = "test_channel"
    messages = [
        {'event': 'event_1', 'data': 'Message 1'},
        {'event': 'event_2', 'data': 'Message 2'},
        {'event': 'event_3', 'data': 'Message 3'}
    ]

    #Subscribe to the channel
    pubsub.subscribe(channel)

    #Publish messages
    for message in messages:
        redis_client.publish(channel, json.dumps(message))

    #Check if all messages were received
    receive_messages = []

    for msg in pubsub.listen():
        if msg['type'] == 'message':
            receive_messages.append(json.loads(msg['data']))
        if len(receive_messages) == len(messages):
            break

    assert receive_messages == messages
            