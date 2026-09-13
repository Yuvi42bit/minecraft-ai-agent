from tools import *
import time

print("i am the bunny lord and therfore all bunnies must obey me. I will now move the mouse to the right for 5 seconds.")

for i in range(5):
    print(f"Starting in {5 - i} seconds...")
    time.sleep(1)

move_mouse(1500, 0)