from tools_v2 import *
import time

print("i am the bunny lord and therfore all bunnies must obey me. I will now move the mouse to the right for 5 seconds.")

for i in range(3):
    print(f"Starting in {5 - i} seconds...")
    time.sleep(1)
def move(x,y):
    move_mouse(x, y)
    print("moved")
    time.sleep(0.5)
move(0,0)
