import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# 1. Load the dataset
# As per instructions, we use a subset of features.
if not os.path.exists('../train.csv'):
    # Fallback if running from within model directory without file
    if os.path.exists('train.csv'):
        df = pd.read_csv('train.csv')
    else:
        # Try parent directory
        df = pd.read_csv('../train.csv')
else:
    df = pd.read_csv('../train.csv')

print(f"Dataset loaded. Shape: {df.shape}")

# Selected features (6 features chosen from the allowed list)
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'FullBath', 'YearBuilt', 'Neighborhood']
target = 'SalePrice'

X = df[features]
y = df[target]

# 2. Preprocessing
# Split numerical and categorical features
numeric_features = ['OverallQual', 'GrLivArea', 'GarageCars', 'FullBath', 'YearBuilt']
categorical_features = ['Neighborhood']

# Create transformers
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine transformers
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# 3. Model Pipeline
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the model
print("Training Random Forest Model...")
model.fit(X_train, y_train)

# 5. Evaluate the model
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("-" * 30)
print("Model Evaluation Metrics:")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.4f}")
print("-" * 30)

# 6. Save the model
model_path = 'house_price_model.pkl'
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")

# Verify reload
loaded_model = joblib.load(model_path)
print("Model reload verification successful.")
