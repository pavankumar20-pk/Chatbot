from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# HTML + CSS + JS all combined in one template
html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Simple Chatbot</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f2f2f2;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .chat-container {
      width: 360px;
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0,0,0,0.2);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .chat-box {
      flex: 1;
      padding: 10px;
      overflow-y: auto;
    }
    .message {
      margin: 8px 0;
      padding: 8px 10px;
      border-radius: 10px;
      max-width: 80%;
    }
    .user {
      background: #0078d7;
      color: #fff;
      align-self: flex-end;
    }
    .bot {
      background: #e0e0e0;
      align-self: flex-start;
    }
    .input-area {
      display: flex;
      border-top: 1px solid #ccc;
    }
    input {
      flex: 1;
      padding: 10px;
      border: none;
      outline: none;
    }
    button {
      background: #0078d7;
      color: white;
      border: none;
      padding: 10px 15px;
      cursor: pointer;
    }
    button:hover {
      background: #005fa3;
    }
  </style>
</head>
<body>
  <div class="chat-container">
    <div id="chat-box" class="chat-box"></div>
    <div class="input-area">
      <input type="text" id="user-input" placeholder="Type your message..." />
      <button onclick="sendMessage()">Send</button>
    </div>
  </div>

  <script>
    async function sendMessage() {
      const input = document.getElementById("user-input");
      const message = input.value.trim();
      if (!message) return;

      addMessage("user", message);
      input.value = "";

      const response = await fetch("/get", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      addMessage("bot", data.response);
    }

    function addMessage(sender, text) {
      const chatBox = document.getElementById("chat-box");
      const msg = document.createElement("div");
      msg.classList.add("message", sender);
      msg.textContent = text;
      chatBox.appendChild(msg);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_page)

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_msg = request.json.get("message", "").lower()

    # Simple rule-based chatbot logic
    if "hello" in user_msg or "hi" in user_msg:
        response = "Hello! How can I help you today?"
    elif "your name" in user_msg:
        response = "I'm your simple chatbot built using Python and Flask!"
    elif "how are you" in user_msg:
        response = "I'm doing great, thanks for asking! 😊"
    elif "bye" in user_msg:
        response = "Goodbye! Have a wonderful day!"
    else:
        response = "I'm not sure I understand that yet."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
