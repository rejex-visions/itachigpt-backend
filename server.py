from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://itachigptv2.netlify.app"}})

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/test', methods=['GET'])
def test():
    return "Server is alive!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Parse JSON request
        body = request.get_json()
        if not body:
            return jsonify({'type': 'error', 'content': 'No JSON data provided!'}), 400
        
        user_message = body.get('message', '')
        if not user_message:
            return jsonify({'type': 'error', 'content': 'Please send a message!'}), 400
        
        # Initialize the model (replace with your exact model name if different)
        model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
        
        # Define less restrictive safety settings
        safety_settings = {
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_ONLY_HIGH',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_ONLY_HIGH',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_ONLY_HIGH',
        }
        
        # Generate content with safety settings
        response = model.generate_content(
            user_message,
            safety_settings=safety_settings,
            generation_config={'response_mime_type': 'image/png'}  # Request image output
        )
        
        # Handle the response
        if hasattr(response, 'parts') and response.parts:
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data.mime_type.startswith('image/'):
                    # Extract image data (assumed to be base64-encoded)
                    image_data = part.inline_data.data
                    return jsonify({
                        'type': 'image',
                        'content': f'data:image/png;base64,{image_data}'
                    })
                elif hasattr(part, 'text'):
                    return jsonify({'type': 'text', 'content': part.text})
        
        # Fallback if no image or text is found
        return jsonify({'type': 'error', 'content': 'No valid content generated'}), 500
    
    except Exception as e:
        return jsonify({'type': 'error', 'content': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)