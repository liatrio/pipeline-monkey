import subprocess

class ExecuteException(Exception):
    def __init__(self, error_msg, error_code):
        self.error_msg = error_msg.strip()
        self.error_code = error_code

def execute_shell(script, msg=None):
    if msg:
        print(msg)
        print('-'*30)
    try: 
        res = subprocess.run(['sh', '-c', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        raise ExecuteException(e.stderr.decode('utf-8'), e.returncode)
    else:
        return res.stdout.decode('utf-8')

