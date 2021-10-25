# Book Depository Price Predictor

## Description

The Book Depository Price Predictor is a Python application deployed on Heroku for predicting prices of books listed on the Book Depository website. This application can be accessesd [here](https://book-depository-predictions.herokuapp.com/predict).

## Tools/Libraries required

* [Python 3.9](https://python.org) : Base programming language for development. The latest version of python.
* flask
* psycopg2
* sklearn
* pickle
* requests

## Usage

To predict book prices, send a post request [here](https://book-depository-predictions.herokuapp.com/predict). The Predict endpoint takes only POST requests with a list of 7 features and then return prices of books (in Euros)

```python

import json
import requests

url = "https://book-depository-predictions.herokuapp.com/predict"
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
response = requests.post(url, data=request_data)
print(response.status_code, response.content)

```

The recent 10 predictions can be obtained from [here](https://book-depository-predictions.herokuapp.com/recent_predictions).

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

The MIT License - Copyright (c) 2021 - Adeyinka J. Oresanya

[MIT](https://choosealicense.com/licenses/mit/)
