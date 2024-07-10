import os
from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from pyngrok import ngrok, conf
import logging

# Set environment variables
os.environ['TWILIO_ACCOUNT_SID'] = 'twilio_sid'
os.environ['TWILIO_AUTH_TOKEN'] = 'twilio_authtoken'

# Load pre-trained model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/process', method='POST')
    response.append(gather)
    app.logger.info("Voice request received, gather input for speech.")
    return str(response)

@app.route("/process", methods=['POST'])
def process():
    try:
        speech_text = request.values.get('SpeechResult', None)
        app.logger.info(f"SpeechResult received: {speech_text}")

        if not speech_text:
            raise ValueError("No speech input received")

        response_text = generate_response(speech_text)
        app.logger.info(f"Generated response: {response_text}")
    except Exception as e:
        response_text = f"Error processing speech: {str(e)}"
        app.logger.error(response_text)

    response = VoiceResponse()
    response.say(response_text)
    return str(response)

if __name__ == "__main__":


    app.run(debug=True)
