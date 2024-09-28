import argparse
import Evaluate
import Generate
import cProfile
import sys
import pstats
import io
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser(description="生成和评分算术练习题。")
    parser.add_argument('-n', type=int, help='生成题目的数量')
    parser.add_argument('-r', type=int, help='题目数字的范围')
    parser.add_argument('-e', type=str, help='输入练习题文件以进行评分')
    parser.add_argument('-a', type=str, help='输入答案文件以进行评分')
    return parser.parse_args()


def main():
    args = parse_args()

    # 使用 cProfile 进行性能分析
    pr = cProfile.Profile()
    pr.enable()  # 开始性能分析

    if args.n is not None and args.r is not None:
        # 检查参数是否大于0
        if args.n <= 0:
            print("错误：参数 n 必须大于 0。")
        if args.r < 0:
            print("错误：参数 r 必须大于或等于 0。")
            sys.exit(1)


        # 生成题目
        exercises = Generate.generate_exercises(args.n, args.r)
        Generate.write_to_file("Exercises.txt", [f"{q[1]}" for q in exercises])
        Generate.write_to_file("Answers.txt", [q[0] for q in exercises])
        print(f"已生成 {args.n} 道题目，保存在 Exercises.txt 和 Answers.txt 中。")

    elif args.e is not None and args.a is not None:
        # 评分
        correct, wrong = Evaluate.grade_exercises(args.e, args.a)

        # 统计正确和错误的题号
        correct_count = len(correct)
        wrong_count = len(wrong)

        # 输出到 Grade.txt 文件
        with open("Grade.txt", "w") as file:
            file.write(f"Correct: {correct_count} ({', '.join(map(str, correct))})\n")
            file.write(f"Wrong: {wrong_count} ({', '.join(map(str, wrong))})\n")

        print(f"评分结果已保存到 Grade.txt 中。")

    else:
        print("请提供有效的参数。")

    pr.disable()  # 停止性能分析
    # 将性能分析结果保存到二进制文件
    pr.dump_stats("profile_data.prof")  # 保存为 .prof 文件


if __name__ == "__main__":
    main()
