# -------------------
# Converts a GravitySystem to JSON format and vice versa
# -------------------

from GravitySystem import GravitySystem
from Body import Body
from Vector import Vector

import json

class SystemSerializer:

    def bodyToJson(body):
        data = {
            "name" : body.name,
            "mass" : body.mass,
            "radius" : body.bodyRadius,
            "locationX" : body.location.x,
            "locationY" : body.location.y,
            "locationZ" : body.location.z,
            "orbitRadius" : body.orbitRadius,
            "orbitSpeed" : body.orbitSpeed,
            "directionX" : body.orbitDirection.x,
            "directionY" : body.orbitDirection.y,
            "directionZ" : body.orbitDirection.z
        }
        jsonString = json.dumps(data)
        return jsonString

    def systemToJson(system):
        jsonObjs = []

        # Generate dictionaries for each part of the system and load into the list
        systemData = {
            "gravityConstant" : system.G,
            "scale" : system.scale,
            "timeScale" : system.timeScale,
            "bodyScale" : system.bodyScale,
            "centralBodyScale" : system.centralBodyScale,
            "elasticity" : system.elasticity,
            "bodyCount" : len(system.orbitingBodies) + 1,
            "centralBodyName" : system.centralBody.name,
            "handMass" : system.handMass,
            "boundary" : system.systemRadius
        }
        systemJson = json.dumps(systemData)
        jsonObjs.append(systemJson)

        centralJson = bodyToJson(system.centralBody)
        jsonObjs.append(centralJson)

        for b in system.orbitingBodies:
            bodyJson = bodyToJson(b)
            jsonObjs.append(bodyJson)

        return jsonObjs

    @staticmethod
    def jsonToSystem(jsonObjs):
        sysObj = str(jsonObjs[0])
        sysLoadStr = sysObj.replace("u'", '"').replace("'", '"').replace("L,", ",")
        systemDict = json.loads(sysLoadStr)

        system = GravitySystem()
        system.G = systemDict["gravityConstant"]
        system.scale = systemDict["scale"]
        system.timeScale = systemDict["timeScale"]
        system.bodyScale = systemDict["bodyScale"]
        system.centralBodyScale = systemDict["centralBodyScale"]
        system.elasticity = systemDict["elasticity"]
        system.systemRadius = systemDict["boundary"]
        system.handMass = systemDict["handMass"]

        centralBody = None
        for i in range(len(jsonObjs) - 1):
            bodyObj = str(jsonObjs[i + 1])
            bodyLoadStr = bodyObj.replace("u'", '"').replace("'", '"').replace("L,", ",")
            dict = json.loads(bodyLoadStr)

            body = Body(dict["name"], dict["mass"], dict["radius"])

            if (body.name == systemDict["centralBodyName"]):
                centralBody = body
                system.centralBody = body
                centralBody.setScale(system.scale)
                centralBody.setBodyScale(system.bodyScale * system.centralBodyScale)
                print "Central body found:", centralBody.name

            if (centralBody != None):
                body.centralBody = centralBody
            else:
                print body.name, "has no central body"

            body.setLocation(Vector(dict["locationX"], dict["locationY"], dict["locationZ"]), False)

            if (body.name != systemDict["centralBodyName"]):
                body.orbitDirection = Vector(dict["directionX"], dict["directionY"], dict["directionZ"])
                body.setSpeed(dict["orbitSpeed"])
                body.setOrbitRadius(dict["orbitRadius"])

                system.addBody(body);

        return system
