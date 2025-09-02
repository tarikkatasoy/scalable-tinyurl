import json
import os
import uuid
import boto3
import logging
import validators

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


       # TODO (tarik): Replace this with base62 logic
       short_id = uuid.uuid4().hex[:7]


 
       item_to_save = {
           'id': short_id,
           'long_url': long_url
       }
       
       logger.info(f"Saving new item to DynamoDB: {item_to_save}")
 
       short_url_table.put_item(
           Item=item_to_save
       )

       api_gateway_url = f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}"
       short_url = f"{api_gateway_url}/{short_id}"


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
   