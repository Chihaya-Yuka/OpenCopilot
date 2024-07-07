import subprocess

def start(filename:str) -> int:
    return subprocess.call(['python', filename])

start('proxy.py')
start('main.py')
print('Copilot is running on http://127.0.0.1:2334.')