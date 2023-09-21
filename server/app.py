from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    # Retrieve all messages ordered by created_at
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.serialize() for message in messages])


# @app.route('/messages')
# def messages():
#     return ''

# @app.route('/messages/<int:id>')
# def messages_by_id(id):
#     return ''
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json
    body = data.get('body')
    username = data.get('username')
    
    if body and username:
        message = Message(body=body, username=username)
        db.session.add(message)
        db.session.commit()
        return jsonify(message.serialize()), 201
    else:
        return jsonify({'error': 'Invalid request data'}), 400
    


    
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    data = request.json
    body = data.get('body')
    
    if body:
        message.body = body
        db.session.commit()
        return jsonify(message.serialize())
    else:
        return jsonify({'error': 'Invalid request data'}), 400
    

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted'})
    

if __name__ == '__main__':
    app.run(port=5555)
