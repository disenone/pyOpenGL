# encoding: utf-8


from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
from numpy.lib.scimath import sqrt
from OpenGL.raw.GL.EXT.fog_coord import glFogCoordfEXT

m_windowWidth = 0;
m_windowHeight = 0;
heightmap = []
terrain_size = 0
max_height = 10.0
max_fog_height = max_height * 0.5
scale_factor = 256.0 / max_height
water_height = 0.8


def MouseHandler(button, state):
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        exit(0)


def KeyboardHandler(key, state):
    if(state == glfw.GLFW_PRESS):
        if(key == 'S'):
            pass

def WindowCLose():
    exit(0)

def ComputeFogCoord(height):
    global max_fog_height, water_height
    if(height > max_fog_height):
        height = max_fog_height
    elif(height < water_height):
        height = water_height
    
    height = height - water_height
    height = 1.0 - (height / (max_fog_height - water_height))
    return height

def DrawTerrain():
    global scale_factor, heightmap, terrain_size, max_height, water_height
    
    # draw the terrain
    for z in range(terrain_size - 1):  # test: why -1
        glBegin(GL_TRIANGLE_STRIP)
        
        for x in range(terrain_size):
            scaledHeight = heightmap[z * terrain_size + x] / scale_factor
            nextScaledHeight = heightmap[(z + 1) * terrain_size + x] / scale_factor

            if(glFogCoordfEXT):  # test
                glFogCoordfEXT(ComputeFogCoord(scaledHeight))
            glColor3f(0.1, 0.5 + 0.5 * scaledHeight / max_height, 0.1)
            glVertex3f(x - terrain_size / 2.0, scaledHeight, z - terrain_size / 2.0)
            
            if(glFogCoordfEXT):  # test
                glFogCoordfEXT(ComputeFogCoord(nextScaledHeight))
            glColor3f(0.1, 0.5 + 0.5 * nextScaledHeight / max_height, 0.1)
            glVertex3f(x - terrain_size / 2.0, nextScaledHeight, z + 1 - terrain_size / 2.0)            
        
        glEnd()

    # draw the water
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    # test: why 2.1 ?
    glVertex3f(-terrain_size / 2.1, water_height, terrain_size / 2.1)
    glVertex3f(terrain_size / 2.1, water_height, terrain_size / 2.1)
    glVertex3f(terrain_size / 2.1, water_height, -terrain_size / 2.1)
    glVertex3f(-terrain_size / 2.1, water_height, -terrain_size / 2.1)
    glEnd()
    
def DrawLine():
    glDisable(GL_DEPTH_TEST);
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    # 画两条线，四个网格
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
    gluPerspective(52.0, float(width) / height, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    global m_windowHeight, m_windowWidth
    m_windowWidth = width
    m_windowHeight = height

def Display():
    glClearColor(0.7, 0.7, 0.9, 1.0)  # test: why?
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    global terrain_size, max_height, m_windowHeight, m_windowWidth
    # set up the view
    glLoadIdentity()
    gluLookAt(terrain_size / 3.0, max_height + 1.0, terrain_size / 3.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)
    
    # use grey for all fog
    fog_color = [0.5, 0.5, 0.5]
    glFogfv(GL_FOG_COLOR, fog_color)
    
    # without fog
    glViewport(0, m_windowHeight / 2, m_windowWidth / 2, m_windowHeight / 2);
    DrawTerrain();
    
    # with linearo fog
    glEnable(GL_FOG);
    glFogi(GL_FOG_MODE, GL_LINEAR);
    glFogf(GL_FOG_START, 10.0);
    glFogf(GL_FOG_END, 60.0);
    glViewport(m_windowWidth / 2, m_windowHeight / 2, m_windowWidth / 2, m_windowHeight / 2);
    DrawTerrain();
    
    # with exponential fog
    glFogi(GL_FOG_MODE, GL_EXP);
    glFogf(GL_FOG_DENSITY, 0.03);
    glViewport(0, 0, m_windowWidth / 2, m_windowHeight / 2);
    DrawTerrain();
    
    # with fog coords
    glFogi(GL_FOG_COORD_SRC, GL_FOG_COORD);
    glFogi(GL_FOG_MODE, GL_EXP2);
    glFogf(GL_FOG_DENSITY, 1.2);
    glViewport(m_windowWidth / 2, 0, m_windowWidth / 2, m_windowHeight / 2);
    DrawTerrain()
    
    
    # switch back to defaults
    glFogi(GL_FOG_COORD_SRC, GL_FRAGMENT_DEPTH);
    glDisable(GL_FOG);
    
    DrawLine();

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
    
    glfw.SetMouseButtonCallback(MouseHandler)
    glfw.SetKeyCallback(KeyboardHandler)
    glfw.SetWindowCloseCallback(WindowCLose)
    
    global heightmap, terrain_size
    tmpheightmap = open("heightmap.raw", 'rb').read()
    for c in tmpheightmap:
        heightmap.append(ord(c))
    print heightmap
    terrain_size = int(sqrt(len(heightmap)))
    print terrain_size
    
    if(glFogCoordfEXT):  # test
        print 'ok'

init()
while(True):
    Display()
    glfw.SwapBuffers()
    if(glfw.GetKey(glfw.KEY_ESC) == glfw.GLFW_PRESS):
        break
    time.sleep(0.1)

glfw.Terminate()

