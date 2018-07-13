from utils import (
    as_user_get,
    login_with_form,
    login,
    admin,
    test_user
)
from api.models import User
from api.schemas import user_schema
from api.auth import decrypt_token
# ---------- User API


def test_login(client):
    """ attempt to login as
            * admin
            * test_user('example1')
            * non_exist_user('nonexist')

        target_url: /api/auth/
    """
    resp = login(client, admin['username'], admin['g-recaptcha-response'])
    assert 'Login Successful' in resp['message']
    resp = login(client, test_user['username'],
                 test_user['g-recaptcha-response'])
    assert 'Login Successful' in resp['message']
    resp = login(client, 'notexist', 'notexist')
    assert 'Login Unsuccessful' in resp['message']


def test_login_form(client):
    """ attempt to login as
            * admin
            * test_user('example1')
            * non_exist_user('nonexist')
        with Content-Type: application/x-www-form-urlencoded
        target_url: /api/auth/
    """
    resp = login_with_form(
        client, admin['username'], admin['g-recaptcha-response'])
    assert 'Login Successful' in resp['message']
    resp = login_with_form(
        client, test_user['username'], test_user['g-recaptcha-response'])
    assert 'Login Successful' in resp['message']
    resp = login_with_form(client, 'notexist', 'notexist')
    assert 'Login Unsuccessful' in resp['message']


def test_login_invalid(client):
    """logging in with invalid request params as
            * test_user
        target_url: /api/auth/
    """
    resp = client.post('/auth/', json={
        'username': test_user['username'],
    }, follow_redirects=True)
    assert resp.status_code == 400
    assert 'Invalid request' in resp.get_json()['message']

    resp = client.post('/auth/', json={
        'username': test_user['username'],
        'g-recaptcha-response': test_user['g-recaptcha-response'],
    }, follow_redirects=True, content_type='application/xml')
    assert resp.status_code == 400
    assert 'Unsupported content type' in resp.get_json()['message']


def test_auth_token(client):
    """test vaild token is returned
       1. test: token is contained in response
       2. test: token is vaild

       target_url: /api/auth/
    """
    resp = login(client, admin['username'], admin['g-recaptcha-response'])
    assert 'token' in resp

    token = resp['token']
    with client.application.app_context():
        data = decrypt_token(token)
        user = User.query.filter_by(id=data['data']['user_id']).first()

    assert user is not None


def test_status(client):
    """test it return a vaild response
        1. test: response contains 'id'
        2. test: response matches the data in DB

        auth: required
        target_url: /api/status
    """
    user = test_user
    resp = as_user_get(client, user['username'],
                       user['g-recaptcha-response'], '/api/status')
    assert 'id' in resp.get_json()['status']

    with client.application.app_context():
        db_status = User.query.filter_by(username=user['username']).first()

        assert resp.get_json()['status'] == user_schema.dump(db_status)[0]


def test_status_invaild_header(client):
    """attempt to get status with wrong header.
        this cause error in /api/auth. not in /api/routes/api
        target_url: /api/status
    """
    resp = client.get('/api/status',
                      headers={'Authorization_wrong': 'Bearer no_token_here'})
    assert resp.status_code == 401
    assert 'token_required' in resp.headers['WWW-Authenticate']


def test_status_invaild_auth(client):
    """attempt to get status with wrong auth data.
        this cause error in /api/auth. not in /api/routes/api
        target_url: /api/status
    """
    resp = client.get('/api/status',
                      headers={'Authorization': 'Bearer wrong_token_here'})
    assert resp.status_code == 401
    assert 'invalid_token' in resp.headers['WWW-Authenticate']
