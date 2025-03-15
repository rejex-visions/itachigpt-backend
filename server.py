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

@app.route('/chat', methods=['POST'])
def chat():
    try:
        body = request.get_json()
        if not body or 'message' not in body:
            return jsonify({'response': 'No message provided!'}), 400
        
        user_message = body['message']
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Safety settings
        safety_settings = {
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_ONLY_HIGH',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_ONLY_HIGH',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_ONLY_HIGH',
        }
        
        # Generate text response
        response = model.generate_content(
            user_message,
            safety_settings=safety_settings
        )
        
        return jsonify({'response': response.text})
    
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)