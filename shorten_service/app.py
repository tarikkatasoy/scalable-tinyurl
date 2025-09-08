import json
import os
import uuid
import boto3
import logging
import validators
from decimal import Decimal

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def to_base62(num):
    """Converts a positive integer to a Base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    
    base62_str = ""
    num = int(num) 
    while num > 0:
        num, rem = divmod(num, 62)
        base62_str = BASE62_ALPHABET[rem] + base62_str
    return base62_str

logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource('dynamodb')
short_url_table = dynamodb.Table(os.environ.get("URL_LOOKUP_TABLE_NAME_DYNAMODB"))


def lambda_handler(event, context):
   logger.info(f"Received event: {event}")

   try:

       body = json.loads(event.get("body", "{}"))
       long_url = body.get("url")

       if not long_url:
           logger.error("Validation Error: The 'long_url' field was not found in the request body.")

           return {
               "statusCode": 400,
                "body": json.dumps({"error": "No URL found in the request."}),
           }
       if not validators.url(long_url):
           logger.error(f"Validation Error: The provided URL is not valid. URL: '{long_url}'")
           return {
               "statusCode": 400,
               "body": json.dumps({"error": "The provided URL is not valid."}),
           }


       response = short_url_table.update_item(
           Key={'id': 'counter'},
           UpdateExpression='ADD url_count :val',
           ExpressionAttributeValues={':val': Decimal(1)}, # Use Decimal for the counter
           ReturnValues="UPDATED_NEW"
       )
       counter_value = response['Attributes']['url_count']

       short_id = to_base62(counter_value)
 
       item_to_save = {
           'id': short_id,
           'long_url': long_url
       }
       
       logger.info(f"Saving new item to DynamoDB: {item_to_save}")
 
       short_url_table.put_item(
           Item=item_to_save
       )

       short_url = f"https://tariksurl.com/{short_id}"


       return {
           "statusCode": 200,
           "body": json.dumps({
               "short_url": short_url,
               "long_url": long_url
           }),
       }
   except Exception as e:
       logger.error(f"An unexpected error occurred: {e}")
       return {
           "statusCode": 500,
           "body": json.dumps({"error": "An internal error occurred"}),
       }
   