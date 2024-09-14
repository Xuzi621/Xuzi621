import unittest
import hashlib
import re
from jieba import cut
import method
import os

class TestSimHash(unittest.TestCase):

    def setUp(self):
        # 在每个测试方法运行前创建测试文件
        self.test_file_path = 'test_file.txt'
        with open(self.test_file_path, 'w', encoding='utf-8') as file:
            file.write('测试文件内容')

    def tearDown(self):
        # 在每个测试方法运行后删除测试文件
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_hash_value(self):
        # 测试 hash_value 函数
        s = 'hello'
        expected = int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)
        result = method.hash_value(s)
        self.assertEqual(result, expected, "hash_value 函数的结果不匹配")

    def test_hamming_distance(self):
        # 测试 hamming_distance 函数
        hash1 = 0b10101010
        hash2 = 0b01010101
        expected_distance = bin(hash1 ^ hash2).count('1')
        result = method.hamming_distance(hash1, hash2)
        self.assertEqual(result, expected_distance, "hamming_distance 函数的结果不匹配")

    def test_simhash(self):
        # 测试 simhash 函数
        text = '我 喜欢 编程'
        processed_text = method.preprocess_text(text)
        expected = self.compute_simhash_for_text(processed_text)
        result = method.simhash(text)
        self.assertEqual(result, expected, "simhash 函数的结果不匹配")

    def compute_simhash_for_text(self, text):
        # 辅助函数计算 simhash 值用于测试
        v = [0] * 64
        for word in text.split():
            h = method.hash_value(word)
            for i in range(64):
                if h & (1 << i):
                    v[i] += 1
                else:
                    v[i] -= 1

        fingerprint = 0
        for i in range(64):
            if v[i] >= 0:
                fingerprint |= (1 << i)

        return fingerprint

    def test_read_file(self):
        # 测试 read_file 函数
        result = method.read_file(self.test_file_path)
        self.assertEqual(result, '测试文件内容', "read_file 函数的结果不匹配")

    def test_preprocess_text(self):
        # 测试 preprocess_text 函数
        text = '我 爱 编程，编程很好！'
        expected = '我 爱 编程 编程 很好'
        result = method.preprocess_text(text)
        self.assertEqual(result, expected, "preprocess_text 函数的结果不匹配")

if __name__ == '__main__':
    unittest.main()
