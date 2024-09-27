import random
import operator
import itertools
import re  # 用于从输入中提取数字

# 定义运算符
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

#规则讲解
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


# 优先级比较函数，决定是否需要添加括号
def needs_parentheses(prev_op, current_op):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    return precedence[current_op] > precedence[prev_op]

# 将数字和运算符转化为带括号的表达式
def format_expression(operators, nums):
    expression = str(nums[0])
    for i in range(1, len(nums)):
        if i > 1 and needs_parentheses(operators[i-2], operators[i-1]):
            expression = f"({expression})"
        expression += f" {operators[i-1]} {nums[i]}"
    return expression

# 生成随机数字
def generate_numbers(count, min_number, max_number):
    return [random.randint(min_number, max_number) for _ in range(count)]

# 根据运算符生成表达式并检查是否满足等式，确保数字不重复使用
def find_solution(nums):
    num_operators = len(nums) - 1
    for operators in itertools.product(ops.keys(), repeat=num_operators):
        # 生成所有可能的数字排列，确保每个数字只使用一次
        for perm_nums in itertools.permutations(nums):
            try:
                # 将数字和运算符分配到左右两部分
                for split_point in range(1, len(perm_nums)):
                    left_expr = str(perm_nums[0])
                    for i in range(1, split_point):
                        left_expr += f" {operators[i-1]} {perm_nums[i]}"
                    
                    right_expr = str(perm_nums[split_point])
                    for i in range(split_point + 1, len(perm_nums)):
                        right_expr += f" {operators[i-1]} {perm_nums[i]}"
                    
                    # 计算左右两部分
                    if eval(left_expr) == eval(right_expr):
                        return f"{left_expr} == {right_expr}"
            except ZeroDivisionError:
                continue  # 避免除以0的情况
            except:
                continue  # 忽略其他异常

    return None


# 从用户输入中提取使用的数字和运算符
def extract_numbers_from_input(user_input):
    # 使用正则表达式提取所有数字，支持负数和浮点数
    return [float(num) for num in re.findall(r'-?\d+\.?\d*', user_input)]

# 确保生成的数字集合有解，且每个数字只能用一次
def generate_valid_numbers(count, min_number, max_number):
    while True:
        numbers = generate_numbers(count, min_number, max_number)
        solution = find_solution(numbers)
        if solution:
            return numbers, solution


# 游戏主循环
def main():
     # 讲解规则
    print_rules()

    play_again = True
    while play_again:
        # 获取用户输入的数字数量
        try:
            num_count = int(input("Enter the number of numbers to generate for the equation (e.g., 4): "))
            if num_count < 2:
                raise ValueError("Number of numbers must be at least 2.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        # 获取用户输入的数字范围
        try:
            min_number = int(input("Enter the minimum number for the range: "))
            max_number = int(input("Enter the maximum number for the range: "))
            if min_number > max_number:
                raise ValueError("Minimum number cannot be greater than maximum number.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        # 生成数字和对应的解
        numbers, solution = generate_valid_numbers(num_count, min_number, max_number)
        print("\nGenerated numbers:", numbers)
        print("\nou can use the following operators:")
        print(" '+' for addition")
        print(" '-' for subtraction")
        print(" '*' for multiplication")
        print(" '/' for division")
        print(" '==' to check if the two sides of the equation are equal (e.g., '3 + 2 == 5')\n")

        # 提供尝试次数
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            # 获取用户输入的等式
            user_equation = input("Enter your equation using the numbers and operators provided: ")

            # 检查用户是否使用了所有生成的数字和运算符
            def check_user_input(user_numbers, user_operators, generated_numbers, generated_operators):
                # 检查是否使用了所有数字
                if sorted(user_numbers) != sorted(generated_numbers):
                    return False, "You must use all the generated numbers."

         
            # 检查用户输入的等式是否正确
            try:
                if eval(user_equation):
                    print("Congratulations, the equation is correct!")
                    break
                else:
                    print("The equation is incorrect or not valid. Please try again.")
            except Exception as e:
                print(f"Error in equation: {e}. Please try again.")

            attempts += 1
            if attempts == max_attempts:
                show_hint = input("Would you like the answer? (yes/no): ").strip().lower()
                if show_hint == 'yes':
                    print(f"The correct equation is: {solution}")

        # 询问用户是否继续游戏
        play_again_input = input("\nDo you want to play again? (yes/no): ").strip().lower()
        play_again = play_again_input == 'yes'

if __name__ == "__main__":
    main()
