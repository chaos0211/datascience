import pandas as pd
import os
import matplotlib
matplotlib.use('TkAgg')  # 或 'Agg'，避免使用 InterAgg
import matplotlib.pyplot as plt


def analyze_dataset(file_path, dataset_name=""):
    df = pd.read_csv(file_path)
    print(f"\n📊 {dataset_name} 基本信息:")
    print(f"- 样本总数: {len(df)}")

    label_counts = df['sentiment'].value_counts().sort_index()
    label_map = {0: "负面", 1: "中立", 2: "正面"}

    for label, count in label_counts.items():
        percent = (count / len(df)) * 100
        print(f"- 标签 {label}（{label_map.get(label, '未知')}）: {count} 条，占比 {percent:.2f}%")

    return label_counts


def plot_distribution(train_stats, test_stats):
    label_map = {0: "负面", 1: "中立", 2: "正面"}
    labels = [label_map[k] for k in train_stats.index]  # 动态生成已有标签名
    x = range(len(labels))

    plt.figure(figsize=(8, 5))
    plt.bar(x, train_stats.values, width=0.4, label='训练集', align='center')
    plt.bar([i + 0.4 for i in x], test_stats.values, width=0.4, label='测试集', align='center')
    plt.xticks([i + 0.2 for i in x], labels)
    plt.ylabel('样本数')
    plt.title('训练集与测试集情感标签分布对比')
    plt.legend()
    plt.tight_layout()
    plt.savefig("sentiment_distribution.png")


if __name__ == "__main__":
    data_dir = "data"
    train_path = os.path.join(data_dir, "train.csv")
    test_path = os.path.join(data_dir, "test.csv")

    train_stats = analyze_dataset(train_path, "训练集")
    test_stats = analyze_dataset(test_path, "测试集")

    plot_distribution(train_stats, test_stats)