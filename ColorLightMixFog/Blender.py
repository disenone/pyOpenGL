# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
from OpenGL.raw.GL.EXT.blend_color import glBlendColorEXT
from OpenGL.raw.GL.EXT.blend_minmax import glBlendEquationEXT
from glfw import GLFW_PRESS

equationDict = {GL_FUNC_ADD: "GL_FUNC_ADD",
                GL_FUNC_SUBTRACT: "GL_FUNC_SUBTRACT",
                GL_FUNC_REVERSE_SUBTRACT: "GL_FUNC_REVERSE_SUBTRACT",
                GL_MIN: "GL_MIN",
                GL_MAX: "GL_MAX"}
srcFactorDict = {GL_ZERO: "GL_ZERO",
                 GL_ONE: "GL_ONE",
                 GL_SRC_COLOR: "GL_SRC_COLOR",
                 GL_ONE_MINUS_SRC_COLOR: "GL_ONE_MINUS_SRC_COLOR",
                 GL_SRC_ALPHA: "GL_SRC_ALPHA",
                 GL_ONE_MINUS_SRC_ALPHA: "GL_ONE_MINUS_SRC_ALPHA",
                 GL_DST_ALPHA: "GL_DST_ALPHA",
                 GL_ONE_MINUS_DST_ALPHA: "GL_ONE_MINUS_DST_ALPHA",
                 GL_DST_COLOR: "GL_DST_COLOR",
                 GL_ONE_MINUS_DST_COLOR: "GL_ONE_MINUS_DST_COLOR",
                 GL_SRC_ALPHA_SATURATE: "GL_SRC_ALPHA_SATURATE",
                 GL_CONSTANT_COLOR: "GL_CONSTANT_COLOR",
                 GL_ONE_MINUS_CONSTANT_COLOR: "GL_ONE_MINUS_CONSTANT_COLOR",
                 GL_CONSTANT_ALPHA: "GL_CONSTANT_ALPHA",
                 GL_ONE_MINUS_CONSTANT_ALPHA: "GL_ONE_MINUS_CONSTANT_ALPHA"}
dstFactorDict = {GL_ZERO: "GL_ZERO",
                 GL_ONE: "GL_ONE",
                 GL_SRC_COLOR: "GL_SRC_COLOR",
                 GL_ONE_MINUS_SRC_COLOR: "GL_ONE_MINUS_SRC_COLOR",
                 GL_SRC_ALPHA: "GL_SRC_ALPHA",
                 GL_ONE_MINUS_SRC_ALPHA: "GL_ONE_MINUS_SRC_ALPHA",
                 GL_DST_ALPHA: "GL_DST_ALPHA",
                 GL_ONE_MINUS_DST_ALPHA: "GL_ONE_MINUS_DST_ALPHA",
                 GL_DST_COLOR: "GL_DST_COLOR",
                 GL_ONE_MINUS_DST_COLOR: "GL_ONE_MINUS_DST_COLOR",
                 GL_SRC_ALPHA_SATURATE: "GL_SRC_ALPHA_SATURATE",
                 GL_CONSTANT_COLOR: "GL_CONSTANT_COLOR",
                 GL_ONE_MINUS_CONSTANT_COLOR: "GL_ONE_MINUS_CONSTANT_COLOR",
                 GL_CONSTANT_ALPHA: "GL_CONSTANT_ALPHA",
                 GL_ONE_MINUS_CONSTANT_ALPHA: "GL_ONE_MINUS_CONSTANT_ALPHA"}
nextEquation = {GL_FUNC_ADD: GL_FUNC_SUBTRACT,
                GL_FUNC_SUBTRACT: GL_FUNC_REVERSE_SUBTRACT, 
                GL_FUNC_REVERSE_SUBTRACT: GL_MIN,
                GL_MIN: GL_MAX,
                GL_MAX: GL_FUNC_ADD}
nextsrcFactor = {GL_ONE: GL_SRC_COLOR,
                 GL_SRC_ALPHA_SATURATE: GL_CONSTANT_COLOR,
                 GL_ONE_MINUS_CONSTANT_ALPHA: GL_ZERO}
