from flask import Flask, render_template, request, jsonify, send_file
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
        data = request.get_json()
        print("Received data:", data)

        # Validate required fields
        required_keys = ["name", "company", "project", "email", "contact", "message", "reason"]
        if not data or not all(key in data and data[key] for key in required_keys):
            print("Missing one or more required fields.")
            return jsonify({"error": "Invalid data"}), 400

        # Add timestamp to data
        data["timestamp"] = datetime.datetime.now().isoformat()

        # Convert to DataFrame in desired column order
        df = pd.DataFrame([data], columns=["name", "company", "project", "email", "contact", "message", "reason", "timestamp"])

        # Ensure the directory exists
        os.makedirs(os.path.dirname(VISITOR_FILE), exist_ok=True)

        # Append to or create the Excel file
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

@app.route("/download", methods=["GET"])
def download_excel():
    if os.path.exists(VISITOR_FILE):
        return send_file(VISITOR_FILE, as_attachment=True)
    else:
        return "File not found", 404

# Required for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)