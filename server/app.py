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

# GET /messages - return all messages ordered by created_at ascending
@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

# POST /messages - create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data.get("body") or not data.get("username"):
        return {"error": "Missing 'body' or 'username'"}, 400

    message = Message(
        body=data["body"],
        username=data["username"]
    )
    db.session.add(message)
    db.session.commit()

    return jsonify(message.to_dict()), 201

# PATCH /messages/<int:id> - update body of message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)
    if not message:
        return {"error": "Message not found"}, 404

    data = request.get_json()
    if "body" in data:
        message.body = data["body"]
    db.session.commit()

    return jsonify(message.to_dict()), 200

# DELETE /messages/<int:id> - delete message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return {"error": "Message not found"}, 404

    db.session.delete(message)
    db.session.commit()
    return {}, 204

if __name__ == '__main__':
    app.run(port=5555)