import datetime

colors = {
    "red": "\33[0;31;1m", 
    "yellow": "\33[0;33;1m", 
    "green": "\33[0;32;1m", 
    "blue": "\33[0;34;1m"
}

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
    c = colors[color]
    print(c+"【{}】({}): ".format(prompt, datetime.datetime.strftime(datetime.datetime.now(), "%m-%d %H:%M:%S"))+"\033[0m"+text)