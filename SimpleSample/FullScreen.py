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
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()   
    ratio = 1.0*height / width
    glFrustum(-1, 1, -1*ratio, 1*ratio, 1, 50)      # set the project style
    glMatrixMode(GL_MODELVIEW)
    
#    glViewport(0, 0, width, height)
#    glMatrixMode(GL_PROJECTION)
#    glLoadIdentity()
#    gluPerspective(90.0, width/height, 1.0, 100.0)
#    glMatrixMode(GL_MODELVIEW)
    
def Display():
    glLoadIdentity()
    gluLookAt(0.0, 1.0, 6.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glBegin(GL_TRIANGLES);
    glColor3f(1.0, 0.0, 0.0);
    glVertex3f(2.0, 2.5, -1.0);
    glColor3f(0.0, 1.0, 0.0);
    glVertex3f(-3.5, -2.5, -1.0);
    glColor3f(0.0, 0.0, 1.0);
    glVertex3f(2.0, -4.0, 0.0);
    glEnd();

    glBegin(GL_POLYGON);
    glColor3f(1.0, 1.0, 1.0);
    glVertex3f(-1.0, 2.0, 0.0);
    glColor3f(1.0, 1.0, 0.0);
    glVertex3f(-3.0, -0.5, 0.0);
    glColor3f(0.0, 1.0, 1.0);
    glVertex3f(-1.5, -3.0, 0.0);
    glColor3f(0.0, 0.0, 0.0);
    glVertex3f(1.0, -2.0, 0.0);
    glColor3f(1.0, 0.0, 1.0);
    glVertex3f(1.0, 1.0, 0.0);
    glEnd();
    

def init():
    width = 640
    height = 480
    glfw.Init()
    glfw.OpenWindow(1440, 900, 8, 8, 8, 0, 24, 0, glfw.FULLSCREEN)
    glfw.SetWindowTitle("full glfw")
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
    time.sleep(0.05)

glfw.Terminate()
