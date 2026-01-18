from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load the trained model
model_path = os.path.join('model', 'house_price_model.pkl')
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    print(f"Model not found at {model_path}")
    model = None

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        try:
            # Extract features from form
            overall_qual = int(request.form['OverallQual'])
            gr_liv_area = float(request.form['GrLivArea'])
            garage_cars = int(request.form['GarageCars'])
            full_bath = int(request.form['FullBath'])
            year_built = int(request.form['YearBuilt'])
            neighborhood = request.form['Neighborhood']

            # Create DataFrame for model input
            input_data = pd.DataFrame([[overall_qual, gr_liv_area, garage_cars, full_bath, year_built, neighborhood]],
                                      columns=['OverallQual', 'GrLivArea', 'GarageCars', 'FullBath', 'YearBuilt', 'Neighborhood'])

            # Predict
            if model:
                predicted_price = model.predict(input_data)[0]
                prediction = f"${predicted_price:,.2f}"
            else:
                prediction = "Error: Model not loaded."

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
