import os
flag = os.path.exists("first open")
if not flag:
    with open("first open","w+"): pass
if flag: import train
else: import chat
