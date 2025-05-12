import joblib
import pandas as pd
import numpy as np

def load_models():
    """
    Load the pre-trained model and preprocessing objects (encoder and scaler)
    Returns:
        tuple: model, encoder, scaler
    """
    model = joblib.load('model/best_model.joblib')
    encoder = joblib.load('model/encoder.joblib')
    scaler = joblib.load('model/scaler.joblib')
    return model, encoder, scaler


def create_salary_band(monthly_income):
    """
    Create SalaryBand based on MonthlyIncome for feature engineering.
    Args:
        monthly_income (float): The employee's monthly income
    Returns:
        str: Salary band category
    """
    if monthly_income < 4000:
        return 'Low'
    elif 4000 <= monthly_income < 8000:
        return 'Medium'
    elif 8000 <= monthly_income < 12000:
        return 'High'
    else:
        return 'Very High'


def predict_attrition(data):
    """
    Make attrition prediction for a single employee dictionary.
    Args:
        data (dict): Dictionary containing all required employee features
    Returns:
        dict: Prediction result with class and probability
    """
    # Load models
    model, encoder, scaler = load_models()

    # Convert input to DataFrame
    df = pd.DataFrame([data])

    # Add engineered feature: SalaryBand
    df['SalaryBand'] = df['MonthlyIncome'].apply(create_salary_band)

    # Get list of expected features from encoder and scaler
    categorical_features = encoder.feature_names_in_.tolist()
    numerical_features = scaler.feature_names_in_.tolist()

    # Check if all required features are present in the input
    for feat in categorical_features + numerical_features:
        if feat not in df.columns.tolist():
            raise ValueError(f"Missing required feature: {feat}")

    # Apply preprocessing
    cat_encoded = encoder.transform(df[categorical_features])
    num_scaled = scaler.transform(df[numerical_features])

    # Combine processed features
    X = np.hstack([cat_encoded, num_scaled])

    # Predict using the model
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]  # Probability for class 1 (attrition)

    # Return prediction result
    return {
        'prediction': int(prediction),
        'probability': float(probability)
    }


# Example usage
if __name__ == "__main__":
    sample_employee = {
        'BusinessTravel': 'Travel_Rarely',
        'JobRole': 'Sales Executive', 
        'MaritalStatus': 'Single',
        'Age': 35,
        'OverTime': 'Yes',
        'DailyRate': 1000,
        'DistanceFromHome': 10,
        'HourlyRate': 50,
        'MonthlyIncome': 5000,
        'MonthlyRate': 15000,
        'PercentSalaryHike': 15,
        'TotalWorkingYears': 5,
        'YearsAtCompany': 2,
        'YearsInCurrentRole': 2
    }
    
    try:
        result = predict_attrition(sample_employee)
        print("\nInput features:", sample_employee)
        print(f"\nPrediction: {'Yes' if result['prediction'] == 1 else 'No'}")
        print(f"Probability of attrition: {result['probability']:.2f}")
    except Exception as e:
        print(f"Error making prediction: {str(e)}")