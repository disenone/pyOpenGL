'''
Created on 2013-8-24

@author: lgl
'''

import string
import sys

class Vertex(object):
    pos = [0.0, 0.0, 0.0];
    textureId = 0
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.pos = [x, y, z]
        self.textureId = 0
    def __getitem__(self, i):
        return self.pos[i]
    def __setitem__(self, i, xyz):
        self.pos[i] = xyz
    def __str__(self):
        return str(self.pos[0]) + ' ' + str(self.pos[1]) + ' ' + str(self.pos[2])
    
    
class TriFace(object):
    index = [0, 0, 0]
    def __init__(self, v0=0, v1=0, v2=0):
        self.index = [v0, v1, v2]
    def __getitem__(self, i):
        return self.index[i]
    def __str__(self):
        return self.index.__str__()

class TextureCoord(object):
    uv = [0.0, 0.0]
    def __init__(self, u = 0.0, v=0.0):
        self.uv = [u, v]
    def __getitem(self, i):
        return self.uv[i]
    def __str__(self):
        return self.uv.__str__()
        
class Mesh(object):
    '''
    classdocs
    '''
    vertexs = []
    faces = []
    textureCoords = []
    center = Vertex()
    radius = 0.0
    
    def __init__(self):
        '''
        Constructor
        '''
        self.vertexs = []
        self.faces = []
        self.textureCoords = []
        self.vertexTextureId = {}
        self.center = Vertex()
        self.radius = 0.0
        
    def LoadFromObj(self, fileName):
        inputData = open(fileName, )
        minXYZ = Vertex(sys.float_info.max, sys.float_info.max, sys.float_info.max)
        maxXYZ = Vertex(-sys.float_info.max, -sys.float_info.max, -sys.float_info.max)
        for line in inputData:
            #print line
            words = line.split(' ')
            if words[0] == 'v':
                #print 'find v'
                pos = [0,0,0]
                for i in range(0, 3):
                    pos[i] = float(words[i+1])
                    minXYZ[i] = min(minXYZ[i], pos[i])
                    maxXYZ[i] = max(maxXYZ[i], pos[i])
                self.vertexs.append(Vertex(pos[0], pos[1], pos[2]))
                
            elif words[0] == 'vt':
                uv = [0,0,0]
                for i in range(2):
                    uv[i] = float(words[i+1])
                self.textureCoords.append(TextureCoord(uv[0], uv[1]))
            elif words[0] == 'f':
                face = [0,0,0,0]
                if(len(words) == 4):
                    for i in range(0, 3):
                        splitIds = words[i+1].split('/')
                        face[i] = int(splitIds[0])
                        self.vertexs[face[i]].textureId = int(splitIds[1])
                    self.faces.append(TriFace(face[0], face[1], face[2]))
                elif(len(words) == 5):
                    for i in range(0, 4):
                        splitIds = words[i+1].split('/')
                        face[i] = int(splitIds[0]) - 1
                        self.vertexs[face[i]].textureId = int(splitIds[1])
                    self.faces.append(TriFace(face[0], face[1], face[2]))
                    self.faces.append(TriFace(face[0], face[2], face[3]))
            else:
                pass
            
            for i in range(3):
                self.center[i] = (maxXYZ[i] + minXYZ[i]) / 2
            self.radius = maxXYZ[0] - minXYZ[0]
            for i in range(1, 3):
                self.radius = maxXYZ[i] - minXYZ[i]
            self.radius /= 2
                
                
                
        
        