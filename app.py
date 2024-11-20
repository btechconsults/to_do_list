from flask import Flask, request, jsonify
import boto3
from uuid import uuid4

app = Flask(__name__)

# Setup DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todo_list')

# Endpoint to create a new to-do item
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo_id = str(uuid4())  # Generate a unique ID for the to-do item
    user_id = data.get('user_id')
    content = data.get('content')
    
    # Add to DynamoDB
    table.put_item(
        Item={
            'id': todo_id,
            'user_id': user_id,
            'content': content,
            'completed': False
        }
    )
    return jsonify({"id": todo_id, "message": "To-do item created successfully"}), 201

# Endpoint to get all to-do items for a user
@app.route('/todos/<user_id>', methods=['GET'])
def get_todos(user_id):
    response = table.query(
        KeyConditionExpression='user_id = :user_id',
        ExpressionAttributeValues={':user_id': user_id}
    )
    todos = response['Items']
    return jsonify(todos)

# Endpoint to update the completion status of a to-do item
@app.route('/todos/<todo_id>', methods=['PUT'])
def update_todo_status(todo_id):
    data = request.get_json()
    completed = data.get('completed')
    
    table.update_item(
        Key={'id': todo_id},
        UpdateExpression="set completed = :completed",
        ExpressionAttributeValues={':completed': completed}
    )
    return jsonify({"message": "To-do item updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
