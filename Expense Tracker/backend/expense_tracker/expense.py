from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Expense, User
from . import db
from datetime import datetime

expense = Blueprint('expense', __name__)

@expense.route('/', methods=['POST'])
@jwt_required()
def create_expense():
    current_user_id = get_jwt_identity()
    data = request.json
    
    expense = Expense(
        amount=data['amount'],
        category=data['category'],
        description=data.get('description'),
        date=datetime.utcnow(),
        user_id=current_user_id 
    )
    db.session.add(expense)
    db.session.commit()
    
    return jsonify({'message': 'Expense created successfully'}), 201

@expense.route('/<int:expense_id>/', methods=['PUT'])
@jwt_required()
def edit_expense(expense_id):
    current_user_id = get_jwt_identity()
    data = request.json
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user_id).first()
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    # Update the expense
    expense.amount = data.get('amount')
    expense.category = data.get('category')
    expense.description = data.get('description')

    db.session.commit()
    return jsonify({'message': 'Expense updated successfully'}), 200

@expense.route('/<int:expense_id>/', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    current_user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user_id).first()
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'}), 200

@expense.route('/', methods=['GET'])
@jwt_required()
def get_all_expenses():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    expenses = [{'id': expense.id,
                 'amount': expense.amount,
                 'category': expense.category,
                 'description': expense.description,
                 'date': expense.date} for expense in user.expenses]
    return jsonify({'expenses': expenses}), 200
