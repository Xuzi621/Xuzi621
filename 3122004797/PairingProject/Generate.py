import random
import Evaluate
from fractions import Fraction

def format_fraction(f):
    # 确保分数是简化过的
    f = f.limit_denominator()  # 自动简化分数
    if f.denominator == 1:  # 如果是整数
        return str(f.numerator)
    elif f.numerator > f.denominator:  # 如果有整数部分
        whole_number = f.numerator // f.denominator
        remainder = f.numerator % f.denominator
        if remainder == 0:  # 没有余数时只返回整数部分
            return str(whole_number)
        else:  # 有余数时返回整数部分和分数部分
            return f"{whole_number}'{remainder}/{f.denominator}"
    else:  # 只有分数部分
        return f"{f.numerator}/{f.denominator}"


def generate_question(rng):
    operators = ['+', '-', '*', '÷']
    num_operators = random.randint(1, 3)

    operands = []
    for _ in range(num_operators + 1):
        if random.choice([True, False]):
            operand = random.randint(1, rng - 1)
        else:
            numerator = random.randint(1, rng - 1)
            denominator = random.randint(1, rng - 1)
            operand = Fraction(numerator, denominator)
        operands.append(Fraction(operand))

    # 随机决定是否在某些操作数之间加括号
    expression = str(operands[0])
    for i in range(num_operators):
        operator = random.choice(operators)
        if random.choice([True, False]) and i < num_operators - 1:  # 在某些情况下加括号
            expression += f" {operator} ({operands[i + 1]})"
        else:
            expression += f" {operator} {operands[i + 1]}"

    try:
        result = Evaluate.evaluate_expression(expression.replace('÷', '/'))
        result = Fraction(result)  # 确保结果为 Fraction
        if result < 0:
            return None, None
        return format_fraction(result), expression
    except ZeroDivisionError:
        return None, None
    except SyntaxError:
        return None, None


def is_unique_expression(expr, existing_expressions):
    normalized_expr = ''.join(sorted(expr.split()))
    return normalized_expr not in existing_expressions


def generate_exercises(num_questions, rng):
    questions = set()
    answers = []
    while len(questions) < num_questions:
        answer, question = generate_question(rng)
        if question and answer and is_unique_expression(question, questions):
            questions.add(question)
            answers.append((answer, question))
    return answers


def write_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        for index, entry in enumerate(data, start=1):  # 添加编号
            f.write(f"{index}.  {entry}\n")  # 写入编号和内容