import json
import os
import pytest
from unittest.mock import MagicMock

# Set the environment variable before importing the app
os.environ['URL_LOOKUP_TABLE_NAME_DYNAMODB'] = 'mock-table'

# Now we can import from the correctly named folder
from shorten_service import app

@pytest.fixture()
def apigw_event():
    """ Generates a sample API GW Event for a POST /shorten request """
    return {
        "body": '{ "url": "https://www.example.com"}',
        "requestContext": {
            "stage": "Prod",
            "domainName": "test.execute-api.us-east-1.amazonaws.com"
        },
        "httpMethod": "POST",
        "path": "/shorten",
    }

def test_lambda_handler(apigw_event, mocker):
    """ Tests that the lambda_handler successfully processes a valid request """
    # Mock the DynamoDB table and its put_item method
    mock_table = MagicMock()
    mocker.patch.object(app, 'short_url_table', mock_table)

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    mock_table.put_item.assert_called_once()
    assert "short_url" in data
    assert data["long_url"] == "https://www.example.com"