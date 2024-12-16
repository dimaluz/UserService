import json


def publish_event(redis_client, channel, event_data):
    """
    Publish an event in to Redis channel.

    :param redis_client: Redis client.
    :param channel: Channel name.
    :param event_data: Even as a dict.
    """
    try:
        message = json.dumps(event_data)
        redis_client.publish(channel, message)
    except Exception as e:
        raise RuntimeError(f"Error during event publishing: {e}")