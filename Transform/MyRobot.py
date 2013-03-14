# encoding: utf-8

from OpenGL.GL import *
from OpenGL.GLU import *

class MyRobot:
    __Forward = 1
    __Backward = 0
    __Left = 0
    __Right = 1
    __legStates = [__Forward, __Backward]
    __armStates = [__Forward, __Backward]
    
    __legAngles = [0.0, 0.0]
    __armAngles = [0.0, 0.0]
    
    def __init__(self):
        pass
    
    def Prepare(self, dt):
        for side in range(0, 2):
            if (self.__armStates[side] == self.__Forward):
                self.__armAngles[side] += 20.0 * dt;
            else:
                self.__armAngles[side] -= 20.0 * dt;
    
            if (self.__armAngles[side] >= 15.0):
                self.__armStates[side] = self.__Backward;
            elif (self.__armAngles[side] <= -15.0):
                self.__armStates[side] = self.__Forward;
    
            if (self.__legStates[side] == self.__Forward):
                self.__legAngles[side] += 20.0 * dt;
            else:
                self.__legAngles[side] -= 20.0 * dt;
    
            if (self.__legAngles[side] >= 15.0):
                self.__legStates[side] = self.__Backward
            elif (self.__legAngles[side] <= -15.0):
                self.__legStates[side] = self.__Forward;
        print "LeftArmLeg:", self.__armStates[self.__Left], self.__legStates[self.__Left]
        print "RightArmLeg:", self.__armStates[self.__Right], self.__legStates[self.__Right]

    def DrawRobot(self, xpos, ypos, zpos):
        glPushMatrix()
        
        glTranslatef(xpos, ypos, zpos)
        self.__DrawHead(1.0, 2.0, 0.0)
        self.__DrawTorso(1.5, 0.0, 0.0)
        
        glPushMatrix()
        glTranslatef(0.0, -0.5, 0.0)
        glRotatef(self.__armAngles[self.__Left], 1.0, 0.0, 0.0)
        self.__DrawArm(2.5, 0.0, -0.5)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.0, -0.5, 0.0)
        glRotatef(self.__armAngles[self.__Right], 1.0, 0.0, 0.0)
        self.__DrawArm(-1.5, 0.0, -0.5)
        glPopMatrix()
        
        glPushMatrix();                    
        glTranslatef(0.0, -0.5, 0.0);
        glRotatef(self.__legAngles[self.__Left], 1.0, 0.0, 0.0);
        self.__DrawLeg(-0.5, -5.0, -0.5);
        glPopMatrix();        
        
        glPushMatrix();
        glTranslatef(0.0, -0.5, 0.0);
        glRotatef(self.__legAngles[self.__Right], 1.0, 0.0, 0.0);
        self.__DrawLeg(1.5, -5.0, -0.5);
        glPopMatrix();
        
        glPopMatrix()

    def __DrawCube(self, xpos=0.0, ypos=0.0, zpos=0.0):
        glPushMatrix();
        glTranslatef(xpos, ypos, zpos);
        glBegin(GL_POLYGON);
        glVertex3f(0.0, 0.0, 0.0);    
        glVertex3f(0.0, 0.0, -1.0);
        glVertex3f(-1.0, 0.0, -1.0);
        glVertex3f(-1.0, 0.0, 0.0);
        glVertex3f(0.0, 0.0, 0.0);    
        glVertex3f(-1.0, 0.0, 0.0);
        glVertex3f(-1.0, -1.0, 0.0);
        glVertex3f(0.0, -1.0, 0.0);
        glVertex3f(0.0, 0.0, 0.0);    
        glVertex3f(0.0, -1.0, 0.0);
        glVertex3f(0.0, -1.0, -1.0);
        glVertex3f(0.0, 0.0, -1.0);
        glVertex3f(-1.0, 0.0, 0.0);    
        glVertex3f(-1.0, 0.0, -1.0);
        glVertex3f(-1.0, -1.0, -1.0);
        glVertex3f(-1.0, -1.0, 0.0);
        glVertex3f(0.0, 0.0, 0.0);    
        glVertex3f(0.0, -1.0, -1.0);
        glVertex3f(-1.0, -1.0, -1.0);
        glVertex3f(-1.0, -1.0, 0.0);
        glVertex3f(0.0, 0.0, 0.0);    
        glVertex3f(-1.0, 0.0, -1.0);
        glVertex3f(-1.0, -1.0, -1.0);
        glVertex3f(0.0, -1.0, -1.0);
        glEnd();
        glPopMatrix();
    
    
    def __DrawArm(self, xpos, ypos, zpos):
        glPushMatrix()
        glColor3f(1.0, 0.0, 0.0)
        glTranslatef(xpos, ypos, zpos)
        glScale(1.0, 4.0, 1.0)
        self.__DrawCube()
        glPopMatrix()
    
    def __DrawHead(self, xpos, ypos, zpos):
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glTranslatef(xpos, ypos, zpos)
        glScalef(2.0, 2.0, 2.0)
        self.__DrawCube()
        glPopMatrix()
    
    def __DrawTorso(self, xpos, ypos, zpos):
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        glTranslatef(xpos, ypos, zpos)
        glScalef(3.0, 5.0, 2.0)
        self.__DrawCube()
        glPopMatrix()
    
    def __DrawLeg(self, xpos, ypos, zpos):
        glPushMatrix()
        glTranslatef(xpos, ypos, zpos)
        
        glPushMatrix()
#        glTranslatef(0.0, -5.0, 0.0)
        self.__DrawFoot(0.0, -5.0, 0.0)
        glPopMatrix()
        
        glScalef(1.0, 5.0, 1.0)
        glColor3f(1.0, 1.0, 0.0)
        self.__DrawCube()
        glPopMatrix()
    
    def __DrawFoot(self, xpos, ypos, zpos):
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glTranslatef(xpos, ypos, zpos)
        glScalef(1.0, 0.5, 3.0)
        self.__DrawCube()
        glPopMatrix()