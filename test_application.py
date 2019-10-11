import json
import pytest
from application import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_decryptMessage(client):
    message = """-----BEGIN PGP MESSAGE-----
    Version: GnuPG v2
    jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
    pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
    =KvJQ
    -----END PGP MESSAGE-----"""
    passphrase = "topsecret"
    response = client.post('/decryptMessage', data=json.dumps(dict(message=str(message), passphrase=passphrase)),
                           content_type='application/json')
    assert "Nice work!" == response.get_json()['DecryptedMessage']


def test_decryptMessageWrongPass(client):
    message = """-----BEGIN PGP MESSAGE-----
Version: GnuPG v2
jA0ECQMCVady3RUyJw3X0kcBF+zdkfZOMhISoYBRwR3uk3vNv+TEg+rJnp4/yYIS
pEoI2S82cDiCNBIVAYWB8WKPtH2R2YSussKhpSJ4mFgqyOA01uwroA==
=KvJQ
-----END PGP MESSAGE-----"""
    passphrase = 'ratttleeed'
    response = client.post('/decryptMessage', data=json.dumps(dict(message=str(message), passphrase=passphrase)),
                           content_type='application/json')

    assert "Invalid Passphrase" == response.get_json()['name']


def test_decryptMessageErrorMessageBody(client):
    response = client.post('/decryptMessage')

    assert 'Empty Message Body' == response.get_json()['name']


def test_decryptMessageErrorNotAllowed(client):
    response = client.get('/decryptMessage')

    assert 'Method Not Allowed' == response.get_json()['name']


def test_decryptMessageErrorInvalidMessage(client):
    response = client.post('/decryptMessage', data=json.dumps(dict(r=7, b=8)), content_type='application/json')
    assert 'Invalid Message Body' == response.get_json()['name']
