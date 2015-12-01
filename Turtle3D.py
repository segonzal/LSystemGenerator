from math import acos,degrees,atan2
from Vector3 import Vector3
from Matrix33 import *

class Turtle3D:
    def __init__(self):
        self.distance = 10
        self.delta = 90
        self.width = 5
        # Needed to compute the transformations
        self.H = Vector3( 0, 0, 1) # Heading vector
        self.L = Vector3( 1, 0, 0) # Left vector
        self.U = Vector3( 0, 1, 0) # Up vector
        self.position = Vector3(0,0,0)

        self.branch = []
        self.polygon = []

    # F: Move forward and draw a line.
    def forwardF(self,distance=self.distance):pass
    # f: Move forward without drawing.
    def forwardf(self,distance=self.distance): pass
    # +: Turn left.
    def turnL(self,delta=self.delta): pass
    # -: Turn right.
    def turnR(self,delta=self.delta): pass
    # ^: Pitch up.
    def pitchU(self,delta=self.delta): pass
    # &: Pitch down.
    def pitchD(self,delta=self.delta): pass
    # \: Roll left.
    def rollL(self,delta=self.delta): pass
    # /: Roll right.
    def rollR(self,delta=self.delta): pass
    # |: Turn around.
    def turnA(self): pass
    # $: Rotate turtle to vertical.
    def rotVertical(self): pass
    # [: Start a branch.
    def startBranch(self): pass
    # ]: Complete a branch.
    def completeBranch(self): pass
    # {: Start a polygon.
    def startPoly(self): pass
    # G: Move forward and draw a line. Do not record a vertex.
    def forwardG(self,distance=self.distance): pass
    # .: Record a vertex in the current polygon.
    def recordVertexPoly(self): pass
    # }: Complete a polygon.
    def completePoly(self): pass
    # ~: Incorporate a predefined surface.
    def incorporateSurface(self): pass
    # !: Decrement the diameter of segments.
    def decrementDiameter(self,width=self.width): pass
    # ': Increment the current color index.
    def incrementColorIdx(self): pass
    # %: Cut out the remainder of the branch.
    def cutoutBranch(self): pass

    # def draw(self):
    #     print "translate([%f,%f,%f])" % (self.position.x,self.position.y,self.position.z),
    #
    #     self.position += self.H.scalar_product(self.d)
    #
    #     # This configuration works for turtle2d in U and L
    #     b = -degrees(acos(self.H.z))
    #     c = -degrees(atan2(self.H.x,self.H.y))
    #
    #     print "rotate([%f,0,%f])" % (b,c),
    #
    #     print "cylinder(%f,%f,%f,false);" % (self.d,self.w,self.w*self.s)
    #     self.w *= self.s
    #
    # def forward(self):
    #     self.position += self.H.scalar_product(self.d)
    #
    # def turn(self,angle):
    #     m = MatrixRU(angle)
    #     (self.H,self.L,self.U) = rotateVec3(self.H,self.L,self.U,m)
    #
    # def pitch(self,angle):
    #     m = MatrixRL(angle)
    #     (self.H,self.L,self.U) = rotateVec3(self.H,self.L,self.U,m)
    #
    # def roll(self,angle):
    #     m = MatrixRH(angle)
    #     (self.H,self.L,self.U) = rotateVec3(self.H,self.L,self.U,m)
    #
    # def turnAround(self):
    #     m = MatrixRU(180)
    #     (self.H,self.L,self.U) = rotateVec3(self.H,self.L,self.U,m)
    #
    # # Alphabet
    # # F: move forward a step of d.
    # # f: move forward without drawing a line
    # # +: Turn left by angle delta, using rotation RU(delta)
    # # -: Turn right by angle delta, using rotation RU(-delta)
    # # &: Pitch down by angle delta, using rotation RL(delta)
    # # ^: Pitch up by angle delta, using rotation RL(-delta)
    # # \: Roll left by angle delta, using rotation RH(delta)
    # # /: Roll right by angle delta, using rotation RH(-delta)
    # # |: Turn around, using rotation RU(180)
    # # [: Save the state = (Position, H, L, U) in stack
    # # ]: Pops a state and restores it
    # def travel(self,path,delta):
    #     for i in path:
    #         if i == "F":
    #             self.draw()
    #         elif i == "f":
    #             self.forward()
    #         elif i == "+":
    #             self.turn(delta)
    #         elif i == "-":
    #             self.turn(-delta)
    #         elif i == "&":
    #             self.pitch(delta)
    #         elif i == "^":
    #             self.pitch(-delta)
    #         elif i == "\\":
    #             self.roll(delta)
    #         elif i == "/":
    #             self.roll(-delta)
    #         elif i == "|":
    #             self.turnAround()
    #         elif i == "[":
    #             state = (self.position.copy(),self.H.copy(),self.L.copy(),self.U.copy(),self.w)
    #             self.stack.append(state)
    #         elif i == "]":
    #             (P,H,L,U,w) = self.stack.pop()
    #             self.position = P
    #             self.H = H
    #             self.L = L
    #             self.U = U
    #             self.w = w
