import json
import pandas as pd


def validate_input(request_data: str) -> tuple:
    """
    This function preprocesses the request data and transforms into the format accepted by model
    
    Args:
        request_data (str): data in JSON format obtained from requests
        
    Returns:
         A dictionary of inputs and a dataframe
    """
    parsed_data = json.loads(request_data)["inputs"]
    assert type(parsed_data) == list and len({k for d in parsed_data for k in d.keys()}) == 7   #'inputs' should contain 7 features
    features = {"genre": [], "format": [], "number_of_pages": [],
                "weight": [], "rating": [], "rating_count": [], "year": []}
    for i in range(len(parsed_data)):
        features["genre"].append(parsed_data[i]["genre"])
        features["format"].append(parsed_data[i]["format"])
        features["number_of_pages"].append(parsed_data[i]["number_of_pages"])
        features["weight"].append(parsed_data[i]["weight"])
        features["rating"].append(parsed_data[i]["rating"])
        features["rating_count"].append(parsed_data[i]["rating_count"])
        features["year"].append(parsed_data[i]["year"])
        data= pd.DataFrame(features)
    return data
