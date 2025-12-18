# engine/rules.py
# 实现一个简单的规则引擎：根据预设规则判断是否存在性能问题

import yaml  # 用于读取 YAML 配置文件
import os  # 用于构建文件路径

from pathlib import Path
# 获取当前文件所在目录
BASE_DIR = Path(__file__).parent
RULES_FILE = BASE_DIR / "suggestions.yaml"

def load_rules():
    """从 YAML 文件加载所有规则"""
    with open(RULES_FILE, encoding='utf-8') as f:
        return yaml.safe_load(f)['rules']


def evaluate_rules(transactions):
    """
    功能：对每个事务应用所有规则，生成修复建议
    输入：transactions —— 字典，key=事务名，value=指标（如 avg_response_time_ms）
    输出：建议列表，按优先级排序
    """
    rules = load_rules()  # 加载规则
    suggestions = []  # 存放匹配成功的建议

    # 遍历每个事务
    for trans_name, metrics in transactions.items():
        # 构建上下文：把事务名和所有指标合并成一个字典
        context = {"transaction_name": trans_name, **metrics}

        # 遍历每条规则
        for rule in rules:
            cond = rule['condition']  # 获取规则的条件部分
            value = context.get(cond['metric'])  # 从上下文中取指标值
            threshold = cond['threshold']  # 获取阈值

            # 如果该指标不存在（比如 LR 没有 TPS），跳过
            if value is None:
                continue

            # 判断是否满足条件（目前只支持 > 和 <）
            triggered = False
            if cond['operator'] == '>':
                triggered = value > threshold
            elif cond['operator'] == '<':
                triggered = value < threshold

            # 如果条件满足，生成建议
            if triggered:
                # 使用 Python 的 .format() 方法替换模板中的占位符
                suggestion = rule['suggestion'].format(
                    transaction_name=trans_name,
                    value=value,
                    threshold=threshold
                )
                # 添加到建议列表
                suggestions.append({
                    "rule_id": rule['id'],
                    "transaction": trans_name,
                    "suggestion": suggestion,
                    "priority": rule.get('priority', 3)  # 默认优先级为3
                })

    # 按优先级从小到大排序（1 最紧急）
    return sorted(suggestions, key=lambda x: x['priority'])