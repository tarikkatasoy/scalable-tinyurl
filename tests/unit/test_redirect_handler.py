import json
import os
import pytest
from unittest.mock import MagicMock

# Set a mock environment variable for the test session
os.environ['URL_LOOKUP_TABLE_NAME_DYNAMODB'] = 'mock-table'
    
from redirect_service import app

def test_redirect_handler_happy_path(mocker):
    """Verifies a 302 redirect is returned for a valid short_id."""
    # Mock the DynamoDB table to simulate finding an item
    mock_table = MagicMock()
    mock_table.get_item.return_value = {
        'Item': {
            'id': 'a1b2c3d',
            'long_url': 'https://www.example.com'
        }
    }
    # Correctly patch the 'table' object in the redirect_service's app module
    mocker.patch.object(app, 'table', mock_table)

    event = {'pathParameters': {'short_id': 'a1b2c3d'}}
    
    ret = app.redirect_handler(event, "")

    assert ret['statusCode'] == 302
    assert ret['headers']['Location'] == 'https://www.example.com'

def test_redirect_handler_not_found(mocker):
    """Verifies a 404 is returned for a short_id that does not exist."""
    mock_table = MagicMock()
    # Simulate the case where get_item finds nothing
    mock_table.get_item.return_value = {}
    # Correctly patch the 'table' object in the redirect_service's app module
    mocker.patch.object(app, 'table', mock_table)

    event = {'pathParameters': {'short_id': 'nonexistent'}}

    ret = app.redirect_handler(event, "")

    assert ret['statusCode'] == 404
