import datetime
from tgmodelclass import TGModule

def a(module: TGModule, *args):
    i(TGModule.TG_API_MSG, args)    

def p(*args):
    i(TGModule.TG_PARSE, args)    

def s(*args):
    i(TGModule.TG_SUBSCRIBE, args)    

def d(*args):
    i(TGModule.TG_DOWNLOAD, args)    



def i(module: TGModule, *args):
    full_str = ""
    for info in args:
        full_str += f" {info}"
    print(f"{datetime.datetime.now().time()} +[{module.value}]: {full_str}")


if __name__ == "__main__":
    i("test")    
    i("test", TGModule.TG_PARSE)    
    i("test", TGModule.TG_SUBSCRIBE)    
    i("test", TGModule.TG_DOWNLOAD)    
