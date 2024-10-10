from iebank_api import app
import pytest

def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check that the response is valid and returns a status code of 200
    """
    response = testing_client.get('/accounts')  # Sending GET request to fetch accounts
    assert response.status_code == 200  # Checking if status code is 200 (OK)

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN a non-existent '/wrong_path' page is requested (GET)
    THEN check that the response returns a 404 status code (Not Found)
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')  # Sending GET request to a non-existent path
        assert response.status_code == 404  # Verifying 404 Not Found response

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a POST request is made to the '/accounts' endpoint with valid data
    THEN check that the account is created and returns a status code of 201 (Created)
    """
    response = testing_client.post('/accounts', json={
        'name': 'John Doe',
        'currency': '€',
        'country': 'Jordan'  # Adding the country field
    })
    
    assert response.status_code == 201  # Expecting status code 201 for resource creation
    response_data = response.get_json()

    # Checking if the returned data matches the input
    assert response_data['name'] == 'John Doe'
    assert response_data['currency'] == '€'
    assert response_data['country'] == 'Jordan'

def test_create_account_missing_fields(testing_client):
    """
    GIVEN a Flask application
    WHEN a POST request is made to the '/accounts' endpoint without required fields
    THEN check that the response returns a status code of 400 (Bad Request)
    """
    response = testing_client.post('/accounts', json={})
    assert response.status_code == 400
    response_data = response.get_json()
    assert 'error' in response_data
    assert response_data['error'] == 'Missing required fields: name and currency'

def test_create_account_invalid_format(testing_client):
    """
    GIVEN a Flask application
    WHEN a POST request is made to the '/accounts' endpoint with non-JSON body
    THEN check that the response returns a status code of 400 (Bad Request)
    """
    response = testing_client.post('/accounts', data="Invalid body")
    assert response.status_code == 400
    response_data = response.get_json()
    assert 'error' in response_data
    assert response_data['error'] == 'Request must be JSON'

def test_get_account_by_id(testing_client):
    """
    GIVEN a Flask application
    WHEN a GET request is made to fetch an account by ID
    THEN check that the account is returned with the correct data
    """
    create_response = testing_client.post('/accounts', json={
        'name': 'Jane Doe',
        'currency': '$',
        'country': 'USA'
    })
    created_account = create_response.get_json()

    response = testing_client.get(f"/accounts/{created_account['id']}")
    assert response.status_code == 200
    response_data = response.get_json()

    assert response_data['name'] == 'Jane Doe'
    assert response_data['currency'] == '$'
    assert response_data['country'] == 'USA'

def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a PUT request is made to update an existing account
    THEN check that the account is updated and the new data is returned
    """
    create_response = testing_client.post('/accounts', json={
        'name': 'Jane Smith',
        'currency': '€',
        'country': 'France'
    })
    created_account = create_response.get_json()

    update_response = testing_client.put(f"/accounts/{created_account['id']}", json={
        'name': 'Jane Updated'
    })
    assert update_response.status_code == 200

    updated_account = update_response.get_json()
    assert updated_account['name'] == 'Jane Updated'

def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a DELETE request is made to remove an account
    THEN check that the account is deleted and cannot be fetched again
    """
    create_response = testing_client.post('/accounts', json={
        'name': 'John Smith',
        'currency': '£',
        'country': 'UK'
    })
    created_account = create_response.get_json()

    delete_response = testing_client.delete(f"/accounts/{created_account['id']}")
    assert delete_response.status_code == 200

    get_response = testing_client.get(f"/accounts/{created_account['id']}")
    assert get_response.status_code == 404  # Not Found

def test_get_non_existent_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a GET request is made to fetch a non-existent account by ID
    THEN check that the response returns a status code of 404 (Not Found)
    """
    response = testing_client.get('/accounts/99999')  # Non-existent account
    assert response.status_code == 404
