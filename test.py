import unittest
from io import StringIO
from unittest.mock import patch
import re  # If needed for extracting numbers

# Import functions from EquationMaster
from EquationMaster import *


class TestInteractiveMathGame(unittest.TestCase):
    def test_generate_numbers(self):
        """Test the generation of random numbers within a specified range."""
        numbers = generate_numbers(4, 1, 10)
        self.assertEqual(len(numbers), 4)
        for number in numbers:
            self.assertTrue(1 <= number <= 10)

    def test_find_solution(self):
        """Test finding a solution for a simple set of numbers."""
        numbers = [3, 1, 2, 5]
        solution = find_solution(numbers)
        self.assertIsNotNone(solution)
        # Ensure the solution is formatted correctly with equality
        self.assertIn('==', solution)

    def test_extract_numbers_from_input(self):
        """Test extracting numbers from a user-provided string."""
        user_input = "3 + 1 == 4"
        extracted_numbers = extract_numbers_from_input(user_input)
        self.assertEqual(extracted_numbers, [3, 1, 4])

    def test_generate_valid_numbers(self):
        """Test generating a set of numbers with a guaranteed solution."""
        numbers, solution = generate_valid_numbers(4, 1, 10)
        self.assertEqual(len(numbers), 4)
        self.assertIsNotNone(solution)


    def test_format_expression(self):
        """Test the correct formatting of expressions with and without parentheses."""
        operators = ['+', '*']
        nums = [2, 3, 4]
        formatted_expression = format_expression(operators, nums)
        self.assertEqual(formatted_expression, "2 + 3 * 4")

    @patch('builtins.input', side_effect=['4', '1', '10', '3 + 2 == 5', 'no'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_game_success(self, mock_stdout, mock_input):
        """Test the main game flow with a correct user input."""
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Congratulations, the equation is correct!", output)

    @patch('builtins.input', side_effect=['4', '1', '10', '3 + 3 == 5', '3 + 3 == 5', '3 + 3 == 5', 'yes', 'no'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_game_failure(self, mock_stdout, mock_input):
        """Test the main game flow with an incorrect user input, then asking for the solution."""
        main()
        output = mock_stdout.getvalue()
        self.assertIn("The correct equation is:", output)
    def test_unsafe_expression(self):
        """Test for unsafe expressions with code injection attempts."""
        unsafe_expression = "3 + 3 == print('hacked')"
        with self.assertRaises(ValueError) as context:
            parse_and_calculate(unsafe_expression)
        self.assertIn("Invalid characters in expression", str(context.exception))

    @patch('builtins.input', side_effect=['4', '1', '10', '3 + 2 == 5','no'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_game_success(self, mock_stdout, mock_input):
        """Test the main game flow with a correct user input."""
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Congratulations, the equation is correct!", output)

    @patch('builtins.input', side_effect=['4', '1', '10', '3 + 3 == 5','3 + 3 == 5','3 + 3 == 5', 'yes', 'no'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_game_failure(self, mock_stdout, mock_input):
        """Test the main game flow with an incorrect user input, then asking for the solution."""
        main()
        output = mock_stdout.getvalue()
        self.assertIn("The correct equation is:", output)



if __name__ == "__main__":
    unittest.main()
