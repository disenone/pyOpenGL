# encoding: utf-8

import struct

class TGATypes:
    TGA_NODATA = 0
    TGA_INDEXED = 1
    TGA_RGB = 2
    TGA_GRAYSCALE = 3
    TGA_INDEXED_RLE = 9
    TGA_RGB_RLE = 10
    TGA_GRAYSCALE_RLE = 11
    
IMAGE_RGB = 0
IMAGE_RGBA = 1
IMAGE_LUMINANCE = 2
IMAGE_DATA_UNSIGNED_BYTE = 0
BOTTOM_LEFT = 0X00
BOTTOM_RIGHT = 0X10
TOP_LEFT = 0X20
TOP_RIGHT = 0X30

class rgba_t:
    r=0
    g=0
    b=0
    a=0

class rgb_t:
    r=0
    g=0
    b=0

class tgaheader_t:
    idLength = 0        # uchar
    colorMapType = 0    # uchar
    imageTypeCode = 0   # uchar
    colorMapSped = [0,0,0,0,0]  # uchar
    xOrigin = 0         # ushort
    yOrigin = 0         # ushort
    width = 0           # ushort
    height = 0          # ushort
    bpp = 0             # uchar
    imageDesc = 0       # uchar
    
class CTargaImage:
    m_colorDepth = 0
    m_imageDataType = 0
    m_imageDataFormat = 0
    m_pImageData = []
    m_width = 0
    m_height = 0
    m_imageSize = 0
    
    def __init__(self):
        pass
    
    def load(self, filename):
        fp = open(filename, 'rb')
        str = fp.read(14)
        tgaheader = tgaheader_t()

        tgaheader.idLength, tgaheader.colorMapType, tgaheader.imageTypeCode,
        tgaheader.colorMapSped[0], tgaheader.colorMapSped[1], tgaheader.colorMapSped[2],
        tgaheader.colorMapSped[3], tgaheader.colorMapSped[4], tgaheader.xOrigin,
        tgaheader.yOrigin, tgaheader.width, tgaheader.height, tgaheader.bpp,
        tgaheader.imageDesc = struct.unpack('4B4H2B', str)
    
a = '1'
b = '2'
str = struct.pack("cc", a, b)
print len(str)
print TGATypes.TGA_INDEXED