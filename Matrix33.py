from Vector3 import Vector3
from math import sin,cos,radians,degrees

class Matrix33:
    # (i,j) = (row,column)
    # | 00 01 02 |
    # | 10 11 12 |
    # | 20 21 22 |
    def __init__(self, arr = [0.0]*9):
        self.array = arr

    def get(self,i,j):
        return self.array[(3*i)+j]

    def set(self,i,j,v):
        self.array[(3*i)+j] = v

    def getCol(self,j):
        return Vector3(self.get(0,j),self.get(1,j),self.get(2,j))

    def __mul__(self,mat):
        m = Matrix33()
        for i in xrange(3):
            for j in xrange(3):
                s = sum([self.get(i,k)*mat.get(k,j) for k in xrange(3)])
                m.set(i,j,s)
        return m

    def __str__(self):
        return "|%f\t%f\t%f|\n|%f\t%f\t%f|\n|%f\t%f\t%f|" % tuple(self.array)

def MatrixRU(alpha):
    r = radians(alpha)
    s = sin(r)
    c = cos(r)
    return Matrix33([c, s, 0,-s, c, 0, 0, 0, 1])

def MatrixRL(alpha):
    r = radians(alpha)
    s = sin(r)
    c = cos(r)
    return Matrix33([c, 0,-s, 0, 1, 0, s, 0, c])

def MatrixRH(alpha):
    r = radians(alpha)
    s = sin(r)
    c = cos(r)
    return Matrix33([1, 0, 0, 0, c,-s, 0, s, c])

def Vec2Mat(v1,v2,v3):
    return Matrix33([v1.x,v2.x,v3.x,v1.y,v2.y,v3.y,v1.z,v2.z,v3.z])

def rotateVec3(v1,v2,v3,R):
    m = Vec2Mat(v1,v2,v3)*R
    return (m.getCol(0).normalize(),m.getCol(1).normalize(),m.getCol(2).normalize())
