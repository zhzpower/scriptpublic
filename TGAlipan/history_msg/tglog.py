"""
打印当前时间和给定模块的值，以及任何附加参数。

参数:
    module (TGModule): 要打印其值的模块。
    *args: 要包含在打印消息中的任何其他参数。

返回:
    无
"""
import datetime
from tgmodelclass import TGModule

def a(*args):
    """
    打印当前时间和给定模块的值，以及任何附加参数。
    """
    i(TGModule.TG_API_MSG, *args)

def p(*args):
    """
    打印当前时间和给定模块的值，以及任何附加参数。
    """
    i(TGModule.TG_PARSE, *args)

def s(*args):
    """
    打印当前时间和给定模块的值，以及任何附加参数。
    """
    i(TGModule.TG_SUBSCRIBE, *args)

def d(*args):
    """
    打印当前时间和给定模块的值，以及任何附加参数。
    """
    i(TGModule.TG_DOWNLOAD, *args)

def i(module: TGModule, *args):
    """
    打印当前时间和给定模块的值，以及任何附加参数。
    """
    try:
        full_str = " ".join(args)
        print(f"{datetime.datetime.now().time()} +[{module.value}]: {full_str}")
    except Exception as e:
        print(f"{datetime.datetime.now().time()} +[{module.value}]: {args}")

if __name__ == "__main__":
    i("test")
    i("test", TGModule.TG_PARSE)
    i("test", TGModule.TG_SUBSCRIBE)
    i("test", TGModule.TG_DOWNLOAD)
