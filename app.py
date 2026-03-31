from flask import Flask, render_template, request, jsonify
import os
import re
from google import genai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 🔑 API KEY
client = genai.Client(api_key="AIzaSyCbr7PSOn7gy6jK0n7SQy6b7Bj29xzWLFs")


# ------------------ GEMINI OCR ------------------
def extract_text_with_ai(image_path):
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": "Extract all medical values like Hemoglobin, Glucose clearly from this report"},
                        {"inline_data": {"mime_type": "image/jpeg", "data": image_bytes}}
                    ]
                }
            ]
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


# ------------------ ANALYSIS ------------------
def analyze_report(text):
    data = {}

    hemo = re.search(r'Hemoglobin[:\s]*([\d.]+)', text, re.IGNORECASE)
    if hemo:
        value = float(hemo.group(1))
        data['Hemoglobin'] = value
        data['Hemoglobin_status'] = "Low" if value < 12 else "Normal"

    glucose = re.search(r'Glucose[:\s]*([\d.]+)', text, re.IGNORECASE)
    if glucose:
        value = float(glucose.group(1))
        data['Glucose'] = value
        data['Glucose_status'] = "High" if value > 140 else "Normal"

    risk = "Low"
    if data.get('Hemoglobin_status') == "Low" or data.get('Glucose_status') == "High":
        risk = "Medium"
    if data.get('Hemoglobin_status') == "Low" and data.get('Glucose_status') == "High":
        risk = "High"

    data['Risk'] = risk
    return data


# ------------------ AI EXPLAIN ------------------
def ai_explain(data):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"""
            Explain this medical report in simple English:
            {data}
            Also suggest precautions.
            """
        )
        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"


# ------------------ ROUTES ------------------
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files['file']

        filename = file.filename.replace(" ", "_")
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        text = extract_text_with_ai(path)
        data = analyze_report(text)
        explanation = ai_explain(data)

        return jsonify({
            "data": data,
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_msg = request.json.get('message')
        report_data = request.json.get('data')

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"""
            You are a medical assistant.

            Report: {report_data}
            Question: {user_msg}

            Give simple answer.
            """
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": str(e)})


# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True, port=50003)