from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

ID = ""
client = OpenAI(api_key="")

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_input = data.get("user_input")

    if not user_input:
        return jsonify({"error": "No user input provided"}), 400

    # Send user input to OpenAI for processing
    chat = client.beta.threads.create(
        messages=[{"role": "user", "content": user_input}]
    )
    run = client.beta.threads.runs.create(thread_id=chat.id, assistant_id=ID)

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=chat.id, run_id=run.id)
        time.sleep(0.5)

    message_response = client.beta.threads.messages.list(thread_id=chat.id)
    messages = message_response.data
    latest_message = messages[0]

    # Return AI response as JSON
    return jsonify({"response": latest_message.content[0].text.value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
