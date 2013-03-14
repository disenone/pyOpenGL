# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
from OpenGL.raw.GL.EXT.secondary_color import *
    
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
    gluOrtho2D(0.0, 10.0, 0.0, 10.0);
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def Display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    
    glShadeModel(GL_FLAT);
    glBegin(GL_TRIANGLE_FAN);
    glColor3d(1.0, 0.0, 0.0);
    glVertex2i(1, 6);
    glColor3d(0.0, 1.0, 0.0);
    glVertex2i(4, 6);
    glColor3d(0.0, 0.0, 1.0);
    glVertex2i(4, 9);
    glColor3d(1.0, 1.0, 1.0);
    glVertex2i(1, 9);
    glEnd();
    
    glShadeModel(GL_SMOOTH);
    glBegin(GL_TRIANGLE_FAN);
    glColor3d(1.0, 0.0, 0.0);
    glVertex2i(1, 1);
    glColor3d(0.0, 1.0, 0.0);
    glVertex2i(4, 1);
    glColor3d(0.0, 0.0, 1.0);
    glVertex2i(4, 4);
    glColor3d(1.0, 1.0, 1.0);
    glVertex2i(1, 4);
    glEnd();
    
    glEnable(GL_COLOR_SUM);
    glShadeModel(GL_FLAT);
    glBegin(GL_TRIANGLE_FAN);
    glColor3d(1.0, 0.0, 0.0);
    glSecondaryColor3f(0.0, 1.0, 0.0);
    glVertex2i(6, 6);
    glColor3d(0.0, 1.0, 0.0);
    glSecondaryColor3f(0.0, 0.0, 1.0);
    glVertex2i(9, 6);
    glColor3d(0.0, 0.0, 1.0);
    glSecondaryColor3f(1.0, 0.0, 0.0);
    glVertex2i(9, 9);
    glColor3d(1.0, 1.0, 1.0);
    glSecondaryColor3f(0.0, 0.0, 0.0);
    glVertex2i(6, 9);
    glEnd();
    
    glShadeModel(GL_SMOOTH);
    glBegin(GL_TRIANGLE_FAN);
    glColor3d(1.0, 0.0, 0.0);
    glSecondaryColor3f(0.0, 1.0, 0.0);
    glVertex2i(6, 1);
    glColor3d(0.0, 1.0, 0.0);
    glSecondaryColor3f(0.0, 0.0, 1.0);
    glVertex2i(9, 1);
    glColor3d(0.0, 0.0, 1.0);
    glSecondaryColor3f(1.0, 0.0, 0.0);
    glVertex2i(9, 4);
    glColor3d(1.0, 1.0, 1.0);
    glSecondaryColor3f(0.0, 0.0, 0.0);
    glVertex2i(6, 4);
    glEnd();
    glDisable(GL_COLOR_SUM);


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
if( bool(glSecondaryColor3f) ):
    print "ok"
while(True):
    Display()
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)

glfw.Terminate()

