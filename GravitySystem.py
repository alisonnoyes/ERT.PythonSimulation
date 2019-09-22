# -------------------
# Stores the bodies in the system and applies the appropriate forces
# -------------------

from __future__ import division

from Vector import Vector
from Body import Body
from Collision import Collision

import math

class GravitySystem:

    elasticity = 1
    gravityLimit = 0

    def __init__(self):
        self.centralBody = None
        self.orbitingBodies = []
        self.playerBodies = ["empty", "empty"]

        # Default physics constants
        self.G = 1
        self.scale = 1
        self.timeScale = 1
        self.bodyScale = 1
        self.centralBodyScale = 1
        self.systemRadius = 5
        self.handMass = 1

        self.statistics = ""

    def updateBody(self, updated):
        if (updated.name[:4] == "left"): self.playerBodies[0] = updated
        if (updated.name[:5] == "right"): self.playerBodies[1] = updated
        if (updated.name == "emptyleft"): self.playerBodies[0] = "empty"
        if (updated.name == "emptyright"):self.playerBodies[1] = "empty"

    # -------------------
    # Mutators
    # -------------------
    def addBody(self, newBody):
        newBody.setScale(self.scale)
        newBody.setBodyScale(self.bodyScale)
        newBody.centralBody = self.centralBody

        self.orbitingBodies.append(newBody)

    def setScale(self, newScale):
        self.scale = newScale

        self.centralBody.setScale(newScale)

        for b in self.orbitingBodies:
            b.setScale(newScale)

    def setBodyScale(self, newScale):
        self.bodyScale = newScale

        self.centralBody.setBodyScale(newScale * self.centralBodyScale)

        for b in self.orbitingBodies:
            b.setBodyScale(newScale)

    # -------------------
    # Accessors
    # -------------------
    def getBodyWithName(self, name):
        for b in self.orbitingBodies:
            if b.name.lower() == name.lower():
                return b

        if self.centralBody.name.lower() == name.lower():
            return self.centralBody

        return False
    
    # -------------------
    # Physics
    # -------------------

    # Get force on a caused by b
    def getForceOn(self, a, b):
        dist = Vector.distance(a.location, b.location)
        if dist <= GravitySystem.gravityLimit: return Vector(0, 0, 0)
        
        mag = self.G * a.mass * b.mass / math.pow(dist, 2)
        dir = Vector.subtract(b.location, a.location).normalize()

        return Vector.multiply(dir, mag)

    def applyForces(self):
        for b in self.orbitingBodies:
            force = self.getForceOn(b, self.centralBody)
            b.addForce(force)
            for other in self.orbitingBodies:
                bodyForce = self.getForceOn(b, other)
                #b.addForce(bodyForce)
            for other in self.playerBodies:
                if other != "empty":
                    handForce = self.getForceOn(b, other)
                    b.addForce(handForce)

    def applyImpulses(self):
        for b in self.orbitingBodies:
            collidedThisFrame = False
            for other in self.orbitingBodies:
                imp = Collision.getCollisionImpulse(b, other, self.elasticity)
                if (imp.x != 0 or imp.y != 0 or imp.z != 0): collidedThisFrame = True
                elif (imp.x == 123.4 and imp.y == 123.4 and imp.z == 123.4): collidedThisFrame = True
                else: b.addImpulse(imp)
            '''   
            for other in self.playerBodies:
                if other != "empty":
                    imp = Collision.getCollisionImpulse(b, other, self.elasticity)
                    if (imp.x != 0 or imp.y != 0 or imp.z != 0): collidedThisFrame = True
                    elif (imp.x == 123.4 and imp.y == 123.4 and imp.z == 123.4): collidedThisFrame = True
                    else: b.addImpulse(imp)
            '''
            # Don't want to apply impulses multiple times
            if collidedThisFrame: b.colliding = True;
            else: b.colliding = False

    def UpdateStatistics(self):
        self.statistics = "";

        self.statistics += self.centralBody.name + "<line>"
        self.statistics += "Mass: " + str(self.centralBody.mass) + "<line>"
        self.statistics += "Radius: " + str(self.centralBody.bodyRadius) + "<line><line>"

        for b in self.orbitingBodies:
            self.statistics += b.name + "<line>"
            self.statistics += "Mass: " + str(b.mass) + "<line>"
            self.statistics += "Radius:" + str(b.bodyRadius) + "<line>"
            self.statistics += "Orbit radius:" + str(b.orbitRadius) + "<line>"
            self.statistics += "Orbit speed:" + str(b.orbitSpeed) + "<line><line>"

    def TickSystem(self, dt):
        self.applyForces()
        self.applyImpulses()

        toRemove = []

        for b in self.orbitingBodies:
            b.tick(dt * self.timeScale)
            if b.scaledOrbitRadius > self.systemRadius:
                toRemove.append(b)

        for b in toRemove:
            self.orbitingBodies.remove(b)

        self.UpdateStatistics()
        return toRemove
