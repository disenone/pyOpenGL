# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time

CUBE_DEG_PER_S = 30.0
LIGHT_DEG_PER_S = 90.0
CUBE_SIZE = 9.0
flashLightPos = [ 0.0, 0.0, 0.0];
flashLightDir = [ 0.0, 0.0, -1.0 ];
flashLightColor = [ 0.2, 0.2, 0.2 ];

redLightColor = [ 0.5, 0.1, 0.2 ];
redLightPos = [ 10.0, 0.0, 5.0, 1.0 ];

greenLightColor = [ 0.1, 0.6, 0.2 ];
greenLightPos = [ 0.0, 0.0, 10.0, 1.0 ];
m_pSphere = gluNewQuadric()
m_cubeAngle = 0.0
m_lightAngle = 0.0
m_flashlightOn = True        

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
    gluPerspective(64.0, float(width)/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def DrawPlane(size, step):
    glBegin(GL_QUADS)
    x=0.0
    z=0.0
    while(z < size):
        x = 0.0
        while (x<size):
            glVertex3f(x, 0.0, z)
            glVertex3f(x+step, 0.0, z)
            glVertex3f(x+step, 0.0, z+step)
            glVertex3f(x, 0.0, z+step)
            x += step
        z += step
    glEnd()

def DrawCube(size, resolution=1.0):
    step = size / resolution
    
    glPushMatrix();
    glTranslatef(-size/2, -size/2, -size/2);
    glNormal3f(0.0, -1.0, 0.0);  ##### test
    
    # top
    glPushMatrix();
    glTranslatef(0.0, size, 0.0);
    glScalef(1.0, -1.0, 1.0);
    DrawPlane(size, step);
    glPopMatrix();
    
    # bottom
    DrawPlane(size, step);
    
    # left
    glPushMatrix();
    glRotatef(90.0, 0.0, 0.0, 1.0);
    glScalef(1.0, -1.0, 1.0);
    DrawPlane(size, step);
    glPopMatrix();
    
    # right
    glPushMatrix();
    glTranslatef(size, 0.0, 0.0);
    glRotatef(90.0, 0.0, 0.0, 1.0);
    DrawPlane(size, step);
    glPopMatrix();
    
    # front
    glPushMatrix();
    glTranslatef(0.0, 0.0, size);
    glRotatef(90.0, -1.0, 0.0, 0.0);
    DrawPlane(size, step);
    glPopMatrix();
    
    # back
    glPushMatrix();
    glRotatef(90.0, -1.0, 0.0, 0.0);
    glScalef(1.0, -1.0, 1.0);
    DrawPlane(size, step);
    glPopMatrix();
    
    glPopMatrix();
    

def Display():
    global m_cubeAngle, m_flashlightOn, m_lightAngle, m_pSphere, CUBE_SIZE
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
    
    glLoadIdentity();
    gluLookAt(0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    
    if (m_flashlightOn):
        glEnable(GL_LIGHT0);
    else:
        glDisable(GL_LIGHT0);
    
    # position the red light
    glLightfv(GL_LIGHT1, GL_POSITION, redLightPos);
    
    # draw the red light
    glPushMatrix();
    glDisable(GL_LIGHTING);
    glTranslatef(redLightPos[0], redLightPos[1], redLightPos[2]);
    glColor3fv(redLightColor);
    gluSphere(m_pSphere, 0.2, 10, 10);
    glEnable(GL_LIGHTING);
    glPopMatrix();
    
    # position and draw the green light
    glPushMatrix();
    glDisable(GL_LIGHTING);
    glRotatef(m_lightAngle, 1.0, 0.0, 0.0);
    glRotatef(m_lightAngle, 0.0, 1.0, 0.0);
    glLightfv(GL_LIGHT2, GL_POSITION, greenLightPos);
    glTranslatef(greenLightPos[0], greenLightPos[1], greenLightPos[2]);
    glColor3fv(greenLightColor);
    gluSphere(m_pSphere, 0.2, 10, 10);
    glEnable(GL_LIGHTING);
    glPopMatrix();

    # set up cube's material
    cubeColor = [ 0.6, 0.7, 1.0 ];
    cubeSpecular = [ 1.0, 1.0, 1.0 ];
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, cubeColor);
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, cubeSpecular);
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 10.0);
    
    # position and draw the cube
    glPushMatrix();
    glRotatef(m_cubeAngle, 1.0, 1.0, 0.0);
    glRotatef(m_cubeAngle, 0.0, 0.0, 1.0);
    DrawCube(CUBE_SIZE, 1.0);
    glPopMatrix();
    

def OpenglInit():
    global m_pSphere
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glEnable(GL_DEPTH_TEST)
    #glDepthFunc(GL_LEQUAL)              ### test
    glEnable(GL_LIGHT0);
    glLightfv(GL_LIGHT0, GL_POSITION, flashLightPos);
    glLightfv(GL_LIGHT0, GL_AMBIENT, flashLightColor);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, flashLightColor);
    glLightfv(GL_LIGHT0, GL_SPECULAR, flashLightColor);
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, flashLightDir);
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 12.0);
    
    # set up static red light
    glEnable(GL_LIGHT1);
    glLightfv(GL_LIGHT1, GL_AMBIENT, redLightColor);
    glLightfv(GL_LIGHT1, GL_DIFFUSE, redLightColor);
    glLightfv(GL_LIGHT1, GL_SPECULAR, redLightColor);
    
    # set up moving green light
    glEnable(GL_LIGHT2);
    glLightfv(GL_LIGHT2, GL_AMBIENT, greenLightColor);
    glLightfv(GL_LIGHT2, GL_DIFFUSE, greenLightColor);
    glLightfv(GL_LIGHT2, GL_SPECULAR, greenLightColor);
    
    # get a quadric object for the light sphere
    m_pSphere = gluNewQuadric()
    
def GlfwInit():
    width = 640
    height = 640
    glfw.Init()
    glfw.OpenWindow(width, height, 8, 8, 8, 0, 24, 0, glfw.WINDOW)
    glfw.SetWindowTitle("glfw line")
    glfw.SetWindowSizeCallback(Reshape)
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)

def ChangeAngle(dt):
    global CUBE_DEG_PER_S, LIGHT_DEG_PER_S, m_cubeAngle, m_lightAngle
    m_cubeAngle += CUBE_DEG_PER_S * dt;
    if (m_cubeAngle > 360.0):
        m_cubeAngle = 0.0;
    m_lightAngle += LIGHT_DEG_PER_S * dt;
    if (m_lightAngle > 360.0):
        m_lightAngle = 0.0;

GlfwInit()
OpenglInit()
while(True):
    Display()
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)
    ChangeAngle(0.03)

glfw.Terminate()