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
        height = 1 
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(52.0, width/height, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
def Display(m_angle =0.0):
    linewidth = 0.5
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
    gluLookAt(0.0, 10.0, 0.1, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    
    # move back 5 units and rotate about all 3 axes
    glTranslatef(0.0, 0.0, -5.0)
    glRotatef(m_angle, 1.0, 0.0, 0.0)
    glRotatef(m_angle, 0.0, 1.0, 0.0)
    glRotatef(m_angle, 0.0, 0.0, 1.0)
    # lime greenish color
    glColor3f(0.7, 1.0, 0.3)

    # draw the triangle such that the rotation point is in the center
    glBegin(GL_TRIANGLES)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glEnd()
    

def init():
    width = 640
    height = 480
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("test glfw")
    glfw.SetWindowSizeCallback(Reshape)
    glEnable(GL_DEPTH_TEST)
    # set eht projection
    
    # mouse
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)
    #


init()
m_angle = 0.0
while(True):
    Display(m_angle)
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)
    m_angle += 0.1

glfw.Terminate()
