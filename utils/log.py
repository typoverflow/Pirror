def printc(color, *texts, **kargs):
    print(color, end="")
    if "sep" in kargs:
        print(*texts, sep=kargs["sep"], end="")
    else:
        print(*texts, end="")
    if "end" in kargs:
        print("\033[0m", end=kargs["end"])
    else:
        print("\033[0m")

def log(color, prompt, text):
    print(color+"【{}】 ".format(prompt)+"\033[0m"+text)