# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time

xAxisAngle = 0
yAxisAngle = 0

def MouseHandler(button, state):
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        exit(0)


def KeyboardHandler(key, state):
    if(key == 'q'):
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
    
    
def DrawAxes(r, g, b):
    glBegin(GL_LINES)
    glColor3f(r, g, b)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 3.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(3.0, 0.0, 0.0)
    glEnd()
    
def DrawPlane():
    glBegin(GL_TRIANGLE_STRIP);
    glColor3f(1.0, 0.0, 0.0);
    glVertex3f(-2.0, 0.0, -2.0);
    glColor3f(0.0, 1.0, 0.0);
    glVertex3f(2.0, 0.0, -2.0);
    glColor3f(0.0, 0.0, 1.0);
    glVertex3f(-2.0, 0.0, 2.0);
    glColor3f(1.0, 1.0, 0.0);
    glVertex3f(2.0, 0.0, 2.0);
    glEnd();
    DrawAxes(1.0, 1.0, 0.0)
    
def Display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -10.0);
    DrawAxes(1.0, 0.0, 0.0);
    glRotatef(xAxisAngle, 1.0, 0.0, 0.0);
    glRotatef(yAxisAngle, 0.0, 1.0, 0.0);
    DrawPlane();


def init():
    width = 640
    height = 480
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw line")
    glfw.SetWindowSizeCallback(Reshape)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_BACK, GL_LINE);
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
    xAxisAngle += 1
    yAxisAngle += 1

glfw.Terminate()

