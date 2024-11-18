import random
import operator
import itertools
import re  # Used to extract numbers from the input

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
    if not re.match(r'^[\d\s\+\-\*/=]+$', equation):
        raise ValueError("Invalid characters in expression")
    
    # 确保表达式包含 '==' 来进行比较
    if '==' not in equation:
        raise ValueError("Expression must include '==' for comparison")

    # 分割左右两侧的表达式
    left_expr, right_expr = equation.split('==')
    
    # 计算左右两侧的值
    left_value = simple_calculate(left_expr.strip())
    right_value = simple_calculate(right_expr.strip())

    # 返回比较结果
    return left_value == right_value

# 计算不带比较的简单数学表达式。
def simple_calculate(expr):
    # 分割表达式中的数字和操作符
    tokens = re.split(r'([\+\-\*/])', expr)
    # 移除空白字符
    tokens = [t.strip() for t in tokens if t.strip()]

    # 将第一个数字初始化为结果
    result = float(tokens.pop(0))

    # 遍历剩余的操作符和数字
    while tokens:
        operator_symbol = tokens.pop(0)
        next_number = float(tokens.pop(0))
        
        # 获取操作符并执行相应的运算
        if operator_symbol in ops:
            result = ops[operator_symbol](result, next_number)
        else:
            raise ValueError(f"Unsupported operator: {operator_symbol}")

    return result


# Explanation of the rules
def print_rules():
    print("Welcome to the Interactive Math Calculation Game!")
    print("Game Rules:")
    print("1. You will be given a set of numbers.")
    print("2. Your task is to place the appropriate operators (addition, subtraction, multiplication, division) between the numbers.")
    print("3. The goal is to create a valid mathematical equation using these numbers and operators.")
    print("4. For example, if given numbers are 3, 1, 3, and 5, you can form an equation like '3 - 1 + 3 == 5'.")
    print("5. You must use the operators to make the equation correct.")
    print("6. Operators to use: '+' for addition, '-' for subtraction, '*' for multiplication, '/' for division.")
    print("7. Use '==' to represent the equality check (e.g., '3 + 2 == 5'). It checks if the two sides of the equation are equal.\n")


# Convert numbers and operators into an expression with parentheses if needed
def format_expression(operators, nums):
    expression = str(nums[0])
    for i in range(1, len(nums)):
        expression += f" {operators[i-1]} {nums[i]}"
    return expression

# Generate random numbers
def generate_numbers(count, min_number, max_number):
    return [random.randint(min_number, max_number) for _ in range(count)]

# Generate an expression with operators and check if it satisfies the equation, ensuring numbers are not reused
def find_solutions(nums):
    solutions = []
    num_operators = len(nums) - 1
    for operators in itertools.product(ops.keys(), repeat=num_operators):
        for perm_nums in itertools.permutations(nums):
            try:
                expression = format_expression(operators, perm_nums)
                if simple_calculate(expression) == simple_calculate('=='.join(map(str, perm_nums))):
                    solutions.append(expression)
            except ZeroDivisionError:
                continue
            except:
                continue
    return solutions

# Extract the numbers and operators from the user's input
def extract_numbers_from_input(user_input):
    return [float(num) for num in re.findall(r'-?\d+\.?\d*', user_input)]

# Ensure the generated set of numbers has a solution, and each number is used only once
def generate_valid_numbers(count, min_number, max_number):
    while True:
        numbers = generate_numbers(count, min_number, max_number)
        solutions = find_solutions(numbers)
        if solutions:
            return numbers, solutions

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

        numbers, solutions = generate_valid_numbers(num_count, min_number, max_number)
        print("\nGenerated numbers:", numbers)
        print("\nYou can use the following operators:")
        print(" '+' for addition")
        print(" '-' for subtraction")
        print(" '*' for multiplication")
        print(" '/' for division")
        print(" '==' to check if the two sides of the equation are equal (e.g., '3 + 2 == 5')\n")

        invalid_attempts = 0
        incorrect_attempts = 0
        max_attempts = 3

        while invalid_attempts < max_attempts and incorrect_attempts < max_attempts:
            user_equation = input("Enter your equation using the numbers and operators provided: ")

            # 验证玩家输入是否符合规则
            user_numbers = extract_numbers_from_input(user_equation)
            if sorted(user_numbers) != sorted(numbers):
                print("Invalid input: You must use all the generated numbers exactly once. Please try again.")
                invalid_attempts += 1
                if invalid_attempts == max_attempts:
                    print("Maximum invalid attempts reached. Game over.")
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
                        show_hint = input("Would you like to see the correct equations? (yes/no): ").strip().lower()
                        if show_hint == 'yes':
                            print("The correct equations are:")
                            for solution in solutions:
                                print(solution)
            except Exception as e:
                print(f"Error in equation: {e}. Please try again.")

        play_again_attempts = 0
        while play_again_attempts < 3:
            play_again_input = input("\nDo you want to play again? (yes/no): ").strip().lower()
            if play_again_input in ['yes', 'no']:
                play_again = play_again_input == 'yes'
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                play_again_attempts += 1
        if play_again_attempts == 3:
            print("Maximum invalid attempts reached. Exiting the game.")
            play_again = False

if __name__ == "__main__":
    main()
