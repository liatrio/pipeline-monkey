import subprocess


class ExecuteException(Exception):
    def __init__(self, error_msg, error_code):
        self.error_msg = error_msg.strip()
        self.error_code = error_code

def execute_shell(script):
    """
    Runs script as a subprocess and returns decoded output.
    Raises ExecuteException on error.
    """
    try: 
        res = subprocess.run(['sh', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        raise ExecuteException(e.stderr.decode('utf-8'), e.returncode)
    else:
        return res.stdout.decode('utf-8')

def execute_shell_with_output(script, msg=None):
    """
    Wrapper for `execute_shell` that provides console output.
    """
    if msg:
        print(msg)
        print('-'*30)
    try:
        output = execute_shell(script)
    except ExecuteException as e:
        print('Error ({}): {}'.format(e.error_code, e.error_msg))
        raise e
    else:
        print(output)
