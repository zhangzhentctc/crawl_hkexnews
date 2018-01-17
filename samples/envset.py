import os

path = os.environ["PATH"]
print("当前PATH变量:",path)
phan = os.getcwd() + "\\bin"
print("phan:", phan)
os.environ["PATH"] = os.environ["PATH"] + ';' + phan
print("当前PATH变量:",os.environ["PATH"])
