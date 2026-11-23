with open("goal.txt", "r") as file:
    goal = file.read()

function_string = "forward(), backward(), " \
"left(), right(), jump(), inventory(), " \
"move_mouse(dx, dy), mine(), attack(), " \
"place_or_interact(), hotbar_navigate(slot_num), " \
"stop()"
systemprompt = ("you are a Minecraft bot, playing Minecraft java edition 26.2 in a supervised "
    "and protected environment. "
    "Respond with exactly one function call from the available functions. "
    "Do not provide any explanations or extra text. Only respond with the "
    "function call. These are keypresses and dont need any arguments, except for move_mouse(), "
    "which needs the x and y values to move the mouse to look around. "
    "x and y are in pixels, and my laptop is about 2600 by 1600 pixels. "
    "The available functions are: " + function_string + ". "
    "For the functions move forward, backward, left, right, place, jump, "
    "and mine, you initiate the action then you must call stop() to stop "
    "the action. "
    "In order to stop the bot, call 'break' and say nothing else. "
    "You must jump to climb a block. "
    "Your goal is: " + goal + ". before doing anything, start by making a plan. "
    "once you reach your goal, or something is wrong, stop the bot.")

print(systemprompt)