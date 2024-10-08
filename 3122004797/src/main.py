import sys
import method
import cProfile
import pstats
import io


def main():
    if len(sys.argv) != 4:
        print("用法: python main.py <原文文件> <抄袭版论文的文件> <答案文件>")
        sys.exit(1)

    original_file, plagiarized_file, output_file = sys.argv[1:4]

    # 读取文件内容
    original_text = method.read_file(original_file)
    plagiarized_text = method.read_file(plagiarized_file)

    # 预处理文本
    original_counter = method.preprocess_text(original_text)
    plagiarized_counter = method.preprocess_text(plagiarized_text)

    # 计算 SimHash 值
    hash1 = method.simhash(original_counter)
    hash2 = method.simhash(plagiarized_counter)

    # 计算汉明距离
    hamming_distance = method.hamming_distance(hash1, hash2)

    # 计算相似度
    max_distance = 64  # SimHash 生成的哈希值长度
    similarity = 1 - hamming_distance / max_distance

    # 写入输出文件
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(f"{similarity:.2f}\n")


if __name__ == "__main__":
    # 开始性能分析
    pr = cProfile.Profile()
    pr.enable()

    main()

    # 结束性能分析
    pr.disable()

    # 输出性能分析结果
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print(s.getvalue())

    # 保存性能分析结果到文件
    pr.dump_stats('profile_output.prof')

