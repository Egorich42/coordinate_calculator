import io
import pytest
import sys
sys.path.append('/app/app')

from app.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_calculate_distances_invalid_csv(client, mocker):
    mocker.patch('app.main.save_task')

    data = {
        'file': (io.BytesIO(b'Invalid CSV content'), 'test.csv')
    }
    response = client.post('/api/v1/calculateDistances', content_type='multipart/form-data', data=data)

    assert response.status_code == 400

def test_get_result_success(client, mocker):
    mocker.patch('app.main.get_task_result', return_value={'task_id': 'test_id', 'status': 'done', 'data': 'Test result'})

    response = client.get('/api/v1/getResult/test_id')

    assert response.status_code == 200
    assert response.json['task_id'] == 'test_id'
    assert response.json['status'] == 'done'

def test_get_result_not_found(client, mocker):
    mocker.patch('app.main.get_task_result', return_value=None)

    response = client.get('/api/v1/getResult?task_id=non_existing_id')

    assert response.status_code == 404