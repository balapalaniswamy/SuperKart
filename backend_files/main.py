import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Loading the trained pipeline (preprocessing + model bundled together)
superkart_model = joblib.load("superkart_model.joblib")

# Creating the Flask app
superkart_api = Flask("superkart_sales_prediction")


@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"


@superkart_api.post('/v1/predict')
def predict_superkart_sales():
    # Getting the single-record JSON payload sent by the client
    prediction_input = request.get_json()

    # Converting the incoming dict into a single-row DataFrame
    # (the pipeline expects a DataFrame with the exact training column names)
    sample = pd.DataFrame({
        'Product_Weight': [prediction_input.get('Product_Weight')],
        'Product_Sugar_Content': [prediction_input.get('Product_Sugar_Content')],
        'Product_Allocated_Area': [prediction_input.get('Product_Allocated_Area')],
        'Product_MRP': [prediction_input.get('Product_MRP')],
        'Store_Size': [prediction_input.get('Store_Size')],
        'Store_Location_City_Type': [prediction_input.get('Store_Location_City_Type')],
        'Store_Type': [prediction_input.get('Store_Type')],
        'Product_Id_char': [prediction_input.get('Product_Id_char')],
        'Store_Age_Years': [prediction_input.get('Store_Age_Years')],
        'Product_Type_Category': [prediction_input.get('Product_Type_Category')],
    })

    # Running the sample through the full pipeline (preprocessing + model)
    predicted_sales = superkart_model.predict(sample).tolist()[0]

    return jsonify({'Predicted_Product_Store_Sales_Total': predicted_sales})


@superkart_api.post('/v1/predictbatch')
def predict_superkart_sales_batch():
    # Getting the uploaded CSV file from the request
    file = request.files.get('file')

    # Reading the CSV into a DataFrame
    batch_sample = pd.read_csv(file)

    # Running the whole batch through the pipeline in one go
    batch_predictions = superkart_model.predict(batch_sample)

    # Returning predictions keyed by row index (as JSON so it's easy to inspect)
    response = pd.Series(batch_predictions).to_json(orient='index')

    return response


if __name__ == '__main__':
    # Running on port 7860, listening on every interface (needed for Docker/Codespaces)
    superkart_api.run(host="0.0.0.0", port=7860)