nextdstFactor = {GL_ONE: GL_SRC_COLOR,
                 GL_ONE_MINUS_DST_COLOR: GL_CONSTANT_COLOR,
                 GL_ONE_MINUS_CONSTANT_ALPHA: GL_ZERO}

DISK_DEG_PER_S = 90.0
DISK_LIMIT = 3.0
m_srcFactor = GL_SRC_ALPHA
m_dstFactor = GL_ONE_MINUS_SRC_ALPHA
m_blendEquation = GL_FUNC_ADD
m_pDisk = 0
m_diskPos = 0.0
m_diskRot = 0.0
increment = 0.4

def MouseHandler(button, state):
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        exit(0)

def NextBlendEquation():
    global nextEquation, m_blendEquation
    try: 
        m_blendEquation = nextEquation[m_blendEquation]
    except KeyError:
        pass
    
def NextSrcFactor():
    global nextsrcFactor, m_srcFactor
    try:
        m_srcFactor = nextsrcFactor[m_srcFactor]
    except KeyError:
        m_srcFactor += 1

def NextDstFactor():
    global nextdstFactor, m_dstFactor
    try:
        m_dstFactor = nextdstFactor[m_dstFactor]
    except KeyError:
        m_dstFactor += 1

def KeyboardHandler(key, state):
    if(state == glfw.GLFW_PRESS):
        if(key == 'S'):
            NextSrcFactor()
        elif(key == 'D'):
            NextDstFactor()
        elif(key == 'E'):
            NextBlendEquation()

def GetBlendEquation():
    global equationDict, m_blendEquation
    try:
        return equationDict[m_blendEquation]
    except KeyError:
        raise Exception("Unknown Equantion: " + m_blendEquation)

def GetSrcFactor():
    global srcFactorDict, m_srcFactor
    try:
        return srcFactorDict[m_srcFactor]
    except KeyError:
        raise Exception("Unknown Source Factor: "+ m_srcFactor)

def GetDstFactor():
    global dstFactorDict, m_dstFactor
    try:
        return dstFactorDict[m_dstFactor]
    except KeyError:
        raise Exception("Unknown Dest Factor: "+m_dstFactor)


def Reshape(width, height):
    if(height == 0):
        height = 1    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(52.0, float(width)/height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def Display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()
    
    gluLookAt(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    
    global m_srcFactor, m_dstFactor, m_blendEquation
    glBlendFunc(m_srcFactor, m_dstFactor)
    if(glBlendEquationEXT):
        glBlendEquationEXT(m_blendEquation)
        
    glColor4f(0.4, 0.8, 0.6, 0.7)
    gluDisk(m_pDisk, 0.0, 4.0, 64, 16)
    
    global m_diskPos, m_diskRot
    glEnable(GL_BLEND)
    glTranslatef(0.0, m_diskPos, 2.0)
    glRotatef(m_diskRot, 1.0, 0.0, 0.0)
    glColor4f(0.7, 0.3, 0.5, 0.6)
    gluDisk(m_pDisk, 0.5, 2.0, 32, 16)
    glDisable(GL_BLEND)

def Prepare(dt):   
    if(dt > 1.0):
        dt = 1.0
    global increment, m_diskPos, DISK_LIMIT
    if(m_diskPos > DISK_LIMIT or m_diskPos < -DISK_LIMIT):
        increment *= -1.0
    
    m_diskPos += increment * dt
    global m_diskRot, DISK_DEG_PER_S
    m_diskRot += DISK_DEG_PER_S * dt
    
    if(m_diskRot > 360.0):
        m_diskRot = 0.0

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

    global m_pDisk    
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)
    m_pDisk = gluNewQuadric()
    
    if( glBlendColorEXT ):
        print "found"
        glBlendColorEXT(0.5, 0.5, 0.5, 0.5)


init()
while(True):
    Display()
    glfw.SwapBuffers()
    if( glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS ):
        break
    time.sleep(0.02)
    Prepare(0.02)
    glfw.SetWindowTitle("src:"+srcFactorDict[m_srcFactor]+
                        ";dst:"+dstFactorDict[m_dstFactor]+
                        ";equ:"+equationDict[m_blendEquation])

glfw.Terminate()

