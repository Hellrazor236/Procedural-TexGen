#Python 3.2.x only, mofos
import decimal, math, types
from decimal    import Decimal      as D
from math       import ceil, floor, fabs, modf, cos, sin, tan

#Meant to hold brushes that contain values, colors, etc.
class Number:
    settings = {}
    description = "A value that holds a float"
    def man(cls):
        return " \"value\": A floating point number"
    def draw(cls, info, posX, posY):
        return dict.fromkeys(info.colorspace, cls.settings["value"])
    def __init__(cls, settings):
        try:
            cls.settings["value"] = float(settings["value"])
        except:
            print("WTF is this shit?")
            raise ValueError("Sombody obviously doesn't know what a number is.")

class Color:
    settings = {}
    _cache = {}
    description = "A value that holds a float for individual channels (use the None object as a key for a default value)"
    def man(cls):
        return " Channel[*channels]: A floating point number to be used for that particular channel"
    def draw(cls, info, posX, posY):#Should index be an iterator?
        if "input" in cls.settings:
            try:
                color = cls.settings["input"].draw(info, posX, posY)
            except AttributeError:
                color = {}
                for s in info.colorspace:
                    if type(cls.settings["input"][s]) != float and type(cls.settings["input"][s]) != D:
                        raise TypeError("The imbecile that made this thought that values don't need to be a floating point number")
                    if s in cls.settings["input"]:
                        color[s] = cls.settings["input"][s]
                    else:
                        color[s] = cls.setting["input"][None]
        for s in info.colorspace:
            if s in cls.settings:
                color[s] = settings["Channels"][s]
            else:
                color[s] = settings[None]
        return color
    def __init__(cls, settings):
        cls.settings = settings