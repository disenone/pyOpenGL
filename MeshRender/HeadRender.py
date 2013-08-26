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
    gluOrtho2D(0.0, 10.0, 0.0, 10.0);
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def Render(mesh = Mesh()):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
        
    gluLookAt(mesh.center[0], mesh.center[1], mesh.center[2] + mesh.radius, 
              mesh.center[0], mesh.center[1], mesh.center[2], 
              mesh.center[0], mesh.center[1] + mesh.radius, mesh.center[2])
    
    glColor3f(1.0, 0.0, 0.5)
    
    glBegin(GL_TRIANGLES)
    for i in range(len(mesh.faces)):
        for j in range(3):
            glVertex3f(mesh.vertexs[mesh.faces[i][j]].pos[0], mesh.vertexs[mesh.faces[i][j]].pos[1], mesh.vertexs[mesh.faces[i][j]].pos[2])   
    glEnd()

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
    
    
def LoadObj(fileName):
    mesh = Mesh()
    mesh.LoadFromObj(fileName)
    return mesh
#    print len(mesh.vertexs)
#    for vertex in mesh.vertexs:
#        print str(vertex.pos[0]) + ' ' + str(vertex.pos[1]) + ' ' + str(vertex.pos[2])
#    print len(mesh.faces)
#    for face in mesh.faces:
#        print str(face[0])
#    print len(mesh.textureCoords)
        
        
init()
mesh = LoadObj('head.obj')
print mesh.center
print mesh.radius
while(True):
    Render(mesh)
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)

glfw.Terminate()

