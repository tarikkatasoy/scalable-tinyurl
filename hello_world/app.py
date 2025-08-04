import json
import os
import uuid
import boto3


# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get("TABLE_NAME"))


def lambda_handler(event, context):
   try:
       # Get the long URL from the POST request body
       body = json.loads(event.get("body", "{}"))
       long_url = body.get("long_url")


       if not long_url:
           return {
               "statusCode": 400,
               "body": json.dumps({"error": "long_url is a required field"}),
           }


       # Generate a unique short ID (I will replace this with base62 later)
       short_id = str(uuid.uuid4())[:7]


       # Save the mapping to DynamoDB
       table.put_item(
           Item={
               'id': short_id,
               'long_url': long_url
           }
       )


       # Construct the short URL to return to the user
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
       print(f"Error: {e}")
       return {
           "statusCode": 500,
           "body": json.dumps({"error": "An internal error occurred"}),
       }

