from math import acos,sqrt,degrees

class Vector3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def dot_product(self,vec):
        return (self.x*vec.x) + (self.y*vec.y) + (self.z*vec.z)

    def scalar_product(self,alpha):
        return Vector3(self.x*alpha,self.y*alpha,self.z*alpha)

    def cross_product(self,vec):
        x = self.y*vec.z - self.z*vec.y
        y = self.z*vec.x - self.x*vec.z
        z = self.x*vec.y - self.y*vec.x
        return Vector3(x,y,z)

    def matrix_product(self,matrix):
        x = self.x*matrix.get(0,0) + self.y*matrix.get(0,1) + self.z*matrix.get(0,2)
        y = self.x*matrix.get(1,0) + self.y*matrix.get(1,1) + self.z*matrix.get(1,2)
        z = self.x*matrix.get(2,0) + self.y*matrix.get(2,1) + self.z*matrix.get(2,2)
        return Vector3(x,y,z)

    def __add__(self,vec):
        return Vector3(self.x+vec.x,self.y+vec.y,self.z+vec.z)

    def __iadd__(self,vec):
        self.x += vec.x
        self.y += vec.y
        self.z += vec.z
        return self

    def __sub__(self,vec):
        return Vector3(self.x-vec.x,self.y-vec.y,self.z-vec.z)

    def __isub__(self,vec):
        self.x -= vec.x
        self.y -= vec.y
        self.z -= vec.z
        return self

    def length(self):
        return sqrt((self.x*self.x)+(self.y*self.y)+(self.z*self.z))

    def getAngle(self,vec):
        l = self.length()*vec.length()
        return degrees(acos(self.dot_product(vec)/l)) if l!=0 else 0

    def normalize(self):
        l = self.length()
        return self.scalar_product(0 if l==0 else 1.0/l)

    def __str__(self):
        return "<%f, %f, %f>" % (self.x,self.y,self.z)

    def copy(self):
        return Vector3(self.x,self.y,self.z)
