import random
import operator
import itertools
import re  # Used to extract numbers from the input

#  Define operators
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

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


# Function to determine if parentheses are needed based on operator precedence
def needs_parentheses(prev_op, current_op):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    return precedence[current_op] > precedence[prev_op]

# Convert numbers and operators into an expression with parentheses if needed
def format_expression(operators, nums):
    expression = str(nums[0])
    for i in range(1, len(nums)):
        if i > 1 and needs_parentheses(operators[i-2], operators[i-1]):
            expression = f"({expression})"
        expression += f" {operators[i-1]} {nums[i]}"
    return expression

# Generate random numbers
def generate_numbers(count, min_number, max_number):
    return [random.randint(min_number, max_number) for _ in range(count)]

# Generate an expression with operators and check if it satisfies the equation, ensuring numbers are not reused
def find_solution(nums):
    num_operators = len(nums) - 1
    for operators in itertools.product(ops.keys(), repeat=num_operators):
        # Generate all possible number permutations, ensuring each number is used only once
        for perm_nums in itertools.permutations(nums):
            try:
                # Assign numbers and operators to the left and right parts of the equation
                for split_point in range(1, len(perm_nums)):
                    left_expr = str(perm_nums[0])
                    for i in range(1, split_point):
                        left_expr += f" {operators[i-1]} {perm_nums[i]}"
                    
                    right_expr = str(perm_nums[split_point])
                    for i in range(split_point + 1, len(perm_nums)):
                        right_expr += f" {operators[i-1]} {perm_nums[i]}"
                    
                    # Evaluate both sides of the equation
                    if eval(left_expr) == eval(right_expr):
                        return f"{left_expr} == {right_expr}"
            except ZeroDivisionError:
                continue  # Avoid division by zero
            except:
                continue  # Ignore other exceptions

    return None


# Extract the numbers and operators from the user's input
def extract_numbers_from_input(user_input):
    # # Use regex to extract all numbers, supporting negative numbers and floats
    return [float(num) for num in re.findall(r'-?\d+\.?\d*', user_input)]

# Ensure the generated set of numbers has a solution, and each number is used only once
def generate_valid_numbers(count, min_number, max_number):
    while True:
        numbers = generate_numbers(count, min_number, max_number)
        solution = find_solution(numbers)
        if solution:
            return numbers, solution


# Main game loop
def main():
     # Explain the rules
    print_rules()

    play_again = True
    while play_again:
        # Get the number of numbers from the user
        try:
            num_count = int(input("Enter the number of numbers to generate for the equation (e.g., 4): "))
            if num_count < 2:
                raise ValueError("Number of numbers must be at least 2.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        # Get the range of numbers from the user
        try:
            min_number = int(input("Enter the minimum number for the range: "))
            max_number = int(input("Enter the maximum number for the range: "))
            if min_number > max_number:
                raise ValueError("Minimum number cannot be greater than maximum number.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        # Generate numbers and the corresponding solution
        numbers, solution = generate_valid_numbers(num_count, min_number, max_number)
        print("\nGenerated numbers:", numbers)
        print("\nou can use the following operators:")
        print(" '+' for addition")
        print(" '-' for subtraction")
        print(" '*' for multiplication")
        print(" '/' for division")
        print(" '==' to check if the two sides of the equation are equal (e.g., '3 + 2 == 5')\n")

        # Provide a limited number of attempts
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            # # Get the user's equation input
            user_equation = input("Enter your equation using the numbers and operators provided: ")

            # Check if the user used all the generated numbers and operators
            def check_user_input(user_numbers, user_operators, generated_numbers, generated_operators):
                # Check if all numbers were used
                if sorted(user_numbers) != sorted(generated_numbers):
                    return False, "You must use all the generated numbers."

         
            # Check if the user's equation is correct
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

        # Ask the user if they want to play again
        play_again_input = input("\nDo you want to play again? (yes/no): ").strip().lower()
        play_again = play_again_input == 'yes'

if __name__ == "__main__":
    main()
