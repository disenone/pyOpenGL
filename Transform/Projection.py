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
projectType = True  # true mean perspective, false means ortho

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
    if(key == glfw.KEY_ENTER and state == glfw.GLFW_PRESS):
        ChangeProjection()


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
    #gluPerspective(52.0, width/height, 1.0, 1000.0)
    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def ChangeProjection():
    global projectType
    projectType = ~projectType
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if(projectType == True):
        glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
        print "Frustum"
    else:
        glOrtho(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
        print "ortho"
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    print projectType

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
#    glTranslatef(xpos, ypos, zpos)
#    glRotatef(xangle, 1.0, 0.0, 0.0)
#    glRotatef(yangle, 0.0, 1.0, 0.0)
#    glRotatef(zangle, 0.0, 0.0, 1.0)
    glTranslatef(0.4, 0.0, -1.5);
    glRotatef(15.0, 1.0, 0.0, 0.0);
    glRotatef(30.0, 0.0, 1.0, 0.0);
    glScalef(0.75, 0.75, 0.75);
    DrawCube()
    glPopMatrix()

def init():
    width = 640
    height = 480
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw cube change projection")
    glfw.SetWindowSizeCallback(Reshape)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)          # ��ʲô����
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

