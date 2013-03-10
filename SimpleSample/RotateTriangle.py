# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
    
def MouseHandler(button, state):
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        exit(0)


def KeyboardHandler(key, state):
    if(key == 'q'):
        exit(0)


def Reshape(width, height):
    if(height == 0):
        return
#    glViewport(0, 0, width, height)
#    glMatrixMode(GL_PROJECTION)
#    glLoadIdentity()   
#    ratio = 1.0*height / width
#    glFrustum(-1, 1, -1*ratio, 1*ratio, 1, 50)      # set the project style
#    glMatrixMode(GL_MODELVIEW)
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(52.0, width/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    
def Display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
    
    gluLookAt(0.0, 10.0, 0.0, 
              0.0, 0.0, 0.0, 
              0.0, 0.0, -1.0)
    
    linewidth = 0.5
    line = 0.0
    while line <= 7.0:
        glLineWidth(linewidth)
        glBegin(GL_LINES)
        glVertex3f(-1.0, 0.0, line-3.0)
        glVertex3f(-5.0, 0.0, line-3.0)
        glEnd()
        linewidth += 0.1
        line += 0.5

def init():
    width = 640
    height = 480
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw line")
    glfw.SetWindowSizeCallback(Reshape)
    glEnable(GL_DEPTH_TEST)
    # set eht projection
    
    # mouse
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)
    #


init()
while(True):
    Display()
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)

glfw.Terminate()
