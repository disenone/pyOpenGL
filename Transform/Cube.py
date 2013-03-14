# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
    
xpos = 0.5
ypos = 0.0
zpos = -5.0
xangle = -10.0
yangle = 30.0
zangle = 45.0
leftPress = False
oldx = 0
oldy = 0

def MouseHandler(button, state):
    global leftPress
    if(state == glfw.GLFW_PRESS):
        if(button == glfw.MOUSE_BUTTON_LEFT):
            leftPress = True
    elif(state == glfw.GLFW_RELEASE):
        if(button == glfw.MOUSE_BUTTON_LEFT):
            leftPress = False

def MouseMoveHandler(x, y):
    global leftPress, oldx, oldy, xangle, yangle
    if(leftPress):
        xangle -= (x - oldx)
        yangle -= (y - oldy)
        oldx = x
        oldy = y

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


def DrawCube():
    glBegin(GL_QUADS)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, -1.0)
    glVertex3f(-1.0, 0.0, -1.0)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)    
    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(0.0, -1.0, -1.0)
    glVertex3f(0.0, 0.0, -1.0);
    glVertex3f(-1.0, 0.0, 0.0);
    glVertex3f(-1.0, 0.0, -1.0);
    glVertex3f(-1.0, -1.0, -1.0);
    glVertex3f(-1.0, -1.0, 0.0);
    glVertex3f(0.0, -1.0, 0.0);
    glVertex3f(0.0, -1.0, -1.0);
    glVertex3f(-1.0, -1.0, -1.0);
    glVertex3f(-1.0, -1.0, 0.0);
    glVertex3f(0.0, 0.0, -1.0);
    glVertex3f(-1.0, 0.0, -1.0);
    glVertex3f(-1.0, -1.0, -1.0);
    glVertex3f(0.0, -1.0, -1.0);
    glEnd();

def Display(xpos, ypos, zpos, xangle, yangle, zangle):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
    
    glPushMatrix()
    glTranslatef(xpos, ypos, zpos)
    glRotatef(xangle, 1.0, 0.0, 0.0)
    glRotatef(yangle, 0.0, 1.0, 0.0)
    glRotatef(zangle, 0.0, 0.0, 1.0)
    DrawCube()
    glPopMatrix()

def init():
    width = 640
    height = 480
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw cube")
    glfw.SetWindowSizeCallback(Reshape)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)          # 有什么用呢
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)
    glfw.SetMousePosCallback(MouseMoveHandler)


init()
while(True):
    Display(xpos, ypos, zpos, xangle, yangle, zangle)
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)

glfw.Terminate()

