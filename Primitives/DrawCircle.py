# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
import numpy

radius=2
side_num=8
edge_only=False

def MouseHandler(button, state):
    global edge_only
    if(button == glfw.MOUSE_BUTTON_LEFT and state == glfw.GLFW_PRESS):
        edge_only = True;
        print "left once"
    elif(button == glfw.MOUSE_BUTTON_RIGHT and state == glfw.GLFW_PRESS):
        edge_only = False;
        print "right once"
    

def KeyboardHandler(key, state):
    global side_num
    global radius
    if(state == glfw.GLFW_PRESS):
        if(key == glfw.KEY_UP):
            radius += 0.2
        elif(key == glfw.KEY_DOWN):
            radius -= 0.2
        elif(key == glfw.KEY_LEFT):
            side_num -= 1
        elif(key == glfw.KEY_RIGHT):
            side_num += 1
            

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
    
    
def DrawCircle(radius, side_num, edge_only):
    if(edge_only):
        glBegin(GL_LINE_LOOP)
    else:
        glBegin(GL_POLYGON)
    
    for vertex in range(0, side_num):
        print vertex
        angle  = float(vertex) * 2.0 * numpy.pi / side_num
        glVertex3f(numpy.cos(angle)*radius, 0.0, numpy.sin(angle)*radius)
    
    glEnd();

def Display(radius, side_num, edge_only):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
    
    gluLookAt(0.0, 12.0, 0.0, 
              0.0, 0.0, 0.0, 
              0.0, 0.0, -1.0)
    
    DrawCircle(radius, side_num, edge_only)

def init():
    width = 640
    height = 480
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw circle")
    glfw.SetWindowSizeCallback(Reshape)
    glEnable(GL_DEPTH_TEST)
    # set eht projection
    
    # mouse
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)
    #


init()

while(True):
    Display(radius, side_num, edge_only)
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)

glfw.Terminate()

