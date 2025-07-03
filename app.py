from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import datetime

app = Flask(__name__)
VISITOR_FILE = "data/visitor/visitor_data.xlsx"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug log

        if not data or "message" not in data:
            print("Missing required fields.")
            return jsonify({"error": "Invalid data"}), 400

        data["timestamp"] = datetime.datetime.now().isoformat()
        df = pd.DataFrame([data])

        os.makedirs(os.path.dirname(VISITOR_FILE), exist_ok=True)

        if os.path.exists(VISITOR_FILE):
            existing_df = pd.read_excel(VISITOR_FILE)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_excel(VISITOR_FILE, index=False)
        else:
            df.to_excel(VISITOR_FILE, index=False)

        print("Data successfully saved to Excel.")
        return jsonify({"message": "Success"}), 200

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)