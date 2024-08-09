import os

commands = ['openai api fine_tunes.create -t model/data.json -m gpt-4-32k-0314']

for command in commands:
    os.system(command)