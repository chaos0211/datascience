import pymysql
from datetime import datetime


conn = pymysql.connect(
        host='localhost',
        port=33309,
        user='root',
        password='123456',  # 替换为你的 MySQL 密码
        database='D-science',
        charset='utf8mb4'
    )

def save_metrics_to_mysql(model_name, metrics: dict):
    cursor = conn.cursor()
    for metric_name, value in metrics.items():
        sql = """
        INSERT INTO model_metrics (model_name, metric_name, metric_value, updated_at)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE metric_value=%s, updated_at=%s
        """
        now = datetime.now()
        cursor.execute(sql, (model_name, metric_name, value, now, value, now))

    conn.commit()
    cursor.close()
    conn.close()

def get_model_metrics():
    with conn.cursor() as cursor:
        cursor.execute("SELECT model_name, metric_name, metric_value FROM model_metrics")
        results = cursor.fetchall()

    metrics = {
        "metrics": ["Precision", "Recall", "F1-score"]
    }

    for row in results:
        model_name = row[0]
        metric_name = row[1]
        metric_value = row[2]

        if model_name not in metrics:
            metrics[model_name] = []

        metrics[model_name].append(metric_value)

    return metrics