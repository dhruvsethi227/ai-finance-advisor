# main.py
from flask import Flask, request, jsonify
from models import add_transaction, get_transactions, update_transaction, delete_transaction
from joblib import load
import pandas as pd

# Initialize the Flask application
app = Flask(__name__)

# Load the trained ML model for expense prediction
model = load('model.joblib')

# /expenses endpoint for CRUD operations
@app.route('/expenses', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_expenses():
    if request.method == 'GET':
        # Return all transactions
        return jsonify(get_transactions())
    elif request.method == 'POST':
        # Add a new transaction
        transaction = request.json
        add_transaction(transaction)
        return jsonify({'message': 'Transaction added!'}), 201
    elif request.method == 'PUT':
        # Update an existing transaction
        data = request.json
        index = data['index']
        update_transaction(index, data['transaction'])
        return jsonify({'message': 'Transaction updated!'}), 200
    elif request.method == 'DELETE':
        # Delete a transaction
        index = request.json['index']
        delete_transaction(index)
        return jsonify({'message': 'Transaction deleted!'}), 200

# /predict-expenses endpoint for predicting future expenses using the ML model
@app.route('/predict-expenses', methods=['POST'])
def predict_expenses():
    data = request.json
    month = data['month']
    # Make prediction using the loaded model
    prediction = model.predict([[month]])[0]
    return jsonify({'predicted_amount': prediction})

# /tips endpoint for generating savings tips based on transactions
@app.route('/tips', methods=['GET'])
def get_tips():
    tips = generate_tips(get_transactions())
    return jsonify({'tips': tips})

# Function to generate dynamic savings tips based on transaction data
def generate_tips(transactions):
    total_spent = sum(t['amount'] for t in transactions)
    tips = []
    if total_spent > 1000:
        tips.append("Consider cutting back on non-essential expenses.")
    if len([t for t in transactions if t['category'] == 'Dining']) > 5:
        tips.append("Reduce dining out to save more.")
    return tips

# Main entry point to run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
