from flask import Flask, request, jsonify
import os
import sys

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

# 导入你的分析模块（根据你的实际结构调整）
try:
    from engine.rules import analyze_report
except ImportError:
    # 如果导入失败，模拟一个简单响应
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

# Vercel 入口（关键！）
if __name__ == "__main__":
    app.run()
