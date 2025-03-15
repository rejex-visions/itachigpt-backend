from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://itachigptv2.netlify.app"}})  # Replace with your frontend URL

# Load environment variables (e.g., API key)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/test', methods=['GET'])
def test():
    return "Server is alive!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Parse the incoming JSON request
        body = request.get_json()
        if body is None:
            return jsonify({'type': 'error', 'content': 'No JSON data provided!'}), 400
        
        user_message = body.get('message', '')
        if not user_message:
            return jsonify({'type': 'error', 'content': 'Please send a message!'}), 400
        
        # Initialize the generative model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Define safety settings to be less restrictive
        safety_settings = {
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_ONLY_HIGH',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_ONLY_HIGH',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_ONLY_HIGH',
        }
        
        # Generate content with the adjusted safety settings
        response = model.generate_content(user_message, safety_settings=safety_settings)
        
        # Handle the response
        if hasattr(response, 'text'):
            return jsonify({'type': 'text', 'content': response.text})
        elif hasattr(response, 'image_url'):  # Note: Check actual attribute for images
            return jsonify({'type': 'image', 'content': response.image_url})
        else:
            return jsonify({'type': 'error', 'content': 'Unknown response type'}), 500
    
    except Exception as e:
        return jsonify({'type': 'error', 'content': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)