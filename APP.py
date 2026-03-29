from flask import Flask, request, jsonify
from rag import recommend
import requests

app = Flask(__name__)

# 🔗 Your n8n webhook (replace if needed)
WEBHOOK_URL = "https://rounakdas.app.n8n.cloud/webhook-test/course-bot"


# ------------------------
# HEALTH CHECK ROUTE
# ------------------------
@app.route("/", methods=["GET"])
def home():
    return "✅ AI Course Recommendation API is running!"


# ------------------------
# MAIN CHAT ROUTE
# ------------------------
@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        # Extract data safely
        name = data.get("name", "User")
        email = data.get("email", "")
        query = data.get("query")

        # Validate input
        if not query:
            return jsonify({"error": "Query is required"}), 400

        # 🔥 Generate AI response
        response = recommend(query)

        # ------------------------
        # SEND DATA TO N8N (OPTIONAL)
        # ------------------------
        if email:
            try:
                payload = {
                    "name": name,
                    "email": email,
                    "goal": query,
                    "recommendation": response
                }

                requests.post(WEBHOOK_URL, json=payload, timeout=5)

            except Exception as e:
                print("⚠️ Webhook error:", e)

        # ------------------------
        # RETURN RESPONSE
        # ------------------------
        return jsonify({
            "name": name,
            "query": query,
            "response": response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------
# RUN SERVER
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
