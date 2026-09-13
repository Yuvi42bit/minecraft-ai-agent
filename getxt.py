def getxt(file):
    with open(file, "r") as file:
        text = file.read().strip()
    return text
