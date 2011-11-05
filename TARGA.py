#Makes a .tga file out of a raster dict
END = "big"

def makeTARGA(sizeX, sizeY, raster, ID=None, originX=0, originY=0, imagetype=None, bpp=8, developer=None, extension=None, out=False, defaultA="FF", defaultR="00", defaultG="00", defaultB="00"):
    if ID is not None:
        if len(ID) > 255: raise ValueError("ID can't be more than 255 characters long, yo")
    if imagetype is not None:
        if imagetype > 255 or (imagetype > 10 and imagetype < 128): raise ValueError("colormaptype has to be either 0, 1 or between 128 and 255")
    if len(raster) > 4: raise ValueError("Too many channels")
    if sizeX > 65535 or sizeY > 65535: raise ValueError("Image too big")
    if originX > 65535 or originY > 65535: raise ValueError("Offset too large")
    #ID length
    header = bytearray(int(0).to_bytes(1, END) if ID is None else len(ID).to_bytes(1, END))
    #Color map type
    header += int(0).to_bytes(1, END)
    #Image type
    if imagetype is None:
        if len(raster) == 0:
            header += int(0).to_bytes(1, END)
        elif len(raster) == 1:
            header += int(3).to_bytes(1, END)
        elif len(raster) >= 2 and len(raster) <= 4:
            header += int(2).to_bytes(1, END)
    else:
        header += imagetype.to_bytes(1, END)
    #Color map specification
    header += int(0).to_bytes(5, END)
    #Image specification
    header += int(originX).to_bytes(2, END)#X-Origin
    header += int(originY).to_bytes(2, END)#Y-Origin
    header += int(sizeX).to_bytes(2, "little")#Width
    header += int(sizeY).to_bytes(2, "little")#Height
    header += int(bpp*4).to_bytes(1, END)#Pixel depth
    header += bpp.to_bytes(1, END)#Alpha depth
    #Image Data
    if ID is not None: header.append(ID)#ID
    keylist = list(raster.keys())
    color = []
    for s in "BGRA":
        color.append(raster[s] if s in raster else None)
        try:
            keylist.remove(s)
        except ValueError:
            pass
    if len(keylist) < 4:
        s = ""
        for c in keylist:
            s.append(c+"\n\t")
        print("The following channels were not mapped: \n"+s)
    image = bytearray.fromhex((defaultB+defaultG+defaultR+defaultA)*sizeX*sizeY)
    for i in range(4):#Only go through channels that are present
        if color[i] is not None:
            for pos in range(sizeX*sizeY):
                image[i+(4*pos)] = int(color[i][pos])
    print(image)
    #Developer area (not implemented yet)
    developerarea = bytearray()
    #Extension area
    extensionarea = bytearray()
    #Footer
    footer = bytearray(int(0).to_bytes(3, END) if extension is None else int(len(header)+len(image)+len(developerarea)).to_bytes(3, END))#Extension area offset
    footer += bytearray(int(0).to_bytes(3, END) if developer is None else int(len(header)+len(image)).to_bytes(3, END))#Extension area offset
    footer += bytearray("TRUEVISION-XFILE.", "ASCII")
    footer += bytearray(int(0).to_bytes(2, END))
    buffer = header+image+developerarea+extensionarea+footer
    if out: print(buffer)
    return buffer
