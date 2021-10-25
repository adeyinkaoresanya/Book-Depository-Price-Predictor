import json
import pytest
from app import app as flask_app


@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(app, client):
    response = client.get('/')
    assert response.status_code == 200
    result = 'Welcome to the Book Depository Price Prediction Page'
    assert response.get_data(as_text=True) == result

def test_predict_endpoint(app, client):
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


def test_incorrect_input(app, client):
    request_data=json.dumps({"inputs":[{
        "genre": 'biography', 
        "format": 'Paperback', 
        "number_of_pages": 320,
        "weight": 224.0, 
        "rating":  4.02, 
        "rating_count": 173.0
        },
        {"genre": 'horror', 
        "format": 'Paperback', 
        "number_of_pages": 70,
        "weight": 186.0, 
        "rating": 4.026789306511371, 
        "rating_count": 552.0
        }]
})
    response = client.post('/predict', data=request_data)
    assert response.status_code == 400
    result = {"error": "CHECK INPUTS: "}
    assert json.loads(response.get_data()) == result

def test_invalid_input_key(app, client):
        request_data=json.dumps({"input":[{
        "genre": 'biography', 
        "format": 'Paperback', 
        "number_of_pages": 320,
        "weight": 224.0, 
        "rating":  4.02, 
        "rating_count": 173.0
        },
        {"genre": 'horror', 
        "format": 'Paperback', 
        "number_of_pages": 70,
        "weight": 186.0, 
        "rating": 4.026789306511371, 
        "rating_count": 552.0
        }]
})
        response = client.post('/predict', data=request_data)
        assert response.status_code == 400
        result = {"error": "CHECK INPUTS: \'inputs\'"}
        assert json.loads(response.get_data()) == result


def test_recent_predictions(app, client):
    response = client.get('/recent_predictions')
    assert response.status_code == 200
    result = {"recent_predictions": [[18, "horror", "Paperback", 70, 186.0, 4.026789306511371, 552.0, 2021, 20.339779227013057], [17,
"biography", "Paperback", 320, 224.0, 4.02, 173.0, 1994, 19.980390655817313], [16, "horror", "Paperback", 70, 186.0,
4.026789306511371, 552.0, 2021, 20.339779227013057], [15, "biography", "Paperback", 320, 224.0, 4.02, 173.0, 1994,
19.980390655817313], [14, "horror", "Paperback", 70, 186.0, 4.026789306511371, 552.0, 2021, 20.339779227013057], [13,
"biography", "Paperback", 320, 224.0, 4.02, 173.0, 1994, 19.980390655817313], [12, "Suspense", "Paperback", 200, 250.0,
5.0, 600.0, 2021, 18.603846920994716], [11, "crime", "hardback", 320, 360.2, 4.02, 173.0, 2000, 22.436943752511514],
[10, "romance", "Paperback", 100, 200.0, 5.0, 600.0, 2021, 15.630483722139024], [9, "religion", "hardback", 320, 350.2,
4.02, 173.0, 2000, 22.436943752511514]]}
    assert json.loads(response.get_data()) == result



