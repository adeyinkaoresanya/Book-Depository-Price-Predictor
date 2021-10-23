import json
import pytest
from src.app import app as flask_app


@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home(app, client):
    response = client.get('/')
    assert response.status_code == 200
    result = 'Welcome to the Book Depository Price Prediction Page'
    assert response.get_data(as_text=True) == result

def test_predict(app, client):
    request_data=json.dumps({"inputs":[{
           "genre": 'biography', 
           "format": 'Paperback', 
           "number_of_pages": 320,
           "weight": 224.0, 
           "rating":  4.02, 
           "rating_count": 173.0, 
           "year": 1994
           },
           {"genre": 'horror', 
           "format": 'Paperback', 
           "number_of_pages": 70,
           "weight": 186.0, 
           "rating": 4.026789306511371, 
           "rating_count": 552.0, 
           "year": 2021
           }]
})
    response = client.post('/predict', data=request_data)
    assert response.status_code == 200
    result = {"predicted_book_price": [19.980390655817313, 20.339779227013057]}
    assert json.loads(response.get_data()) == result

# def test_recent_predictions(app, client):
#     response = client.get('/recent_predictions')
#     assert response.status_code == 200
#     result = 'Welcome to the Boston House Prediction Page'
#     assert response.get_data(as_text=True) == result

