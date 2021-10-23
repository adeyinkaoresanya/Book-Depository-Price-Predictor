# Boston House Predictor

## Description

The Book Price Predictor is a Python application deployed on Heroku for predicting prices of books listed on the Book Depository website. This application can be accessesd [here](https://boston-house-price-predict.herokuapp.com).

## Tools/Libraries required

* [Python 3.9](https://python.org) : Base programming language for development. The latest version of python.
* sklearn
* pickle
* requests
* flask

## Usage

To predict book prices, send a post request [here](https://boston-house-price-predict.herokuapp.com/predict). The Predict endpoint takes only POST requests using a list of 7 features and return prices of books (in Euros)

```python

import json
import requests

url = "https://boston-house-price-predict.herokuapp.com/predict"
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
post_data = json.dumps(data)
response = requests.post(url, data=post_data)
print(response.status_code, response.content)

```

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

The MIT License - Copyright (c) 2021 - Adeyinka J. Oresanya

[MIT](https://choosealicense.com/licenses/mit/)
