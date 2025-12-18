# parsers/jmeter_parser.py
# 专门用于解析 JMeter 生成的 CSV 格式测试报告

import pandas as pd  # pandas 是强大的数据分析库，用于处理表格数据
from io import StringIO  # 用于把字符串当作文件来读取


def parse_jmeter_csv(csv_text: str):
    """
    功能：解析 JMeter 的 CSV 报告文本，提取每个事务（接口）的性能指标
    输入：csv_text —— JMeter 导出的 CSV 内容（字符串）
    输出：字典，包含事务名称、平均响应时间、错误率等
    """

    # 把字符串转换成类似文件的对象，供 pandas 读取
    df = pd.read_csv(StringIO(csv_text))

    # 创建一个空字典，用来存储每个事务的汇总数据
    summary = {}

    # 按 "label" 列（即事务/接口名称）分组处理
    for label, group in df.groupby('label'):
        total = len(group)  # 该事务的总请求数

        # 计算平均响应时间（单位：毫秒）
        avg_rt = group['elapsed'].mean()

        # 计算 95% 响应时间（即 95% 的请求比这个快）
        p95_rt = group['elapsed'].quantile(0.95)

        # 计算错误率：success 列为 False 的比例 × 100 得到百分比
        error_rate = (group['success'] == False).mean() * 100

        # 把结果存入字典
        summary[label] = {
            "total_requests": int(total),
            "avg_response_time_ms": round(avg_rt, 2),  # 保留两位小数
            "p95_response_time_ms": round(p95_rt, 2),
            "error_rate_percent": round(error_rate, 2)
        }

    # 返回最终结果
    return {
        "report_type": "jmeter",
        "transactions": summary,  # 所有事务的性能数据
        # 简单估算 TPS（每秒事务数）：总请求数 / 测试总时间（秒）
        "global_tps": len(df) / ((df['timeStamp'].max() - df['timeStamp'].min()) / 1000) if len(df) > 1 else 0
    }