from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import datetime

app = Flask(__name__)

# Path to save visitor data
VISITOR_FILE = "data/visitor/visitor_data.xlsx"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Receive JSON data from frontend
        data = request.get_json()
        print("Received data:", data)  # Debug log

        # Basic validation
        if not data or "message" not in data:
            print("Missing required fields.")
            return jsonify({"error": "Invalid data"}), 400

        # Add timestamp
        data["timestamp"] = datetime.datetime.now().isoformat()
        df = pd.DataFrame([data])

        # Ensure directory exists
        os.makedirs(os.path.dirname(VISITOR_FILE), exist_ok=True)

        # Append or create Excel file
        if os.path.exists(VISITOR_FILE):
            existing_df = pd.read_excel(VISITOR_FILE)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_excel(VISITOR_FILE, index=False)
        else:
            df.to_excel(VISITOR_FILE, index=False)

        print("Data saved to Excel successfully.")
        return jsonify({"message": "Success"}), 200

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": "Internal server error"}), 500

# Required for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)