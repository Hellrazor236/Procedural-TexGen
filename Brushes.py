#Python 3.2.x only, mofos
import decimal, math, types, Base
from decimal    import Decimal      as D
from math       import ceil, floor, fabs, modf, cos, sin, tan

#Meant to hold brushes that create things (shapes, etc.)
class Circle:
    settings = {}
    _cache = {}
    _description = "Draws a color (or stroke) inside a circle, and another outside of it"
    def __init__(cls, settings):
        cls.settings = settings
        cls._cache["r**2"] = settings["radius"]**2
        for s in ("inside", "outside", "border"):
            if s+"color" in settings:
                if hasattr(settings[s+"color"], "draw"):
                    cls._cache[s+"isstroke"] = True
                elif isinstance(settings[s+"color"], dict):
                    cls._cache[s+"isstroke"] = False
                else:
                    raise TypeError("I don't know WTF you tried to pass as "+s+"color, but it ain't gonna work")
    def man(cls):
        return " \"radius\": The radius of the circle\n \"x\": The center along the X axis\n \"y\": The center along the Y axis\n*\"insidecolor\": The color (or stroke) to paint inside the circle\n*\"outsidecolor\": The color (or stroke) to paint outside the circle"
    def draw(cls, info, posX, posY):
        color = {}
        distance = fabs((posX-D(cls.settings["x"]))**2 + (posY-D(cls.settings["y"]))**2)
        s = "in" if distance <= cls._cache["r**2"] else "out"
        try:
            color = cls.settings[s+"sidecolor"].draw(info, posX, posY) if cls._cache[s+"sideisstroke"] else cls.settings[s+"sidecolor"]
        except AttributeError:#Fix this shit!
            color = cls.settings[s+"sidecolor"]
        if "borderthickness" in cls.settings:#Fix this shit!
            if distance - cls._cache["r**2"] >= cls.settings["borderthickness"]:
                color = cls.settings["bordercolor"].draw(info, posX, posY) if cls._cache["borderisstroke"] else cls.settings["bordercolor"]
        return color