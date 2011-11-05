#Version 0.006 - Python 3.2.x only, mofos
import decimal, math, copy, os
from decimal    import Decimal as D
from math       import ceil, floor, fabs, modf, cos, sin, tan
LINEINFO = False
PADDING = None#Either an integer or None

class _Info:
    """A class that is used to pass info from one brush to another"""
    colorspace = ""
    resoX, resoY = D("0.00"), D("0.00")#Meant to be updated for zooming, etc.
    def __init__(cls, resoX, resoY, colorspace=""):
        cls.colorspace, cls.resoX, cls.resoY  = colorspace, resoX, resoY

class Texture:
    """A class that holds data about how a texture should render"""
    _sd = {}
    _channels = {}#bytearrays
    input = None
    strokes = None
    def __init__(cls, sizeX, sizeY, dimensionX, dimensionY):
        if sizeX < 1 or sizeY < 1:
            raise ValueError("The person that made this texture (or tried to) is retarded.\n\n Also sizeX or sizeY is less than 1.")
        cls._sd = {"sizeX":int(sizeX), "sizeY":int(sizeY), "dimensionX":(D(dimensionX[0]), D(dimensionX[1])), "dimensionY":(D(dimensionY[0]), D(dimensionY[1])), "resoX":D((D(dimensionX[1])-D(dimensionX[0]))/D(str(sizeX-1))), "resoY":D((D(dimensionY[1])-D(dimensionY[0]))/D(str(sizeY-1)))}
    def render(cls, sizeX=None, sizeY=None, dimensionX=None, dimensionY=None, colorspace="RGBA", bpc=8, thread=(0, 1), altch=None, iterY=None, iterX=None):
        """Asks the input attribute to draw for every sample"""
        print("Thread "+str(thread[0])+" (process "+str(os.getpid()).zfill(4)+") reporting for duty!")
        if cls.input is None: raise TypeError("Some dumbass thinks that you can make an image without painting a stroke. What is this, modern art?")
        if bpc > 8: raise ValueError("You can't have more than one byte per channel (mostly because I can't figure out how to do it without fucking everything up; I would gladly let you do this if I could)")
        maxvalue = (2**bpc)-1
        padto = len(str(sizeY)) if PADDING is None else PADDING
        q = {"sizeX":sizeX, "sizeY":sizeY, "dimensionX":dimensionX, "dimensionY":dimensionY,#This needs to be seperate:
             "resoX":D((D(dimensionX[1])-D(dimensionX[0]))/D(str(sizeX-1))) if (dimensionX is not None and sizeX is not None) else None, "resoY":D((D(dimensionY[1])-D(dimensionY[0]))/D(str(sizeY-1))) if (dimensionY is not None and sizeY is not None) else None}
        sd = cls._sd#Figure out how to merge with line 34?
        sd.update(dict((k, v) for k, v in q.items() if v is not None))
        if hasattr(cls.input, "draw"):
            isstroke = True
        elif isinstance(cls.input, dict):
            isstroke = False
        else:
            raise TypeError("I don't know what the hell you just tried to pass as input, but it ain't gonna work")
        for s in "XY":
            sd["dimension"+s] = (D(sd["dimension"+s][0]), D(sd["dimension"+s][1]))
            sd["reso"+s] = D((D(sd["dimension"+s][1])-D(sd["dimension"+s][0]))/D(str(sd["size"+s]-1)))#Is this needed?
        info = _Info(sd["resoX"], sd["resoY"], colorspace)
        channels = cls._channels if altch is None else altch
        if altch is None:
            b = bytearray.fromhex("00"*sd["sizeX"]*sd["sizeY"])#I'm sure this can be faster
            for s in colorspace:
                cls._channels[s] = copy.copy(b)
        for iY in range(sd["sizeY"]-thread[0]-1, -1, -thread[1]) if iterY is None else iterY:#Figure out how to make it render algebraically (bottom up)
            fY = sd["dimensionY"][1]-(iY*sd["resoY"])
            for iX in (range(sd["sizeX"]) if iterX is None else iterX):
                fX = sd["dimensionX"][1]-(iX*sd["resoX"])#Only gets used once, is it necessary to make it a variable?
                color = cls.input.draw(info, fX, fY) if isstroke else cls.input
                for s in colorspace: channels[s][(iY*sd["sizeY"])+iX] = ceil((color[s]*maxvalue)-.5)
                if iX == sd["sizeX"]-1 and LINEINFO is True:
                    print(str(os.getpid()).zfill(4)+": "+str(iY).zfill(padto)+"@"+("" if fY < 0 else " ")+str(fY)+" cm Y")
        return (cls._channels if thread[1] == 1 else None)
    def draw(cls, info, posX, posY):
        if cls._channels == {}:#Make sure it's already rendered
            cls.render()
        if (posX <= cls._sd["dimensionX"][0] and posX >= cls._sd["dimensionX"][1]) or (posY <= cls._sd["dimensionY"][0] and posY >= cls._sd["dimensionY"][1]):
            return {}
        else:
            pass#Figure out which sample is needed and return it.
    def clearBuffer(cls):
        """Clears the channel buffers"""
        cls._channels = {}
    def getBuffer(cls):
        """Returns the channel buffers"""
        return copy.copy(cls._channels)
