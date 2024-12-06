import random
import operator
import itertools
import re  # Used to extract numbers from the input
import ast  # Used to safely parse expressions without eval
import time  # 用于控制函数执行时间

# Define operators
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}


# 解析和计算简单的数学表达式，不使用 eval。仅支持 +, -, *, / 四种操作符。
def parse_and_calculate(equation):
    # 验证表达式是否仅包含数字、空格和支持的操作符（包括'=='）
    if not re.match(r'^[\d\s\+\-\*/\(\)=]+$', equation):
        raise ValueError("Invalid characters in expression")
    
    # 确保表达式包含 '==' 来进行比较
    if '==' not in equation:
        raise ValueError("Expression must include '==' for comparison")

    # 分割左右两侧的表达式
    left_expr, right_expr = equation.split('==')
    
    # 计算左右两侧的值
    left_value = evaluate_expression(left_expr.strip())
    right_value = evaluate_expression(right_expr.strip())

    # 返回比较结果
    return left_value == right_value

# 计算带括号的数学表达式。
def evaluate_expression(expr):
    try:
        # 使用 ast.literal_eval 安全地解析表达式
        node = ast.parse(expr, mode='eval').body
        return evaluate_ast(node)
    except (SyntaxError, ValueError, TypeError):
        raise ValueError("Invalid mathematical expression")

