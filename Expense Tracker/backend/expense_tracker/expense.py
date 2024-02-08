from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Expense
from . import db

expense = Blueprint('expense', __name__)

@expense.route('/', methods=['POST'])
@jwt_required()
def create_expense():
    current_user_id = get_jwt_identity()
    data = request.json
    # Create expense logic here
    return jsonify({'message': 'Expense created successfully'}), 201

@expense.route('/<int:expense_id>/edit/', methods=['PUT'])
@jwt_required()
def edit_expense(expense_id):
    current_user_id = get_jwt_identity()
    data = request.json
    # Edit expense logic here
    return jsonify({'message': 'Expense updated successfully'}), 200

@expense.route('/<int:expense_id>/delete/', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    current_user_id = get_jwt_identity()
    # Delete expense logic here
    return jsonify({'message': 'Expense deleted successfully'}), 200

@expense.route('/', methods=['GET'])
@jwt_required()
def get_all_expenses():
    current_user_id = get_jwt_identity()
    # Get all expenses for the current user logic here
    expenses = Expense.query.filter_by(user_id=current_user_id).all()
    return jsonify([expense.serialize() for expense in expenses]), 200
