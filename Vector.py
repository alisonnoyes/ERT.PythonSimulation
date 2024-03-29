# -------------------
# A three-dimensional Vector which can represent location, rotation, etc.
# -------------------

from __future__ import division
import math

class Vector:

    def __init__(self, x, y, z):
        self.x = x;
        self.y = y;
        self.z = z;

    def addToSelf(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def multiplyToSelf(self, scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar

    def magnitude(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))

    def normalize(self):
        mag = self.magnitude()
        if (mag == 0): return Vector(0, 0, 0)
        return Vector(self.x / mag, self.y / mag, self.z / mag)

    def zero(self):
        self.x = 0
        self.y = 0
        self.z = 0

    # -------------------
    # Static methods
    # -------------------
    def multiply(vector, scalar):
        return Vector(vector.x * scalar, vector.y * scalar, vector.z * scalar)

    def subtract(a, b):
        return Vector(a.x - b.x, a.y - b.y, a.z - b.z)

    def add(a, b):
        return Vector(a.x + b.x, a.y + b.y, a.z + b.z)

    def copy(vector):
        return Vector(vector.x, vector.y, vector.z)

    def distance(a, b):
        return math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2) + math.pow(a.z - b.z, 2))

    #@staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z
