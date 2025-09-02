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

def test_should_return_400_when_url_is_missing(apigw_event, mocker):
    """
    Tests that the handler returns a 400 error if the 'url' key is missing from the body.
    """
    # Modify the fixture to have an empty body for this test
    apigw_event["body"] = "{}"
    
    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 400
    assert "error" in data
    assert data["error"] == "No URL found in the request."


def test_should_return_400_when_url_is_invalid(apigw_event, mocker):
    """
    Tests that the handler returns a 400 error if the 'url' value is not a valid URL.
    """
    # Modify the fixture to have an invalid URL for this test
    apigw_event["body"] = '{ "url": "this-is-not-a-url" }'

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 400
    assert "error" in data
    assert data["error"] == "The provided URL is not valid."