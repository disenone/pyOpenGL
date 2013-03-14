# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time

m_windowWidth = 0;
m_windowHeight = 0;

def MouseHandler(button, state):
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        exit(0)


def KeyboardHandler(key, state):
    if(state == glfw.GLFW_PRESS):
        if(key == 'S'):
            pass
       

def DrawLine():
    glDisable(GL_DEPTH_TEST);
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    gluOrtho2D(0.0, 2.0, 0.0, 2.0);
    global m_windowHeight, m_windowWidth
    glViewport(0, 0, m_windowWidth, m_windowHeight);
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();
    glColor3f(1.0, 1.0, 0.5);
    glBegin(GL_LINES);
    glVertex2i(2, 1);
    glVertex2i(0, 1);
    glVertex2i(1, 2);
    glVertex2i(1, 0);
    glEnd();
    glPopMatrix();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glMatrixMode(GL_MODELVIEW);
    glEnable(GL_DEPTH_TEST);       

def Reshape(width, height):
    if(height == 0):
        height = 1
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(52.0, float(width)/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    global m_windowHeight, m_windowWidth
    m_windowWidth = width
    m_windowHeight = height

def Display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
    
    gluLookAt(0.0, 12.0, 0.0, 
              0.0, 0.0, 0.0, 
              0.0, 0.0, -1.0)
    
    DrawLine()

def init():
    width = 640
    height = 640
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw line")
    glfw.SetWindowSizeCallback(Reshape)
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL);
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

