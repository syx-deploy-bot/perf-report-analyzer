from flask import Flask, request, jsonify
import os
import sys

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

try:
    from engine.rules import analyze_report
except ImportError:
    def analyze_report(content):
        return {"summary": "Demo mode: file received", "issues": []}

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    content = file.read().decode('utf-8')
    
    result = analyze_report(content)
    return jsonify(result)

@app.route('/')
def home():
    return jsonify({"message": "Performance Report Analyzer is running on Vercel!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
