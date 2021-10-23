import pytest
import json
from utils.validate import validate_input

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

parsed_data = json.loads(request_data)["inputs"]

def test_validate_correct_number_of_inputs():
    #parsed_data = json.loads(request_data)["inputs"]
    features = validate_input(request_data)
    assert len(features.columns)== 7