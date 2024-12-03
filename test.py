import unittest
from unittest.mock import patch
from io import StringIO
from EquationMaster import *  
import time  # 用于控制函数执行时间

class TestInteractiveMathGame(unittest.TestCase):

    def setUp(self):
        self.valid_numbers = [3, 1, 2, 2]
        self.invalid_expression = "3 + 2 == "  # 修正无效表达式，确保格式符合解析要求
        self.valid_expression = "3 + 1 == 2 + 2"
        self.unsupported_expression = "3 + 1 == 4 + 2"

    @patch('EquationMaster.generate_numbers', return_value=[3, 1, 2, 2])
    def test_generate_numbers(self, mock_generate_numbers):
        """测试在给定范围内生成随机数"""
        numbers = generate_numbers(4, 1, 10)
        self.assertEqual(len(numbers), 4)
        for number in numbers:
            self.assertTrue(1 <= number <= 10)

    def test_parse_and_calculate(self):
        """测试对有效和无效表达式的解析和计算"""
        with self.assertRaises(ValueError):
            parse_and_calculate(self.invalid_expression)
        self.assertTrue(parse_and_calculate(self.valid_expression))

    @patch('EquationMaster.generate_numbers', return_value=[3, 1, 2, 2])
    def test_find_solutions(self, mock_generate_numbers):
        """测试是否可以为给定的数字找到解决方案"""
        start_time = time.time()
        solutions = find_solutions(self.valid_numbers, max_iterations=1000)  # 增加 max_iterations 限制
        # 如果运行时间超过 10 秒，说明可能进入无限循环
        self.assertLess(time.time() - start_time, 10, "find_solutions took too long, possible infinite loop")
        self.assertTrue(len(solutions) > 0, "No valid solution found for the given numbers.")
        for solution in solutions:
            self.assertIn('==', solution)

    @patch('EquationMaster.generate_numbers', return_value=[3, 1, 2, 2])
    def test_generate_valid_numbers(self, mock_generate_numbers):
        """测试生成一组保证有解的数字"""
        try:
            numbers, solutions = generate_valid_numbers(4, 1, 10, max_retries=50)  # 减少最大重试次数
            self.assertEqual(len(numbers), 4)
            self.assertTrue(len(solutions) > 0)
        except RuntimeError:
            self.fail("generate_valid_numbers exceeded maximum retry limit")

    def test_parentheses_handling(self):
        """测试程序在括号计算中的正确性"""
        valid_expression_with_parentheses = "8 * (5 - 2) == 24"
        self.assertTrue(parse_and_calculate(valid_expression_with_parentheses))

        invalid_expression_with_parentheses = "8 * 5 - 2 == 24"
        self.assertFalse(parse_and_calculate(invalid_expression_with_parentheses))

    @patch('EquationMaster.generate_numbers', return_value=[3, 1, 2, 2])
    @patch('builtins.input', side_effect=['4', '1', '10', '3 + 1 == 2 + 2', 'game over'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_success_flow(self, mock_stdout, mock_input, mock_generate_numbers):
        """测试用户输入正确时的主游戏流程"""
        with patch('sys.exit', side_effect=SystemExit):
            try:
                main()
            except SystemExit:
                pass
        output = mock_stdout.getvalue()
        self.assertIn("Congratulations, the equation is correct!", output)

    @patch('EquationMaster.generate_numbers', return_value=[3, 1, 2, 2])
    @patch('builtins.input', side_effect=['4', '1', '10', '3 + 2 +2 == 1', '3 + 2 + 2== 1', '3 + 2 +2 == 1', 'yes','game over'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_provide_solution_after_max_attempts(self, mock_stdout, mock_input, mock_generate_numbers):
        """测试在用户三次错误答案后提供正确答案"""
        with patch('sys.exit', side_effect=SystemExit):
            try:
                main()
            except SystemExit:
                pass
        output = mock_stdout.getvalue()
        self.assertIn("The correct equations are:", output)

    @patch('EquationMaster.generate_numbers', return_value=[3, 1, 2, 2])
    @patch('builtins.input', side_effect=['4', '1', '10', '3 + 2 ==', '3 + 2 ==', '3 + 2 ==', 'maybe', 'maybe', 'maybe'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_again_prompt(self, mock_stdout, mock_input, mock_generate_numbers):
        """测试用户输入无效时重新游戏的提示，并确保在最大尝试次数后结束"""
        with patch('sys.exit', side_effect=SystemExit):
            try:
                main()
            except SystemExit:
                pass
        output = mock_stdout.getvalue()
        self.assertIn("Invalid input. Please enter 'play again' or 'game over'.", output)
        self.assertIn("Maximum invalid attempts reached. Exiting the game.", output)

    def test_priority_with_parentheses(self):
        """测试程序在带有括号优先级的运算时是否正确运行"""
        expression = "(3 + 2) * 5 == 25"
        self.assertTrue(parse_and_calculate(expression))
        
    def test_spaces_handling(self):
        """测试程序在处理带空格与不带空格的输入时的正确性"""
        generated_numbers = [3, 2, 6, 2, 7]
        # 测试含有空格和不含空格的等式是否都被正确解析
        self.assertTrue(parse_and_calculate("3 + 2 == 6 * 2 - 7"))
        self.assertTrue(parse_and_calculate("3+2==6*2-7"))
        self.assertTrue(parse_and_calculate("3 + 2 == 6 * 2 - 7"))
        self.assertTrue(parse_and_calculate("3+2 == 6*2-7"))

if __name__ == '__main__':
    unittest.main(verbosity=2)
