"""
打印当前时间和给定模块的值，以及任何附加参数。

参数:
    module (TGModule): 要打印其值的模块。
    *args: 要包含在打印消息中的任何其他参数。

返回:
    无
"""
import datetime
from .tgmodelclass import TGModule

def a(*args):
    i(TGModule.TG_API_MSG, args)   

def p(*args):
    i(TGModule.TG_PARSE, args)  

def s(*args):
    i(TGModule.TG_SUBSCRIBE, args)

def d(*args):
    i(TGModule.TG_DOWNLOAD, args)   

def i(module: TGModule, *args):
    full_str = " ".join(args)
    print(f"{datetime.datetime.now().time()} +[{module.value}]: {full_str}")

if __name__ == "__main__":
    i("test")
    i("test", TGModule.TG_PARSE)
    i("test", TGModule.TG_SUBSCRIBE)
    i("test", TGModule.TG_DOWNLOAD)

