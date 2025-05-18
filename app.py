from flask import Flask, request, jsonify, send_from_directory
import os
import requests  # for calling the Groq or OpenAI API

app = Flask(__name__, static_folder="build", static_url_path="")

# Load your API key from environment variable
API_KEY = os.environ.get("GROQ_API_KEY")  # Or OPENAI_API_KEY

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Send request to Groq API (example with Mixtral or LLaMA3)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",  # or "llama3-70b-8192"
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    else:
        return jsonify({"error": "Failed to get response"}), 500

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
