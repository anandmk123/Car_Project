from flask import Flask, request, jsonify
import pandas as pd
import joblib
import shap

app = Flask(__name__)

# Load the complete pipeline from Google Drive
model_path = 'best_car_price_model.pkl'
loaded_pipeline = joblib.load(model_path)

def predict_price(data):
    input_data = pd.DataFrame([data])
    predicted_price = loaded_pipeline.predict(input_data)[0]
    return predicted_price

def get_max_contribution(data):
    input_data = pd.DataFrame([data])
    
    # Transform input data
    input_transformed = loaded_pipeline.named_steps['preprocessor'].transform(input_data)
    
    # Create SHAP explainer and get SHAP values
    explainer = shap.Explainer(loaded_pipeline.named_steps['model'])
    shap_values = explainer(input_transformed)

    # Convert SHAP values to DataFrame
    shap_values_df = pd.DataFrame(shap_values.values, columns=loaded_pipeline.named_steps['preprocessor'].get_feature_names_out())

    # Get the highest contributing attribute
    max_contribution_feature = shap_values_df.abs().max().idxmax()
    max_contribution_value = shap_values_df[max_contribution_feature].values[0]
    predicted_price = predict_price(data)
    percentage_contribution = (max_contribution_value / predicted_price) * 100
    
    return max_contribution_feature, percentage_contribution

@app.route('/predict_price', methods=['GET'])
def price_prediction():
    # Get query parameters
    params = {
        'brand': request.args.get('brand'),
        'model': request.args.get('model'),
        'year_of_manufacture': int(request.args.get('year_of_manufacture')),
        'km_driven': int(request.args.get('km_driven')),
        'fuel_type': request.args.get('fuel_type'),
        'transmission_type': request.args.get('transmission_type'),
        'mileage': float(request.args.get('mileage')),
        'engine': float(request.args.get('engine')),
        'max_power': float(request.args.get('max_power')),
        'seats': int(request.args.get('seats'))
    }

    predicted_price = predict_price(params)
    return jsonify({'predicted_price': predicted_price})

@app.route('/max_contribution', methods=['GET'])
def max_contribution():
    # Get query parameters
    params = {
        'brand': request.args.get('brand'),
        'model': request.args.get('model'),
        'year_of_manufacture': int(request.args.get('year_of_manufacture')),
        'km_driven': int(request.args.get('km_driven')),
        'fuel_type': request.args.get('fuel_type'),
        'transmission_type': request.args.get('transmission_type'),
        'mileage': float(request.args.get('mileage')),
        'engine': float(request.args.get('engine')),
        'max_power': float(request.args.get('max_power')),
        'seats': int(request.args.get('seats'))
    }

    feature, percentage = get_max_contribution(params)
    return jsonify({'highest_contributing_feature': feature, 'percentage_contribution': percentage})

if __name__ == '__main__':
    app.run(debug=True)

