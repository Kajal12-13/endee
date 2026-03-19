import os
import requests
import pdfplumber
from flask import Flask, request, render_template_string
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# 1. Load the Model (Fast and accurate for RAG)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Configuration for Endee Vector DB
ENDEE_URL = os.getenv("ENDEE_URL", "http://localhost:8080")
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 3. Logic: Extract PDF text and send to Endee
def index_resume_to_endee(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
        chunks = [c.strip() for c in text.split('\n\n') if len(c) > 30]
        
        for i, chunk in enumerate(chunks):
            embedding = model.encode(chunk).tolist()
            try:
                requests.post(f"{ENDEE_URL}/upsert", json={
                    "collection": "resumes",
                    "id": f"chunk_{i}",
                    "vector": embedding,
                    "payload": {"text": chunk}
                }, timeout=5)
            except Exception as e:
                print(f"Index Error: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        # Handle Resume Upload
        if 'resume' in request.files:
            file = request.files['resume']
            if file.filename != '':
                path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(path)
                index_resume_to_endee(path)
                response = "✅ Resume successfully indexed in Endee Vector DB!"
        
        # Handle AI Query
        elif 'user_query' in request.form:
            query = request.form.get("user_query")
            query_vec = model.encode(query).tolist()
            try:
                res = requests.post(f"{ENDEE_URL}/search", json={
                    "collection": "resumes",
                    "vector": query_vec,
                    "limit": 3
                }, timeout=5).json()
                
                hits = res.get('results', [])
                if hits:
                    response = "\n\n".join([h['payload']['text'] for h in hits])
                else:
                    response = "No matching information found in the resume."
            except Exception as e:
                response = f"❌ Error connecting to Endee: {str(e)}"

    return render_template_string(HTML_UI, response=response)

# 4. Clean UI Template
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>Endee AI Resume Chatbot</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f8f9fa; display: flex; justify-content: center; padding: 50px; }
        .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); width: 600px; }
        .box { background: #e9f5ff; padding: 20px; border-radius: 8px; margin: 20px 0; white-space: pre-wrap; text-align: left; }
        input, textarea, button { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #ddd; }
        button { background: #007bff; color: white; border: none; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>AI Resume Assistant 🤖</h2>
        <form method="POST" enctype="multipart/form-data">
            <p><strong>Step 1: Upload Resume (PDF)</strong></p>
            <input type="file" name="resume" accept=".pdf">
            <button type="submit">Upload & Index</button>
        </form>
        <hr>
        <form method="POST">
            <p><strong>Step 2: Ask a Question</strong></p>
            <textarea name="user_query" placeholder="e.g. What is the candidate's education?"></textarea>
            <button type="submit">Search Resume</button>
        </form>
        {% if response %}<div class="box"><strong>AI Response:</strong>\n\n{{ response }}</div>{% endif %}
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(port=5000, debug=True)