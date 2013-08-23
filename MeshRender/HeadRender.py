# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
from Mesh import Mesh
    
def MouseHandler(button, state):
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        exit(0)


def KeyboardHandler(key, state):
    if(state == glfw.GLFW_PRESS):
        if(key == 'S'):
            pass

def WindowCLose():
    exit(0)


def Reshape(width, height):
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
    gluPerspective(52.0, float(width)/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def Render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
    
    gluLookAt(0.0, 12.0, 0.0, 
              0.0, 0.0, 0.0, 
              0.0, 0.0, -1.0)


def init():
    width = 640
    height = 640
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw line")
    glfw.SetWindowSizeCallback(Reshape)
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)
    glfw.SetWindowCloseCallback(WindowCLose)
    
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL);
    
    
def LoadObj():
    mesh = Mesh()
    mesh.LoadFromObj('head.obj')

    print len(mesh.vertexs)
    for vertex in mesh.vertexs:
        print str(vertex.pos[0]) + ' ' + str(vertex.pos[1]) + ' ' + str(vertex.pos[2])
    print len(mesh.faces)
    for face in mesh.faces:
        print str(face[0])
    
    print len(mesh.textureCoords)
        
        
init()
LoadObj()

while(True):
    Render()
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)

glfw.Terminate()

