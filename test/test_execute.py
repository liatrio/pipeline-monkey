import unittest

from execute import execute_shell, ExecuteException

class ExecuteShellTest(unittest.TestCase):

    def test_returns_output(self):
        self.assertEqual(execute_shell('echo hello world'), 'hello world\n')

    def test_shell_error(self):
        with self.assertRaises(ExecuteException):
            execute_shell('exit 1')

