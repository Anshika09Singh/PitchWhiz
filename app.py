from flask import Flask, request, render_template
from classify_startup import classify_startup
import json
from airtable_handler import store_data  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    classified_data = None
    error = None

    if request.method == "POST":
        pitch_text = request.form.get("emailBody")
        try:
            result = classify_startup(pitch_text)
            print("Gemini raw output:", result)  # ✅ Inside try block

            classified_data = json.loads(result)

            # Optional: Save to Airtable
            store_data(classified_data)

        except Exception as e:
            error = str(e)

    return render_template("test_form.html", classified_data=classified_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
