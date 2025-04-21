import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
import os,re

def load_data(file_path):
    df = pd.read_csv(file_path, encoding='latin-1', header=None)
    df.columns = ['sentiment', 'id', 'date', 'query', 'user', 'text']
    df = df[['sentiment', 'text']]
    return df

def preprocess_text(text):
    # 文本清洗、去除标点符号、大小写标准化
    pass

def preprocess_dataset(df):
    df['text'] = df['text'].apply(preprocess_text)
    return df

def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # 移除URL
    text = re.sub(r"@\w+", "", text)     # 移除@用户
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)  # 移除特殊字符
    text = text.lower()                  # 转小写
    return text.strip()

def preprocess_and_split(csv_path, output_dir):
    df = pd.read_csv(csv_path, encoding='latin-1', header=None)
    df.columns = ['sentiment', 'id', 'date', 'query', 'user', 'text']
    df = df[['sentiment', 'text']]

    df['sentiment'] = df['sentiment'].map({0: 0, 2: 1, 4: 2})  # 0:负, 1:中, 2:正
    df['text'] = df['text'].apply(clean_text)

    # 去除空文本
    df = df[df['text'].str.strip().astype(bool)]

    # 切分训练集和测试集
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    os.makedirs(output_dir, exist_ok=True)
    train_df.to_csv(os.path.join(output_dir, "train.csv"), index=False)
    test_df.to_csv(os.path.join(output_dir, "test.csv"), index=False)
    print(f"预处理完成，已生成 train.csv 与 test.csv，共 {len(train_df)} 条训练数据，{len(test_df)} 条测试数据。")

def main():
    df = load_data('data/sentiment140.csv')
    df = preprocess_dataset(df)
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    train.to_csv('data/train.csv', index=False)
    test.to_csv('data/test.csv', index=False)

if __name__ == "__main__":
    preprocess_and_split(
        csv_path="data/training.1600000.processed.noemoticon.csv",
        output_dir="data"
    )