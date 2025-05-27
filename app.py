
from flask import Flask, render_template, request, jsonify, session
from models import db, User, Message
import requests
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

db.init_app(app)

API_KEY = os.getenv("API_KEY")  # Ensure your .env contains API_KEY=your_key_here
print("API_KEY:", API_KEY)  # This should print something like 'sk-or-...'

# 👤 Manage guest users and session tracking
def get_guest_user():
    if 'user_id' not in session:
        user = User(username='guest')
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
    return session['user_id']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history', methods=['GET'])
def chat_history():
    user_id = get_guest_user()
    history = Message.query.filter_by(user_id=user_id).order_by(Message.id).all()
    messages = [{"role": m.role, "content": m.content} for m in history]
    return jsonify(messages)


@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'reply': 'Please enter a message.'})

    user_id = get_guest_user()

    history = Message.query.filter_by(user_id=user_id).order_by(Message.id).all()
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": user_input})

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek/deepseek-r1:free",
            "messages": messages
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers, json=payload)

        if response.status_code != 200:
            return jsonify({'reply': f"Error: {response.status_code} - {response.text}"})

        data = response.json()
        choices = data.get("choices", [])
        if choices and "message" in choices[0]:
            reply = choices[0]["message"].get("content", "No response.")
        else:
            reply = "No response from the assistant."

        db.session.add(Message(user_id=user_id, role='user', content=user_input))
        db.session.add(Message(user_id=user_id, role='assistant', content=reply))
        db.session.commit()

        return jsonify({'reply': reply})

    except Exception as e:
        return jsonify({'reply': f"Error: {str(e)}"})

@app.before_request
def before_request_function():
    db.create_all()

if __name__ == '__main__':
    print("APP TYPE:", type(app))
    app.run(debug=True)
