import datetime
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
    print(color+"【{}】({}): ".format(prompt, datetime.datetime.strftime(datetime.datetime.now(), "%m-%d %H:%M:%S"))+"\033[0m"+text)