# 递序计算 AST 节点值
def evaluate_ast(node):
    if isinstance(node, ast.BinOp):
        left = evaluate_ast(node.left)
        right = evaluate_ast(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise ZeroDivisionError("division by zero")
            return left / right
    elif isinstance(node, ast.Constant):
        return node.value
    else:
        raise ValueError("Unsupported expression")

# Explanation of the rules
def print_rules():
    print("Welcome to the Interactive Math Calculation Game!")
    print("Game Rules:")
    print("1. You will be given a set of numbers.")
    print("2. Your task is to place the appropriate operators (addition, subtraction, multiplication, division) between the numbers in the given order.")
    print("3. The goal is to create a valid mathematical equation using these numbers and operators.")
    print("4. For example, if given numbers are 3, 1, 3, and 5, you can form an equation like '3 - 1 + 3 == 5'.")
    print("5. You must use the operators to make the equation correct.")
    print("6. Operators to use: '+' for addition, '-' for subtraction, '*' for multiplication, '/' for division.")
    print("7. Use '==' to represent the equality check (e.g., '3 + 2 == 5'). It checks if the two sides of the equation are equal.")
    print("8. You can also use parentheses to change the order of operations, e.g., '(3 + 2) * 5 == 25'.\n")

# Convert numbers and operators into an expression with parentheses if needed
def format_expression(operators, nums):
    # 确保数字和操作符之间有空格
    tokens = []
    for i, num in enumerate(nums):
        tokens.append(str(num))
        if i < len(operators):
            tokens.append(operators[i])
    expression = " ".join(tokens)  # 数字与运算符之间用空格
    return expression



# Generate random numbers
def generate_numbers(count, min_number, max_number):
    return [random.randint(min_number, max_number) for _ in range(count)]

# Generate an expression with operators and check if it satisfies the equation, ensuring numbers are used in order
def find_solutions(nums, max_iterations=1000):
    solutions = []
    iteration = 0
    n = len(nums)
    
    # 如果长度小于2，无法构成等式
    if n < 2:
        return solutions

    # 尝试在 nums 中的任意位置插入 '=='
    # 例如 nums = [3, 1, 2, 2]
    # split_pos = 1 -> 左侧: [3], 右侧: [1, 2, 2]
    # split_pos = 2 -> 左侧: [3, 1], 右侧: [2, 2]
    # split_pos = 3 -> 左侧: [3, 1, 2], 右侧: [2]
    for split_pos in range(1, n):
        left_nums = nums[:split_pos]
        right_nums = nums[split_pos:]

        left_ops_count = len(left_nums) - 1
        right_ops_count = len(right_nums) - 1

        # 遍历左侧的所有操作符组合
        for left_ops in itertools.product(ops.keys(), repeat=left_ops_count):
            left_expr = format_expression(left_ops, left_nums)
            left_result = evaluate_expression(left_expr)
            if left_result is None:
                continue

            # 遍历右侧的所有操作符组合
            for right_ops in itertools.product(ops.keys(), repeat=right_ops_count):
                right_expr = format_expression(right_ops, right_nums)
                right_result = evaluate_expression(right_expr)
                if right_result is None:
                    continue

                # 检查左右两侧结果是否相等
                # 同时检查最终从整个表达式中提取的数字集是否与 nums 匹配
                if left_result == right_result:
                    combined_expr = f"{left_expr} == {right_expr}"
                    solution_numbers = [int(num) for num in re.findall(r'-?\d+', combined_expr)]
                    if sorted(solution_numbers) == sorted(nums):
                        solutions.append(combined_expr)
                        
                iteration += 1
                if iteration > max_iterations:
                    return solutions

    return solutions


# Extract the numbers and operators from the user's input
def extract_numbers_from_input(user_input):
    return [float(num) for num in re.findall(r'-?\d+\.?\d*', user_input)]


# Ensure the generated set of numbers has a solution, and each number is used in the given order
def generate_valid_numbers(count, min_number, max_number, max_retries=50):
    retries = 0

    while retries < max_retries:
        retries += 1
        numbers = generate_numbers(count, min_number, max_number)
        solutions = find_solutions(numbers)

        if solutions:
            return numbers, solutions

    raise RuntimeError("Exceeded maximum retry limit, unable to generate valid numbers with a solution.")

# Main game loop
def main():
    print_rules()

    play_again = True
    while play_again:
        try:
            num_count = int(input("Enter the number of numbers to generate for the equation (e.g., 4): "))
            if num_count < 2:
                raise ValueError("Number of numbers must be at least 2.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        try:
            min_number = int(input("Enter the minimum number for the range: "))
            max_number = int(input("Enter the maximum number for the range: "))
            if min_number > max_number:
                raise ValueError("Minimum number cannot be greater than maximum number.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        try:
            numbers, solutions = generate_valid_numbers(num_count, min_number, max_number)
        except RuntimeError as e:
            print(e)
            continue

        print("\nGenerated numbers:", numbers)
        print("\nYou can use the following operators:")
        print(" '+' for addition")
        print(" '-' for subtraction")
        print(" '*' for multiplication")
        print(" '/' for division")
        print(" '==' to check if the two sides of the equation are equal (e.g., '3 + 2 == 5')")
        print(" You can also use parentheses to change the order of operations.\n")

        invalid_attempts = 0
        incorrect_attempts = 0
        max_attempts = 3

        while invalid_attempts < max_attempts and incorrect_attempts < max_attempts:
            user_equation = input("Enter your equation using the numbers and operators provided: ")
            user_equation = re.sub(r'(\+|\-|\*|/)', r' \1 ', user_equation)

            # 现在提取数字会更稳定
            user_numbers = extract_numbers_from_input(user_equation)

            # 验证玩家输入是否符合规则
            user_numbers = extract_numbers_from_input(user_equation)
            if sorted(user_numbers) != sorted(numbers):
                print("Invalid input: You must use all the generated numbers in the given order. Please try again.")
                invalid_attempts += 1
                if invalid_attempts == max_attempts:
                    print("Maximum invalid attempts reached. Game over.")
                    if solutions:
                        print("The correct equations are:")
                        for solution in solutions:
                            print(solution)
                    break
                continue

            try:
                if parse_and_calculate(user_equation):
                    print("Congratulations, the equation is correct!")
                    break
                else:
                    print("The equation is incorrect or not valid. Please try again.")
                    incorrect_attempts += 1
                    if incorrect_attempts == max_attempts:
                        print("Maximum incorrect attempts reached.")
                        if solutions:
                            print("The correct equations are:")
                            for solution in solutions:
                                print(solution)
            except Exception as e:
                print(f"Error in equation: {e}. Please try again.")

        play_again_attempts = 0
        while play_again_attempts < 3:
            play_again_input = input("\nPlay again or game over? (play again/game over): ").strip().lower()
            if play_again_input in ['play again', 'game over']:
                if play_again_input == 'game over':
                    print("Game over.")
                play_again = play_again_input == 'play again'
                break
            else:
                print("Invalid input. Please enter 'play again' or 'game over'.")
                play_again_attempts += 1
        if play_again_attempts == 3:
            print("Maximum invalid attempts reached. Exiting the game.")
            play_again = False

if __name__ == "__main__":
    main()
