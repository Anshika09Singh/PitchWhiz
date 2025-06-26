from flask import Flask, request, render_template
from classify_startup import classify_startup
from airtable_handler import store_data
import json
import re
from collections import Counter

app = Flask(__name__)

# Dummy summary generator (replace with AI model integration)
def generate_summary(email_text):
    return "This is a summary of the pitch: A startup is solving a problem with a unique solution and seeks funding."

# Simple keyword extractor (can be improved with NLP libraries later)
def extract_keywords(text, top_n=10):
    if not text:
        return []

    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())  # Extract words with 4+ letters
    stopwords = set([
        'this', 'that', 'with', 'from', 'they', 'have', 'which', 'will', 'their', 'about',
        'would', 'could', 'should', 'we’re', 'were', 'where', 'your', 'what', 'when', 'then',
        'being', 'such', 'into', 'them', 'also', 'just', 'more', 'than', 'like', 'some',
        'team', 'startup', 'capital', 'dear', 'auxano', 'hello', 'thank', 'regards', 'best'
    ])
    filtered_words = [word for word in words if word not in stopwords]
    most_common = Counter(filtered_words).most_common(top_n)
    return [kw for kw, _ in most_common]

# Home page with Classifier
@app.route("/", methods=["GET", "POST"])
def index():
    classified_data = None
    error = None
    summary_text = None
    keywords = None

    if request.method == "POST":
        pitch_text = request.form.get("emailBody")
        try:
            result = classify_startup(pitch_text)
            print("Gemini raw output:", result)
            classified_data = json.loads(result)
            store_data(classified_data)
        except Exception as e:
            error = str(e)

    return render_template("test_form.html", classified_data=classified_data, error=error)

# Summary generator route
@app.route("/summary", methods=["POST"])
def summary():
    summary_text = None
    error = None
    classified_data = None
    keywords = None

    try:
        email_text = request.form.get("summaryInput")
        if email_text:
            summary_text = generate_summary(email_text)
        else:
            error = "No email text provided for summary generation."
    except Exception as e:
        error = str(e)

    return render_template("test_form.html", summary=summary_text, error=error)

# Keyword extractor route
@app.route("/keywords", methods=["POST"])
def keywords_route():
    keywords = None
    error = None
    classified_data = None
    summary_text = None

    try:
        email_text = request.form.get("keywordsInput")
        if email_text:
            keywords = extract_keywords(email_text)
        else:
            error = "No email text provided for keyword extraction."
    except Exception as e:
        error = str(e)

    return render_template("test_form.html", keywords=keywords, error=error)

if __name__ == "__main__":
    app.run(debug=True)
