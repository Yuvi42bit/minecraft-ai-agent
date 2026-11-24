from tools_v2 import *
#run a script
#example script:
# forward(),wait(1),jump(),wait(0.5),stop()
def run(text):
    commands=text.split(",")
    for com in commands(text):
        try:
            eval(com)
        except Exception as exc:
            print(exc)
