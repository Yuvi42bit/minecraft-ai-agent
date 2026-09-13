from tools_v2 import *

def run(response):
    try:
        eval(response)
    except Exception as e:
        print(e)