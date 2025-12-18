# app.py
# 这是整个插件的入口文件，使用 Flask 框架创建一个 Web 服务
# Coze 智能体会通过 HTTP 请求调用这个服务来分析性能报告

from flask import Flask, request, jsonify  # Flask 是 Python 的轻量级 Web 框架
from parsers.jmeter_parser import parse_jmeter_csv  # 导入 JMeter 报告解析函数
from parsers.lr_parser import parse_lr_html  # 导入 LoadRunner 报告解析函数
from engine.rules import evaluate_rules  # 导入规则引擎函数
import logging  # 用于记录日志，方便调试

# 创建 Flask 应用实例
app = Flask(__name__)

# 设置日志级别为 INFO，这样在出错时能看到详细信息
logging.basicConfig(level=logging.INFO)


# 定义一个 API 接口：当 Coze 发送 POST 请求到 /analyze 时，执行这个函数
@app.route('/analyze', methods=['POST'])
def analyze_report():
    try:
        # 从请求中获取 JSON 数据（Coze 会传 report_type 和 content）
        data = request.json

        # 获取报告类型（"jmeter" 或 "loadrunner"）
        report_type = data.get('report_type')

        # 获取报告内容（JMeter 的 CSV 文本 或 LoadRunner 的 HTML 文本）
        content = data.get('content')

        # 检查参数是否完整
        if not report_type or not content:
            # 如果缺少参数，返回错误信息（HTTP 400）
            return jsonify({"error": "缺少 report_type 或 content"}), 400

        # 根据报告类型，调用不同的解析函数
        if report_type == "jmeter":
            # 调用 JMeter 解析器，传入 CSV 文本
            parsed = parse_jmeter_csv(content)
        elif report_type == "loadrunner":
            # 调用 LoadRunner 解析器，传入 HTML 文本
            parsed = parse_lr_html(content)
        else:
            # 如果类型不支持，返回错误
            return jsonify({"error": "不支持的报告类型"}), 400

        # 使用规则引擎分析解析后的数据，生成修复建议
        suggestions = evaluate_rules(parsed['transactions'])

        # 返回成功结果（JSON 格式）
        return jsonify({
            "status": "success",
            "summary": parsed,  # 包含原始指标数据
            "suggestions": suggestions  # 包含修复建议列表
        })

    except Exception as e:
        # 如果发生任何错误，记录日志并返回错误信息（HTTP 500）
        logging.error(f"分析失败: {str(e)}")
        return jsonify({"error": f"分析失败: {str(e)}"}), 500


# 如果直接运行这个文件（而不是被导入），就启动 Web 服务
if __name__ == '__main__':
    # 监听所有网络接口（0.0.0.0），端口 5000，开启调试模式（方便开发）
    app.run(host='0.0.0.0', port=5000, debug=True)
    print("正在加载解析器...")
    from parsers.jmeter_parser import parse_jmeter_csv
    print("✅ 成功导入 JMeter 解析器")