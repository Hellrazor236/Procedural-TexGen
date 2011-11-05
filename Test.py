import Base
import itertools, math, multiprocessing, copy
import Values as V
import Brushes as B
import TARGA
from multiprocessing import Process
Cores = 2

Size = 10
print("Going over some basics:\nInit:")
TexA = Base.Texture(Size, Size, ("-1.00", "1.00"), ("-1.00", "1.00"))
TexA.strokes = (V.Number({"value":0.5}),)
TexA.input = B.Circle({"outsidecolor":TexA.strokes[0], "radius":.5, "x":0.00, "y":0.00, "insidecolor":{"R":1.00, "G":0.00, "B":0.00, "outsidecolor":TexA.strokes[0]}})
print("Init finished, rendering:")
Picture = TexA.render(colorspace="RGB")
spititout = input("Rendering finished, print?")
if spititout.lower() == "y" or spititout.lower() == "ye" or spititout.lower() == "yes" or spititout.lower() == "yep" or spititout.lower() == "t" or spititout.lower() == "true":
    for y in range(int(len(Picture["R"])/Size)):
        line = []
        for x in range(Size):
            line.append(str(Picture["R"][x+(y*Size)]).zfill(3)+"|"+str(Picture["G"][x+(y*Size)]).zfill(3)+"|"+str(Picture["B"][x+(y*Size)]).zfill(3))
        print(line)
TexA.clearBuffer()
print("TARGA file:")
w = TARGA.makeTARGA(sizeX=Size, sizeY=Size, raster=Picture)
file = open("Out1.tga", "wb")
file.write(w)
file.close()
del Picture, spititout

print("\n\nGoing over advanced stuff (like rendering upside-down)\nInit: ")
Base.LINEINFO = True
BigSize = Size*2
BigBPC = 8
Bytes = math.ceil(BigBPC/8)
TexB = Base.Texture(Size, Size, ("1.00", "-1.00"), ("1.00", "-1.00"))#Note the dimensions are reversed
Outsidestrokes = (B.Circle({"insidecolor":{"R":.5, "G":0.0, "B":1.00}, "outsidecolor":{"R":0.00, "G":0.00, "B":0.25}, "radius":.5, "x":.3, "y":.3}), )
TexB.input = B.Circle({"radius":.5, "x":0.0, "y":0.0, "insidecolor":{"R":1.00, "G":0.00, "B":0.00}, "outsidecolor":Outsidestrokes[0]})
print(TexB.input.man())
print("Init finished, rendering:")
Picture = TexB.render(sizeX=BigSize, sizeY=BigSize, dimensionX=("2.00", "-2.00"), dimensionY=("2.00", "-2.00"), colorspace="RGB", bpc=BigBPC)#Still reversedTexB.clearBuffer()
spititout = input("Rendering finished, print?")
if spititout.lower() == "y" or spititout.lower() == "ye" or spititout.lower() == "yes" or spititout.lower() == "yep" or spititout.lower() == "t" or spititout.lower() == "true":
    for y in range(int(len(Picture["R"])/(BigSize))):
        line = []
        for x in range(BigSize):
            index = (x+(y*BigSize))*Bytes
            line.append(str(Picture["R"][index]).zfill(3)+"|"+str(Picture["G"][index]).zfill(3)+"|"+str(Picture["B"][index]).zfill(3))
        print(line)
del Picture, spititout

print("\n\nGoing over some multicore stuff.\nThis shit won't work on Windows (or at all).")
Base.lineinfo = True
BigSize = Size*2
BigBPC = 8
Bytes = math.ceil(BigBPC/8)
TexC = Base.Texture(Size, Size, ("1.00", "-1.00"), ("1.00", "-1.00"))#Note the dimensions are reversed
Outsidestrokes = (B.Circle({"insidecolor":{"R":.5, "G":0.0, "B":1.00}, "outsidecolor":{"R":0.00, "G":0.00, "B":0.25}, "radius":.5, "x":.3, "y":.3}), )
TexC.input = B.Circle({"input":Outsidestrokes[0], "radius":.5, "x":0.0, "y":0.0, "insidecolor":{"R":1.00, "G":0.00, "B":0.00}})
print("Init finished")
t = bytearray.fromhex("00"*(BigSize**2))
d = {}
for s in ("R", "G", "B"):
    d[s] = multiprocessing.Array("B", copy.copy(t))

if str(input("Do multicore? Guarunteed to not work on Windows (if at all):"))[0].lower() == "y":
    proc = []
    print("Starting making processes!")
    for i in range(Cores):
        if __name__ == "__main__":
            print("Going through __main__!")
            proc.append(None)
            proc[i-1] = Process(target=TexC.render, kwargs={"colorspace":"RGB", "bpc":BigBPC, "sizeX":BigSize, "sizeY":BigSize, "dimensionX":("2.00", "-2.00"), "dimensionY":("2.00", "-2.00"), "thread":(i, Cores), "altch":copy.copy(d)})
    for i in range(Cores):
        proc[i].start()
        proc[i].join()
    print(proc)
    #for i in range(Cores):
        #TexB.render("RGB", bpc=BigBPC, sizeX=BigSize, sizeY=BigSize, dimensionX=("2.00", "-2.00"), dimensionY=("2.00", "-2.00"), thread=(i, 2), altch=copy.copy(d))#Still reversedTexB.clearBuffer()

    spititout = input("Rendering finished, print?")
    if spititout.lower() == "y" or spititout.lower() == "ye" or spititout.lower() == "yes" or spititout.lower() == "yep" or spititout.lower() == "t" or spititout.lower() == "true":
        for y in range(int(len(d["R"])/(BigSize))):
            line = []
            for x in range(BigSize):
                index = (x+(y*BigSize))*Bytes
                line.append(str(d["R"][index]).zfill(3)+"|"+str(d["G"][index]).zfill(3)+"|"+str(d["B"][index]).zfill(3))
            print(line)
    del d
