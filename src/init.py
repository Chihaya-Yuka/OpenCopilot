import _thread
import subprocess

def start(filename:str) -> int:
    return subprocess.call(['python', filename])

print('Copilot is running on http://127.0.0.1:2334.')
_thread.start_new_thread(start,('main.py',))
_thread.start_new_thread(start,('proxy.py',))
while True: pass