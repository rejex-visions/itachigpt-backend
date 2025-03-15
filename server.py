from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Adjust CORS settings as needed

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Replace with actual model name if different

@app.route('/test', methods=['GET'])
def test():
    return "Server is alive!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'response': 'No message provided!'}), 400
        
        user_message = data['message']
        response = model.generate_content(user_message)
        
        # Determine the response type
        if hasattr(response, 'text'):
            return jsonify({'type': 'text', 'content': response.text})
        elif hasattr(response, 'image_url'):
            return jsonify({'type': 'image', 'content': response.image_url})
        else:
            return jsonify({'type': 'unknown', 'content': str(response)})
    
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)