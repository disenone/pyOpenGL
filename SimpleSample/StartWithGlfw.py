# encoding: utf-8

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from glfw import glfw
import time

def init():
    width = 640
    height = 480
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("test glfw")
    
    # set eht projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    ratio = 1.0*height / width
    print ratio
    glFrustum(-1, 1, -1*ratio, 1*ratio, 1, 50)      # set the project style
    glMatrixMode(GL_MODELVIEW)
    
    
def drawFunc():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 1.0, 0.0, 0.0, -1.0, 0.0, 1, 0.0)
#    glTranslatef(0.5, 0.0, 0)
    
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0);
    glVertex3f(0.2, 0.0, 0);
    glColor3f(0.0, 1.0, 0.0);
    glVertex3f(0, 0.2, 0);
    glColor3f(0.0, 0.0, 1.0);
    glVertex3f(-0.2, 0.0, 0.0);
    glEnd()
#    glRotatef(5, 1, 1, 0)
    glFlush()



init()
while(True):
    drawFunc()
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.05)

glfw.Terminate()
