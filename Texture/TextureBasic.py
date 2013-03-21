# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
from CTargaImage import CTargaImage
from OpenGL.GL.exceptional import glGenTextures, glEnd
from OpenGL.raw.GL.VERSION.GL_1_1 import glTexCoord2f
    
texture1 = CTargaImage()
texture2 = CTargaImage()
textureOne = 0
textureTwo = 0
zpos = -5.0
zmoveback = True 

def MouseHandler(button, state):
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        exit(0)


def KeyboardHandler(key, state):
    if(state == glfw.GLFW_PRESS):
        if(key == 'S'):
            pass

def WindowCLose():
    global textureOne, textureTwo 
    glDeleteTextures(textureOne)
    glDeleteTextures(textureTwo)
    exit(0)


def Reshape(width, height):
    if(height == 0):
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(54.0, float(width)/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def Render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
    
    global zpos, textureOne, textureTwo
    
    glPushMatrix()
    glTranslatef(-3.0, 0.0, zpos)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glBindTexture(GL_TEXTURE_2D, textureOne)
    DrawPlane()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(3.0, 0.0, zpos)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glBindTexture(GL_TEXTURE_2D, textureTwo)
    DrawPlane()
    glPopMatrix()

def DrawPlane():
    glBegin(GL_TRIANGLE_STRIP)
    glTexCoord2f(1.0, 0.0); glVertex3f(2.0, -2.0, -2.0)     # coord set to 2.0 would make the texture replicate
    glTexCoord2f(0.0, 0.0); glVertex3f(-2.0, -2.0, -2.0)
    glTexCoord2f(1.0, 2.0); glVertex3f(2.0, -2.0, 2.0)
    glTexCoord2f(0.0, 2.0); glVertex3f(-2.0, -2.0, 2.0)
    glEnd()
    

def init():
    width = 1024
    height = 768
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw line")
    glfw.SetWindowSizeCallback(Reshape)
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)
    glfw.SetWindowCloseCallback(WindowCLose)
    
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glEnable(GL_TEXTURE_2D)
    
    global texture1, texture2, textureOne, textureTwo
    if(not texture1.load("opengl_logo.tga")):
        exit(0)
    if(not texture2.load("checkerboard.tga")):
        exit(0)   
    
    print texture1.m_width, texture1.m_height
    
    # texture one
    textureOne = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureOne)
    # filter for min and mag texture
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    # specify the texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture1.m_width, texture1.m_height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, texture1.m_imageData)
    
    # texure two
    textureTwo = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureTwo)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture2.m_width, texture2.m_height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, texture2.m_imageData)
    
def Prepare(dt):
    global zpos, zmoveback
    if(zmoveback):
        zpos -= 5.0 * dt
    else:
        zpos += 5.0 * dt
    
    if(zpos > -5.0):
        zpos = -5.0
        zmoveback = True
    if(zpos < -20.0):
        zpos = -20.0
        zmoveback = False
    

init()
while(True):
    Render()
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)
    Prepare(0.1)

glfw.Terminate()

