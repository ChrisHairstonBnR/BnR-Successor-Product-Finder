

def invertHexColor(hexColor):
    r = int(hexColor[1:3], 16)
    g = int(hexColor[3:5], 16)
    b = int(hexColor[5:7], 16)
    #use lstrip(0x)
    rInv = 255-r
    gInv = 255-g
    bInv = 255-b

    return '#%s%s%s' % (hex(rInv).lstrip('0x'),  hex(gInv).lstrip('0x'), hex(bInv).lstrip('0x'))
