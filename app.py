# import os
# from dotenv import load_dotenv
# from flask import Flask, render_template, request, jsonify
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure the API with your key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Create Flask app
# app = Flask(__name__)

# # Enhanced response function with dynamic structuring
# def get_gemini_response(user_input):
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content([user_input])

#     if response and response.text:
#         # Dynamically format the AI response and remove unwanted characters
#         response_text = format_response(response.text)
#         return response_text
#     else:
#         return "I'm here to help, but I'm experiencing some technical issues. Please try again later."

# def format_response(text):
#     # Remove '*' characters and apply structuring
#     text = text.replace('*', '')  # Remove asterisk symbols

#     # Split text into sentences for structured formatting
#     sentences = text.split('. ')
#     formatted_text = ""
    
#     for sentence in sentences:
#         if "reach out" in sentence.lower():
#             formatted_text += f"<li><strong>Reach Out:</strong> {sentence}</li>"
#         elif "seek professional help" in sentence.lower():
#             formatted_text += f"<li><strong>Seek Professional Help:</strong> {sentence}</li>"
#         elif "self-care" in sentence.lower():
#             formatted_text += f"<li><strong>Practice Self-Care:</strong> {sentence}</li>"
#         elif "challenge negative thoughts" in sentence.lower():
#             formatted_text += f"<li><strong>Challenge Negative Thoughts:</strong> {sentence}</li>"
#         elif "set realistic goals" in sentence.lower():
#             formatted_text += f"<li><strong>Set Realistic Goals:</strong> {sentence}</li>"
#         elif "connect with others" in sentence.lower():
#             formatted_text += f"<li><strong>Connect with Others:</strong> {sentence}</li>"
#         else:
#             formatted_text += f"<p>{sentence.strip()}</p>"

#     # Wrap list items in an unordered list if there are any
#     if "<li>" in formatted_text:
#         formatted_text = f"<ul>{formatted_text}</ul>"

#     return formatted_text

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/chat', methods=['POST'])
# def chat():
#     try:
#         user_input = request.json.get('input')  # Get user input from the request

#         # Simple validation
#         if not user_input:
#             return jsonify({"error": "No input provided"}), 400
        
#         # Get response from Gemini model
#         gemini_response = get_gemini_response(user_input)

#         return jsonify({"response": gemini_response}), 200
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re

# Load environment variables
load_dotenv()

# Configure the API with your key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the Flask app
app = Flask(__name__)

# Define the input prompt to guide the AI's responses to be compassionate and mental health-focused
mental_health_prompt = """
You are a compassionate mental health assistant. Respond to user questions with empathy, focusing on mental well-being 
and emotional support. Avoid giving any specific personal contact details, such as phone numbers, email addresses, or 
physical addresses. Do not include links or referrals to external sources. Structure your response to be comforting, 
supportive, and concise, encouraging users to focus on self-care and positive coping strategies.
"""

# Helper function to clean and format the AI response
def sanitize_and_format_response(response_text):
    # Remove any undesired characters (like asterisks)
    response_text = response_text.replace('*', '')

    # Ensure responses are well structured
    sentences = response_text.split('. ')
    formatted_text = ""

    for sentence in sentences:
        if "reach out" in sentence.lower():
            formatted_text += f"<li><strong>Reach Out:</strong> {sentence}</li>"
        elif "seek professional help" in sentence.lower():
            formatted_text += f"<li><strong>Seek Professional Help:</strong> {sentence}</li>"
        elif "self-care" in sentence.lower():
            formatted_text += f"<li><strong>Practice Self-Care:</strong> {sentence}</li>"
        elif "challenge negative thoughts" in sentence.lower():
            formatted_text += f"<li><strong>Challenge Negative Thoughts:</strong> {sentence}</li>"
        elif "set realistic goals" in sentence.lower():
            formatted_text += f"<li><strong>Set Realistic Goals:</strong> {sentence}</li>"
        elif "connect with others" in sentence.lower():
            formatted_text += f"<li><strong>Connect with Others:</strong> {sentence}</li>"
        else:
            formatted_text += f"<p>{sentence.strip()}</p>"

    if "<li>" in formatted_text:
        formatted_text = f"<ul>{formatted_text}</ul>"

    return formatted_text

# Generate AI response using Gemini model with prompt guidance
def get_gemini_response(user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([user_input, mental_health_prompt])

    if response and response.text:
        # Clean and format the AI response
        response_text = sanitize_and_format_response(response.text)
        return response_text
    else:
        return "I'm here to help, but I'm experiencing some technical issues. Please try again later."

@app.route('/')
def home():
    return render_template("index.html", title="Mental Health Friend")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('input')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        # Get response from Gemini with the mental health prompt
        gemini_response = get_gemini_response(user_input)
        return jsonify({"response": gemini_response}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
