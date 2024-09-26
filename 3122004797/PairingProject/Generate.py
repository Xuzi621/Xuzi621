import random
import Evaluate
from fractions import Fraction

def format_fraction(f):
    # 格式化分数为字符串
    f = f.limit_denominator()  # 简化分数
    if f.denominator == 1:  # 如果是整数
        return str(f.numerator)
    elif f.numerator > f.denominator:  # 有整数部分
        whole_number = f.numerator // f.denominator
        remainder = f.numerator % f.denominator
        if remainder == 0:  # 没有余数
            return str(whole_number)
        else:  # 有余数
            return f"{whole_number}'{remainder}/{f.denominator}"
    else:  # 只有分数部分
        return f"{f.numerator}/{f.denominator}"

def generate_question(rng):
    # 生成数学题目和答案
    operators = ['+', '-', '*', '÷']
    num_operators = random.randint(1, 3)  # 随机操作符数量

    operands = []
    for _ in range(num_operators + 1):
        if random.choice([True, False]):
            operand = random.randint(1, rng - 1)  # 整数操作数
        else:
            numerator = random.randint(1, rng - 1)
            denominator = random.randint(1, rng - 1)
            operand = Fraction(numerator, denominator)  # 分数操作数
        operands.append(Fraction(operand))

    # 构建表达式
    expression = str(operands[0])
    for i in range(num_operators):
        operator = random.choice(operators)
        if random.choice([True, False]) and i < num_operators - 1:  # 随机加括号
            expression += f" {operator} ({operands[i + 1]})"
        else:
            expression += f" {operator} {operands[i + 1]}"

    try:
        result = Evaluate.evaluate_expression(expression.replace('÷', '/'))  # 计算结果
        result = Fraction(result)  # 确保结果是分数
        if result < 0:  # 负数不合要求
            return None, None
        return format_fraction(result), expression  # 返回格式化结果和表达式
    except ZeroDivisionError:
        return None, None  # 处理除零错误
    except SyntaxError:
        return None, None  # 处理语法错误

def is_unique_expression(expr, existing_expressions):
    # 检查表达式是否唯一
    normalized_expr = ''.join(sorted(expr.split()))  # 标准化表达式
    return normalized_expr not in existing_expressions  # 不在已有表达式中

def generate_exercises(num_questions, rng):
    # 生成指定数量的题目和答案
    questions = set()
    answers = []
    while len(questions) < num_questions:
        answer, question = generate_question(rng)  # 生成题目
        if question and answer and is_unique_expression(question, questions):  # 检查唯一性
            questions.add(question)
            answers.append((answer, question))  # 存储答案和题目
    return answers  # 返回所有题目和答案

def write_to_file(filename, data):
    # 将数据写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        for index, entry in enumerate(data, start=1):  # 添加编号
            f.write(f"{index}.  {entry}\n")  # 写入编号和内容
