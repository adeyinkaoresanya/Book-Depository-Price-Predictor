import os
import sys
import numpy as np
from flask import Flask, request
from utils.validate import validate_input
from database.dbconnector import DatabaseConnector
import json
import pickle


db = DatabaseConnector()

model = pickle.load(open('models\model.pkl', 'rb'))
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return ('Welcome to the Book Depository Price Prediction Page')

@app.route("/predict", methods=["POST"])
def predict() -> str:
    '''
    Feeds the request data to the model and returns the predicted values

    Returns:
        The predictions in JSON format
    '''
    try:
        
        data= validate_input(request.data)
        predictions = model.predict(data)
        data["price"] = predictions
        db.save_predictions_to_database(data)
        return json.dumps({"predicted_book_price": predictions.tolist()}), 200
    except (KeyError, json.JSONDecodeError, AssertionError) as error:
        return json.dumps({"error": f"CHECK INPUTS: {error}"}), 400
    except Exception as e:
        raise e
        # return json.dumps({"error": f"{e}"}), 400


@app.route("/recent_predictions", methods=["GET"])
def recent_predictions():
    """
    Fetches the lastest 10 predictions from the database
    
    Returns:
        The latest 10 predictions
    """
    try:
        latest_ten = db.pull_predictions_from_database()
        return json.dumps({"recent_predictions": latest_ten})
    except Exception as error:
        return json.dumps({"error": f"Something went wrong.Try again later."}), 500
