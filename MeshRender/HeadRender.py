# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
from Image import *
import glfw
import time
import numpy
from Mesh import Mesh
from Converter import *
import os

orthoSize = 200.0
currentHandle = None

def MouseHandler(button, state):
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        exit(0)

def KeyboardHandler(key, state):
    if(state == glfw.GLFW_PRESS):
        if(key == 'S'):
            pass

def WindowCLose():
    global currentHandle
    glDeleteTextures(currentHandle)
    exit(0)


def Reshape(width, height):
    global orthoSize
    if(height == 0):
        height = 1
#    glViewport(0, 0, width, height)
#    glMatrixMode(GL_PROJECTION)
#    glLoadIdentity()   
#    ratio = 1.0*height / width
#    glFrustum(-1, 1, -1*ratio, 1*ratio, 1, 50)      # set the project style
#    glMatrixMode(GL_MODELVIEW)
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    print 'orthoSize:', orthoSize
    glOrtho(-orthoSize, orthoSize, -orthoSize, orthoSize, -orthoSize, orthoSize);
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def Render(mesh = Mesh(),textureImg = None, textureHandle = None, angle = 0.0):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
    
    glPushMatrix()
#    gluLookAt(0.0, 0.0, mesh.radius, 
#          0.0, 0.0, 0.0, 
#          0.0, mesh.radius, 0.0)
#    gluLookAt(0.0, 0.0, 100, 
#          0.0, 0.0, 0.0, 
#          0.0, 100, 0.0)
#    glPushMatrix()
    glRotatef(-180, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glTranslatef(-mesh.center[0], -mesh.center[1], -mesh.center[2])
    #
    
#    glPopMatrix()
#    textureImg.
#    glColor3f(1.0, 0.0, 0.5)
    glBindTexture(GL_TEXTURE_2D, textureHandle)
#    DrawPlane()
    #DrawTriangle()
    DrawMesh(mesh)
    glPopMatrix()

def init(textureImg):
    width = 640
    height = 640
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw mesh")
    glfw.SetWindowSizeCallback(Reshape)
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)
    glfw.SetWindowCloseCallback(WindowCLose)
    
    glClearColor(1.0, 1.0, 1.0, 1.0);
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL);
    
    glEnable(GL_TEXTURE_2D)
        
    # texture one
    textureHandle = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureHandle)
    # filter for min and mag texture
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    # specify the texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textureImg.size[0], textureImg.size[1],
                 0, GL_RGB, GL_UNSIGNED_BYTE, PIL2array(textureImg))
    return textureHandle
    
def DrawPlane():
    glBegin(GL_TRIANGLE_STRIP)
    glTexCoord2f(1.0, 1.0); 
    glVertex3f(50.0, -50.0, 0)     # coord set to 2.0 would make the texture replicate
    glTexCoord2f(1.0, 0.0); 
    glVertex3f(50.0, 50.0, 0)
    glTexCoord2f(0.0, 1.0); 
    glVertex3f(-50.0, -50.0, 0)
    glTexCoord2f(0.0, 0.0); 
    glVertex3f(-50.0, 50.0, 0)
    glEnd()
    
def DrawMesh(mesh):
    glBegin(GL_TRIANGLES)
    for i in range(len(mesh.faces)):
        for j in range(3):
            glTexCoord2f(
                         mesh.textureCoords[mesh.vertexs[mesh.faces[i][j]].textureId][0],
                         mesh.textureCoords[mesh.vertexs[mesh.faces[i][j]].textureId][1])
            glVertex3f(
                       mesh.vertexs[mesh.faces[i][j]].pos[0], 
                       mesh.vertexs[mesh.faces[i][j]].pos[1], 
                       mesh.vertexs[mesh.faces[i][j]].pos[2])
#            print mesh.vertexs[mesh.faces[i][j]]   
    glEnd()
    
def DrawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex3f(50, -50, 0)
    glVertex3f(-50, -50, 0)
    glVertex3f(0, 50, 0)
    glEnd()

def CaptureOpenGLImage():
    viewPort = glGetIntegerv(GL_VIEWPORT)
    arrayImg = glReadPixels(viewPort[0], viewPort[1], viewPort[2], viewPort[3], GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombuffer('RGB', (viewPort[2], viewPort[3]), arrayImg, 'raw', 'RGB', 0, 1)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return image

def LoadObj(fileName):
    mesh = Mesh()
    mesh.LoadFromObj(fileName)
    return mesh
    print len(mesh.vertexs)
    for vertex in mesh.vertexs:
        print str(vertex.pos[0]) + ' ' + str(vertex.pos[1]) + ' ' + str(vertex.pos[2])
    print len(mesh.faces)
    for face in mesh.faces:
        print str(face[0])
    print len(mesh.textureCoords)

def PrintList(list):
    for i in list:
        print i

def RenderHead(folderPath, headMeshName, textureName, capturePath = None):
    global orthoSize, currentHandle
    print folderPath
    if capturePath != None:
       capturePath = os.path.join(capturePath, os.path.basename(folderPath))
    mesh = LoadObj(os.path.join(folderPath, headMeshName))
    orthoSize = mesh.radius * 1.5
    print 'mesh center = ', mesh.center
    print 'mesh radius = ', mesh.radius
    print 'len texturecoord = ', len(mesh.textureCoords)
    print 'len faces = ', len(mesh.faces)
    print 'len vertex = ', len(mesh.vertexs)
#    PrintList(mesh.vertexs)
    textureImg = Image.Image()
    textureImg = Image.open(os.path.join(folderPath, textureName))
    textureHandle = None
    arr = PIL2array(textureImg)
#    tempImage = array2PIL(arr, textureImg.size)
#    textureImg.save(os.path.join(folderPath, 'temp_texture.jpg'))
#    print arr.size
#    print textureImg.format
    print 'texture size = ', textureImg.size
#    print textureImg.size[0], textureImg.size[1]
#    print textureImg.info
    print list(textureImg.getdata())[0]
    print textureImg.mode
    angle = 0
    textureHandle = init(textureImg)
    currentHandle = textureHandle
    Render(mesh, textureImg, angle)
    glfw.SwapBuffers()
    print 'handle = ', textureHandle
    endFlag = 361
    angleChange = {0:30, 30:-30, -30:endFlag}
    while(True):
        Render(mesh, textureImg, textureHandle, angle)
        if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
            break
#        angle += 1;
        if(angleChange.get(angle) != None):
            captureImage = CaptureOpenGLImage()
            captureImage.save(folderPath + '/capture_' + str(angle) +'.jpg')
            if capturePath != None:
                captureImage.save(capturePath + '_capture_' + str(angle) +'.jpg')
            angle = angleChange[angle]
        else:
            print 'end'
            glfw.Terminate()
            glfw.CloseWindow()
            break
        glfw.SwapBuffers()
        time.sleep(0.02)
                
    
if __name__ == '__main__':
    path = 'I:/TextureCompletionTest'
    capturePath = os.path.join(path, 'capture')
    if os.path.exists(capturePath) == False:
        os.mkdir(capturePath)
    #path = 'F:/program/opengl'
    headMeshName = 'head_in_phone.obj'
    textureName = 'Debug_HeadTexture_phone.png'
    pathInfo = os.listdir(path)
    print pathInfo
    for name in pathInfo:
        dir = os.path.join(path, name)
        if os.path.isdir(dir):
            if os.path.exists(os.path.join(dir, headMeshName)) == False:
                continue
            RenderHead(dir, headMeshName, textureName, capturePath)

 #   RenderHead('.', 'head.obj', 'fit.jpg')
    

