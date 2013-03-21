# encoding: utf-8

import struct
import copy

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
BOTTOM_LEFT = 0x00
BOTTOM_RIGHT = 0x10
TOP_LEFT = 0x20
TOP_RIGHT = 0x30

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
    
    def printInfo(self):
        print "tga header:"
        print "idLength: ", self.idLength
        print "colorMapType: ", self.colorMapType
        print "imageTypeCode: ", self.imageTypeCode
        print "colorMapSped: [",
        for i in range(5):
            print self.colorMapSped[i],
        print "]"
        print "xOrigin: ", self.xOrigin
        print "yOrigin: ", self.yOrigin
        print "width: ", self.width
        print "height: ", self.height
        print "bpp: ", self.bpp
        print "imageDesc: ", self.imageDesc
    
class CTargaImage:
    m_colorDepth = 0
    m_imageDataType = 0
    m_imageDataFormat = 0
    m_imageData = []
    m_width = 0
    m_height = 0
    m_imageSize = 0
    
    def __init__(self):
        pass
    
    def load(self, filename):
        fp = open(filename, 'rb')
        
        # read header
        str = fp.read(18)
        tgaheader = tgaheader_t()
        tgaheader.idLength, tgaheader.colorMapType, tgaheader.imageTypeCode,\
        tgaheader.colorMapSped[0], tgaheader.colorMapSped[1], tgaheader.colorMapSped[2],\
        tgaheader.colorMapSped[3], tgaheader.colorMapSped[4], tgaheader.xOrigin,\
        tgaheader.yOrigin, tgaheader.width, tgaheader.height, tgaheader.bpp,\
        tgaheader.imageDesc = struct.unpack('8B4H2B', str)
        
#        tgaheader.printInfo()
        
        if( tgaheader.imageTypeCode != TGATypes.TGA_RGB and 
            tgaheader.imageTypeCode != TGATypes.TGA_GRAYSCALE and
            tgaheader.imageTypeCode != TGATypes.TGA_RGB_RLE and
            tgaheader.imageTypeCode != TGATypes.TGA_GRAYSCALE_RLE and
            tgaheader.colorMapType != 0):
            fp.close()
            print "failed to read file: ", filename
            return False
        
        # read image data
        self.m_width = tgaheader.width
        self.m_height = tgaheader.height
        color_mode = tgaheader.bpp / 8
        if(color_mode < 3):
            fp.close()
            return False
        self.m_imageSize = self.m_width * self.m_height * color_mode
        # skip pass the id if there is one
        fp.read(tgaheader.idLength)
        
        if( tgaheader.imageTypeCode == TGATypes.TGA_RGB or
            tgaheader.imageTypeCode == TGATypes.TGA_GRAYSCALE):
            unpackstr = '%dB' %(self.m_imageSize)
            self.m_imageData = list(struct.unpack(unpackstr, fp.read(self.m_imageSize)))
        else:   # if this is a RLE compressed image
            color = rgba_t()
            while(len(self.m_imageData) < self.m_imageSize):
                id = ord(fp.read(1))
                if(id > 128):   # run lenght data
                    length = id - 127
                    color.b = ord(fp.read(1))
                    color.g = ord(fp.read(1))
                    color.r = ord(fp.read(1))
                    if(color_mode == 4):
                        color.a = ord(fp.read(1))
                    while(length > 0):
                        self.m_imageData.append(color.b)
                        self.m_imageData.append(color.g)
                        self.m_imageData.append(color.r)
                        if(color_mode == 4):
                            self.m_imageData.append(color.a)
                        length -= 1
                        
                else:
                    length = id+1   # the num of non RLE pixels
                    while(length > 0):
                        color.b = ord(fp.read(1))
                        color.g = ord(fp.read(1))
                        color.r = ord(fp.read(1))
                        if(color_mode == 4):
                            color.a = ord(fp.read(1))
                        self.m_imageData.append(color.b)
                        self.m_imageData.append(color.g)
                        self.m_imageData.append(color.r)
                        if(color_mode == 4):
                            self.m_imageData.append(color.a)
                        length -= 1
                    
        fp.close()
        
        global IMAGE_RGB, IMAGE_RGBA, IMAGE_DATA_UNSIGNED_BYTE, IMAGE_LUMINANCE, TOP_LEFT
        if(tgaheader.imageTypeCode == TGATypes.TGA_RGB or
           tgaheader.imageTypeCode == TGATypes.TGA_RGB_RLE):
            if(3 == color_mode):
                self.m_imageDataFormat = IMAGE_RGB
                self.m_imageDataType = IMAGE_DATA_UNSIGNED_BYTE
                self.m_colorDepth = 24
            else:
                self.m_imageDataFormat = IMAGE_RGBA
                self.m_imageDataType = IMAGE_DATA_UNSIGNED_BYTE
                self.m_colorDepth = 32
        elif(tgaheader.imageTypeCode == TGATypes.TGA_GRAYSCALE or
             tgaheader.imageTypeCode == TGATypes.TGA_GRAYSCALE_RLE):
            self.m_imageDataFormat = IMAGE_LUMINANCE
            self.m_imageDataType = IMAGE_DATA_UNSIGNED_BYTE
            self.m_colorDepth = 8
        
        if( (tgaheader.imageDesc & TOP_LEFT) == TOP_LEFT):
            self.FlipVertical()
        
        self.SwapRedBlue()
        return True

    def SwapRedBlue(self):
        swap_method = {32: self.SwapRedBlue32, 24: self.SwapRedBlue24, 8: self.SwapRedBlue8,}
        try:
            swap_method[self.m_colorDepth]()
        except KeyError:
            pass
    
    def SwapRedBlue32(self):
        for i in range(0, len(self.m_imageData), 4):
            tmp = self.m_imageData[i]
            self.m_imageData[i] = self.m_imageData[i+2]
            self.m_imageData[i+2] = tmp
            
    def SwapRedBlue24(self):
        for i in range(0, len(self.m_imageData), 3):
            tmp = self.m_imageData[i]
            self.m_imageData[i] = self.m_imageData[i+2]
            self.m_imageData[i+2] = tmp
            
    def SwapRedBlue8(self):
        pass
    
    def FlipVertical(self):
        if(len(self.m_imageData) == 0):
            return False
        if(self.m_colorDepth != 32 and self.m_colorDepth != 24):
            return True
        
        line_width = 0;
        if(self.m_colorDepth == 32):
            line_width = self.m_width * 4
        elif(self.m_colorDepth == 24):
            line_width = self.m_width * 3
        top = 0
        bottom = line_width*(self.m_height - 1)
        
        # swap all the pixels
        for i in range(self.m_height / 2):
            tmp = self.m_imageData[top: top+line_width] 
            self.m_imageData[top: top+line_width] = self.m_imageData[bottom: bottom+line_width]
            self.m_imageData[bottom: bottom+line_width] = tmp
            top += line_width
            bottom -= line_width

        
if __name__ == '__main__':
    ct = CTargaImage()
    ct.load("opengl_logo_un.tga")