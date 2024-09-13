from jieba import cut
import hashlib
import re

def hash_value(s):
    # 生成 64 位哈希值
    return int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)

def hamming_distance(hash1, hash2):
    # 计算两个 SimHash 的汉明距离
    return bin(hash1 ^ hash2).count('1')

def simhash(text, hash_bits=64):
    # 计算文本的 SimHash
    # 初始化一个位数组，长度等于哈希位数
    v = [0] * hash_bits
    for word in text.split():
        h = hash_value(word)
        for i in range(hash_bits):
            if h & (1 << i):
                v[i] += 1
            else:
                v[i] -= 1

    # 计算最终的 SimHash
    fingerprint = 0
    for i in range(hash_bits):
        if v[i] >= 0:
            fingerprint |= (1 << i)

    return fingerprint

def read_file(file_path: str) -> str:
    # 从文件中读取中文文本内容
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def preprocess_text(text: str) -> str:
    # 对中文文本进行分词处理
    text = re.sub(r'[^\w\s]', '', text)  # 去除标点
    return ' '.join(cut(text))
