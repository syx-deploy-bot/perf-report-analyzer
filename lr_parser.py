# parsers/lr_parser.py
# 用于解析 LoadRunner 生成的 HTML 格式测试报告

from bs4 import BeautifulSoup  # 用于解析 HTML 的库


def parse_lr_html(html_content: str):
    """
    功能：从 LoadRunner 的 HTML 报告中提取事务性能数据
    输入：html_content —— LR 报告的 HTML 源码（字符串）
    输出：字典，包含每个事务的平均响应时间和错误率
    """

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'lxml')  # 'lxml' 是解析器，速度快

    # 在 HTML 中查找事务汇总表（假设 class="TransactionSummary"）
    # ⚠️ 注意：不同版本 LR 表格 class 可能不同，需根据实际调整
    table = soup.find('table', {'class': 'TransactionSummary'})

    # 如果没找到表格，抛出错误
    if not table:
        raise ValueError("未找到事务汇总表，请确保使用标准 LR HTML 报告")

    # 创建空字典存储事务数据
    transactions = {}

    # 找到所有表格行（<tr>），跳过第一行（表头）
    rows = table.find_all('tr')[1:]

    # 遍历每一行（每个事务）
    for row in rows:
        cols = row.find_all('td')  # 获取所有单元格（<td>）

        # 确保这一行有足够的列（至少5列）
        if len(cols) >= 5:
            name = cols[0].get_text(strip=True)  # 第1列：事务名称
            # 第3列：平均响应时间（格式如 "2.45 s"），去掉 "s" 并转为毫秒
            avg_rt = float(cols[2].get_text().replace('s', '')) * 1000
            # 第5列：错误率（格式如 "1.23%"），去掉 "%" 并转为数字
            error_rate = float(cols[4].get_text().strip('%'))

            # 存入字典
            transactions[name] = {
                "avg_response_time_ms": round(avg_rt, 2),
                "error_rate_percent": round(error_rate, 2),
                "total_requests": 0  # LR HTML 通常不提供总请求数，暂时设为0
            }

    return {
        "report_type": "loadrunner",
        "transactions": transactions
    }