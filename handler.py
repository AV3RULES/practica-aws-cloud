import boto3
import json
import os
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone

ads_table = boto3.resource('dynamodb').Table(os.environ.get('DYNAMODB_ADS_TABLE'))

def get_comments(event, context):
    """Return all the comments of an ad
    :param ad_id: (path parameter) ID of the ad
    :type ad_id: str
    :rtype: dict
        return example:
        {
            "comments": [
                {   "timestamp": "timestamp",   "user"": "Sir Author the first",   "text": "I bought this product and It is amazing"   },
                ...
            ]
        }
    """
    ad_id = event.get('pathParameters', {}).get('ad_id')
    comments = ads_table.query(KeyConditionExpression=Key('ad_id').eq(ad_id))
    if "Items" in comments:
        body = {
            "status": 200,
            'comments': [ {'timestamp': comment['timestamp'], 'user': comment['user'], 'text': comment['text']} for comment in comments["Items"] ],
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
    else:
        body = {
            "status": 404,
            "title": "comments not found",
            "detail": f"There are no comments for ad {ad_id}",
        }
        response = {
            "statusCode": 404,
            "body": json.dumps(body)
        }
    return response


def send_message(event, context):
    """Send a message into a chat room
    :param chat_id: (path parameter) ID of the chat
    :type chat_id: str
    :param message: (body) new info
    :type message: dict
        message example:
        {
            "user_id": "user ID of the author",
            "text": "content written by the user",
        }
    :rtype: SimpleResponse
    """
    chat_id = event.get('pathParameters', {}).get('chat_id')
    message = json.loads(event.get('body', '{}'))
    messages_table.put_item(
        Item={
            'chat_id': chat_id,
            'ts': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            'user_id': message['user_id'],
            'text': message['text'],
        }
    )
    body = {
        "status": 201,
        "title": "OK",
        "detail": f"New message posted into chat {chat_id}",
    }
    return {
        "statusCode": 201,
        "body": json.dumps(body)
    }