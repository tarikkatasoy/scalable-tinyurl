import os
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get("URL_LOOKUP_TABLE_NAME_DYNAMODB"))

def redirect_handler(event, context):
    logger.info(f"Received event: {event}")

    try:
        short_id = event['pathParameters']['short_id']
        logger.info(f"Looking up short_id: {short_id}")

        response = table.get_item(Key={'id': short_id})
        
        if 'Item' in response:
            long_url = response['Item']['long_url']
            logger.info(f"Found long_url: {long_url}. Redirecting...")
            return {
                'statusCode': 302,
                'headers': {
                    'Location': long_url
                }
            }
        else:
            logger.warning(f"short_id '{short_id}' not found in the database.")
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Short URL not found'})
            }
    except KeyError:
        logger.error("'short_id' not found in pathParameters.")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': "Bad request: 'short_id' missing from path."})
        }
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An internal error occurred'})
        }
