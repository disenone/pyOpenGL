# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import Image
import glfw
import time
import numpy
from Mesh import Mesh

def MouseHandler(button, state):
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        exit(0)


def KeyboardHandler(key, state):
    if(state == glfw.GLFW_PRESS):
        if(key == 'S'):
            pass

def WindowCLose():
    global textureHandle
    glDeleteTextures(textureHandle)
    exit(0)


def Reshape(width, height):
    global mesh
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
    if(mesh.radius > 0):
        glOrtho(
            -mesh.radius*2, mesh.radius*2, 
            -mesh.radius*2, mesh.radius*2,
            -mesh.radius*2, mesh.radius*2);
    else:
        glOrtho(-200.0, 200.0, -200.0, 200.0,-200.0, 200.0);
        print 100
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def Render(mesh = Mesh(),textureImg = None,angel = 0.0):
    global textureHandle
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
    
    glTranslatef(mesh.center[0], mesh.center[1], mesh.center[2])
    glRotatef(angle, 0.0, 1.0, 0.0)
#    glPopMatrix()
#    textureImg.
#    glColor3f(1.0, 0.0, 0.5)
    glBindTexture(GL_TEXTURE_2D, textureHandle)
#    DrawPlane()
    #DrawTriangle()
    DrawMesh(mesh, textureImg)
    glPopMatrix()

def init():
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
    
    global textureImg, textureHandle
    
    # texture one
    textureHandle = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureHandle)
    # filter for min and mag texture
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    # specify the texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textureImg.size[0], textureImg.size[1],
                 0, GL_RGB, GL_UNSIGNED_BYTE, PIL2array(textureImg))
    
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
    
def DrawMesh(mesh, textureImg):
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
        
def PIL2array(img):
    return numpy.array(img.getdata(),
                    numpy.uint8).reshape(img.size[1], img.size[0], 3)

def array2PIL(arr, size):
    mode = 'RGB'
    #arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = numpy.c_[arr, 255*numpy.ones((len(arr),1), numpy.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)

        
mesh = LoadObj('head.obj')
print mesh.center
print mesh.radius
print len(mesh.textureCoords)
print len(mesh.faces)
textureImg = Image.Image()
textureImg = Image.open('fit.jpg')
textureHandle = None
arr = PIL2array(textureImg)
print arr.size
img2 = array2PIL(arr, textureImg.size)
img2.save('fit2.jpg')
print textureImg.format
print textureImg.size
print textureImg.size[0], textureImg.size[1]
print textureImg.info
print textureImg.getdata()
print textureImg.mode
angle = 0.0
init()
while(True):
    Render(mesh, textureImg, angle)
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)
    angle += 1

glfw.Terminate()

