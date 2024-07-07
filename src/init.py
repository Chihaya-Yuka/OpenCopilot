import subprocess

def start(filename:str) -> int:
    return subprocess.call(['python', filename])

start('proxy.py')
start('main.py')
