import Generate

def parse_mixed_number(mixed_str):
    # 解析混合数为分数对象
    if "'" in mixed_str:
        whole, frac = mixed_str.split("'")  # 分离整数和分数
        whole = int(whole)
        numerator, denominator = map(int, frac.split('/'))  # 分子分母转换
        return Generate.Fraction(whole) + Generate.Fraction(numerator, denominator)
    else:
        return Generate.Fraction(mixed_str)  # 直接返回分数

def evaluate_expression(expression):
    # 计算数学表达式，返回结果为分数对象
    result = Generate.Fraction(0)
    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()
    stack = []
    current_op = '+'

    for token in tokens:
        if token in '+-*/':
            current_op = token
        elif token == '(':
            stack.append(current_op)
            current_op = '+'
        elif token == ')':
            if stack:
                current_op = stack.pop()
        else:
            value = Generate.Fraction(token)
            if current_op == '+':
                result += value
            elif current_op == '-':
                result -= value
            elif current_op == '*':
                result *= value
            elif current_op == '/':
                result /= value

    return result  # 返回计算结果

def grade_exercises(exercise_file, answer_file):
    # 评估练习题的答案
    with open(exercise_file, 'r') as ef, open(answer_file, 'r') as af:
        exercises = ef.readlines()
        answers = af.readlines()

    correct = []
    wrong = []

    for i, (exercise, answer) in enumerate(zip(exercises, answers)):
        exercise = exercise.strip().split(' ', 1)[-1]
        answer = answer.strip()

        exercise = exercise.replace('梅', '/')  # 替换特殊符号

        try:
            eval_answer = evaluate_expression(exercise)  # 计算答案
            parsed_answer = parse_mixed_number(answer)  # 解析答案

            if eval_answer == parsed_answer:
                correct.append(i + 1)  # 正确答案
            else:
                wrong.append(i + 1)  # 错误答案
        except ZeroDivisionError:
            print(f"ZeroDivisionError on Exercise {i + 1}")
            wrong.append(i + 1)
        except Exception as e:
            print(f"Error on Exercise {i + 1}: {e}")
            wrong.append(i + 1)

    return correct, wrong  # 返回正确和错误的题目编号