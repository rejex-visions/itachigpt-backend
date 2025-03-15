from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://itachigptv2.netlify.app"}})

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/test', methods=['GET'])
def test():
    return "Server is alive!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        body = request.get_json()
        if body is None:
            return jsonify({'response': 'No JSON data provided!'}), 400
        user_message = body.get('message', '')
        if not user_message:
            return jsonify({'response': 'Please send a message!'}), 400
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)