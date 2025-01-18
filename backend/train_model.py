# train_model.py
import pandas as pd
from sklearn.linear_model import LinearRegression
from joblib import dump

# Assuming data/expenses.csv exists with columns 'month' and 'amount'
data = pd.read_csv('data/expenses.csv')
model = LinearRegression()
model.fit(data[['month']], data['amount'])

# Save the model
dump(model, 'model.joblib')
