import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

# Load housing dataset
df = pd.read_csv("Housing.csv")
df = df.dropna()

# Convert categorical features to numeric
df = pd.get_dummies(df, columns=[
    'mainroad', 'guestroom', 'basement',
    'hotwaterheating', 'airconditioning', 
    'prefarea', 'furnishingstatus'
], drop_first=True)

X = df.drop("price", axis=1)
y = df["price"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save trained model
with open("model.pkl", "wb") as f:
    pickle.dump((model, X.columns), f)

print("✅ Model trained and saved to model.pkl")
