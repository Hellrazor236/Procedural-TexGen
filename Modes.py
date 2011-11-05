#Python 3.2.x only, mofos
def _add(a, b, ):
    return a+b

def _multiply(a, b):
    return a*b

def _power(a, b):
    return a**b

def _rpower(a, b):
    return b**a

def _subtract(a, b):
    return a-b

def _rsubtract(a, b):
    return b-a

def _divide(a, b):
    return a/b

def _rdivide(a, b):
    return b/a

def _max(a, b):
    if a > b:
        return a
    else:
        return b

def _min(a, b):
    if a < b:
        return a
    else:
        return b

Modes = {"+": _add, "add": _add, "*": _multiply, "multiply": _multiply, "**": _power, "r**": _rpower, "power": _power,
         "rpower": _power,  "-": _subtract, "r-": _rsubtract, "subtract": _subtract, "rsubtract": _rsubtract,
         "/": _divide, "r/": _rdivide, "divide": _divide, "rdivide": _rdivide, "^": _max, "max": _max, "v": _min,
         "min": _min}