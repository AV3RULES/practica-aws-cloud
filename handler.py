import boto3
import json
import os
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone

ads_table = boto3.resource('dynamodb').Table(os.environ.get('DYNAMODB_ADS_TABLE'))

def get_ads(event, context):
    """Return all the ads
    :rtype: dict
        return example:
        {
            "ads": [
                {
                    "ad_id": "e25721ef-f83e-4a67-825d-f00c5de97ae5",
                    "title": "VX500 300Hz PLA exchangeable"
                },
                {
                    "ad_id": "ddd7f744-ab40-4b46-8dda-dad9c09caa4c",
                    "title": "New mobile videogame available"
                }
                ...
            ]
        }
    """
    ads = ads_table.scan()

    if "Items" in ads:
        body = {
            'ads': [ {'ad_id': ad['ad_id'], 'title': ad['title']} for ad in ads["Items"] ],
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
    else:
        body = {
            "title": "Ads not found",
            "detail": "Ads table must be empty",
        }
        response = {
            "statusCode": 404,
            "body": json.dumps(body)
        }
    return response

def get_add(event, context):
    """Return an details ad given id
    :param ad_id: (path parameter) ID of the ad
    :type ad_id: str
    :rtype: dict
        return example:
        {
            "ad_id": "e25721ef-f83e-4a67-825d-f00c5de97ae5",
            "title": "VX500 300Hz PLA exchangeable",
            "description": "orem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "image": "http://s3-us-east-1.amazonaws.com/bucket/img1.png"
        }
    """
    ad_id = event.get('pathParameters', {}).get('ad_id')
    ad = ads_table.query(KeyConditionExpression=Key('ad_id').eq(ad_id))
    if "Items" in ad:
        response = {
            "statusCode": 200,
            "body": json.dumps(ad)
        }
    else:
        body = {
            "title": "ad not found",
            "detail": f"There is no ad for this id {ad_id}"
        }
        response = {
            "statusCode": 404,
            "body": json.dumps(body)
        }
    return response

def publish_ad(event, context):
    """publish an ad
    :param ad_id: (path parameter) ID of the ad
    :type ad_id: str
    :param comment: (body) new ad info
    :type comment: dict
        comment example:
        {
            "ad_id": "e25721ef-f83e-4a67-825d-f00c5de97ae5",
            "title": "VX500 300Hz PLA exchangeable",
            "description": "orem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "image": "http://s3-us-east-1.amazonaws.com/bucket/img1.png",
            "comments": []
        }
    :rtype: SimpleResponse
    """
    ad_id = event.get('pathParameters', {}).get('ad_id')
    ad = json.loads(event.get('body', '{}'))
    ads_table.put_item(ad)
    body = {
        "title": "Created",
        "detail": f"New comment posted into ad {ad_id}"
    }
    return {
        "statusCode": 201,
        "body": json.dumps(body)
    }

def get_comments(event, context):
    """Return all the comments of an ad given id
    :param ad_id: (path parameter) ID of the ad
    :type ad_id: str
    :rtype: dict
        return example:
        {
            "comments": [
                {   "timestamp": "timestamp",   "user"": "Sir Author the first",   "text": "I bought this product and It is amazing"   },
                {   "timestamp": "timestamp",   "user"": "Author II",   "text": "Good product for this price"   },
                ...
            ]
        }
    """
    ad_id = event.get('pathParameters', {}).get('ad_id')
    ad = ads_table.query(KeyConditionExpression=Key('ad_id').eq(ad_id))
    if "Items" in ad:
        body = {
            'comments': [ {ad['comments']} ]
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
    else:
        body = {
            "title": "comments not found",
            "detail": f"There are no comments for ad {ad_id}"
        }
        response = {
            "statusCode": 404,
            "body": json.dumps(body)
        }
    return response


def send_comment(event, context):
    """Send a comment into an ad
    :param ad_id: (path parameter) ID of the ad
    :type ad_id: str
    :param comment: (body) new comment
    :type comment: dict
        comment example:
        {
            "user": "author of the comment",
            "text": "content written by the user",
        }
    :rtype: SimpleResponse
    """
    ad_id = event.get('pathParameters', {}).get('ad_id')
    comment = json.loads(event.get('body', '{}'))
    new_comment = {
        'user': comment['user'],
        'timestamp': datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        "text": comment['text'],
    }
    ad = ads_table.query(KeyConditionExpression=Key('ad_id').eq(ad_id))
    ad['comments'] += comment
    ads_table.update_item(
        Key={
            'id': ad_id
        },
        AttributeUpdates={
            'comments': ad['comments'],
        }
    )
    body = {
        "title": "Created",
        "detail": f"New comment posted into ad {ad_id}"
    }
    return {
        "statusCode": 201,
        "body": json.dumps(body)
    }