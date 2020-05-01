# This program creates an Auto Rigger, a tool that creates a skeleton for 
# rigging a humanoid 3D model. It consists of a window with several input boxes 
# that tie to how many joints of each type. It will mirror specific joints across
# the z axis.

#Left to accomplish: create handles, and aim constraints

import maya.cmds as base

#Create the window with the controls
base.window("Auto Rigger")
base.rowColumnLayout(nc = 2)

#base.button(l = "Create Locators", w = 200, c = "createLocators()")
#base.button(l = "Delete Locators", w = 200, c = "deleteLocators()")

#Spine Count Input
base.text("Spine Count", l = "Spine Count")
spineCount = base.intField(minValue = 2, maxValue = 10, v = 3)

#Neck Count Input
base.text("Neck Count", l = "Neck Count")
neckCount = base.intField(minValue = 0, maxValue = 10, value = 1)

#Finger Count Input
base.text("Finger Count", l = "Finger Count")
fingerCount = base.intField(minValue = 0, maxValue = 10, value = 5)

#Eye Count Input
base.text("Eye Count", l = "Eye Count")
eyeCount = base.intField(minValue = 0, maxValue = 4, value = 2)

#Cheek Count Input - saved for later
# base.text("Cheek Count", l = "Cheek Count per side")
# cheekCount = base.intField(minValue = 0, maxValue = 4, value = 0)

#Lip Count Input
base.text("Lip Count", l = "Lip Count per side")
lipCount = base.intField(minValue = 0, maxValue = 10, value = 2)

# #Ear Count Input - saved for later
# base.text("Ear Count", l = "Ear Count per side")
# earCount = base.intField(minValue = 0, maxValue = 4, value = 0)

#Tongue Count Input - saved for later
# base.text("Tongue Count", l = "Tongue Count")
# tongueCount = base.intField(minValue = 0, maxValue = 4, value = 0)

#Other buttons
base.button(l = 'Create Joints', w = 200, c = "createJoints()")
base.button(l = 'Create Leg IK handles', w = 200, c = "createIKHandlesLeg()")
base.button(l = 'Mirror L ->R', w = 200, c = "mirrorLtoR()")
base.button(l = 'Create Arm IK handles', w = 200, c = "createIKHandlesArm()")
base.button(l = 'Orient Joints', w = 200, c = "orientJoints()")
base.button(l = "Handles", w = 200, c = "createHandles()")

base.showWindow()

########################Functions##########

# Makes all the joints
def createJoints():
    spineHeight = (base.intField(spineCount, query = True, value = True) * 5)
    neckHeight = (base.intField(neckCount, query = True, value = True) * 3)
    createRoot()
    createSpine()
    createNeck(spineHeight)
    createHead(spineHeight, neckHeight)
    createArmL(spineHeight)
    createHandL(spineHeight)
    createLegL()
    createEyes(spineHeight, neckHeight)
    createLipsL(spineHeight, neckHeight)

#Creates all of the handles
def createHandles():
    createRootHandle()
    createSpineNeckHandle()

#Not used - saved for reference
def createLocators():
    if base.objExists('Loc_Master'):
        print('Loc_Master already exists')
    else:
        base.group(em = True, name = "Loc_Master")
        print("true")
    root = base.spaceLocator(name = 'Loc_ROOT')
    #base.scale(1, 1, 1, root)
    base.move(0, 10, 0, root)
    base.parent(root, "Loc_Master")
    createSpine()
    
#Creates the base or root of the skeleton
def createRoot():
    base.joint(p = (0, 10, 0), n = "root_JNT")

#Creates the spine bones
def createSpine():
    for i in range(0, base.intField(spineCount, query = True, value = True)):
        base.joint(n = "spine" + str(i) + "_JNT", p = (0, 15 + 5 * i, 0))

#Creates the neck bones    
def createNeck(spineHeight):
    for i in range(0, base.intField(neckCount, query = True, value = True)):
        base.joint(n = "neck" + str(i) + "_JNT", p = (0, 13 + spineHeight + 3 * i, 0))
            
#Creates the head bones
def createHead(spineHeight, neckHeight):
    base.joint(n = "head_JNT", p = (0, 13 + spineHeight + neckHeight, 0))
    base.joint(n = "head_NULL", p = (0, 16 + spineHeight + neckHeight, 0))

#Creates the left arm bones. Needs to be mirrored for the right
def createArmL(height):
    spine = base.intField(spineCount, query = True, value = True)
    clavicle = base.joint(n = "clavicle_L_JNT", p = (1, 11 + height, 1))
    base.parent(clavicle, "spine" + str(spine - 1) + "_JNT")
    base.joint(n = "shoulder_L_JNT", p = (5, 11 + height, 0))
    base.joint(n = "elbow_L_JNT", p = (10, 11 + height, -1))
    base.joint(n = "wrist_L_JNT", p = (15, 11 + height, 0))

#Creates the left hand bones. Needs to be mirrored for the right
def createHandL(spineHeight):
    for i in range(0, base.intField(fingerCount, query = True, value = True)):
        for j in range(0, 3):
            finger = base.joint(n = "finger" + str(i) + "_knuckle" + str(j) + "_L_JNT", p = (17 + j, 11 + spineHeight, 1 - i))
        base.joint(n = "finger" + str(i) + "_L_NULL", p = (17 + j + 1, 11 + spineHeight, 1 - i))
        if i > 0:
            base.parent("finger"+ str(i) + "_knuckle0_L_JNT", "wrist_L_JNT")

#Creates the left leg bones. Needs to be mirrored for the right
def createLegL():
    hipL = base.joint(p = (2, 10, 0), n = "hip_L_JNT")
    base.parent(hipL, "root_JNT")
    base.joint(p = (2, 5, 1), n = "knee_L_JNT")
    base.joint(p = (2, 1, 0), n = "ankle_L_JNT")
    base.joint(p = (2, 0, 1), n = "toePad_L_JNT")
    base.joint(p = (2, 0, 2), n = "toe_L_NULL")

#Creates the eyes. First two will appear in roughly the correct locations
def createEyes(spineHeight, neckHeight):
    for i in range(0, base.intField(eyeCount, query = True, value = True)):
        eyeball = base.joint(n = "eye" + str(i) + "_JNT", p = (1 - (2 * i), 15 + spineHeight + neckHeight, 1))
        base.parent(eyeball, "head_JNT")

#Creates the jaw, the upper lips and lower lips
def createLipsL(spineHeight, neckHeight):
    upperMouth = base.joint(n = "upperMouth_C_JNT", p = (0, 14 + spineHeight + neckHeight, 1))
    base.parent(upperMouth, "head_JNT")
    base.joint(n = "upperlip_C_JNT", p = (0, 14 + spineHeight + neckHeight, 2))
    for i in range(0, base.intField(lipCount, query = True, value = True)):
        upperlip = base.joint(n = "upperLip" + str(i) + "_L_JNT", p = (.5 + (.5 * i), 14 + spineHeight + neckHeight, 2))
        base.parent(upperlip, "upperMouth_C_JNT")
    jaw = base.joint(n = "jaw_C_JNT", p = (0, 12 + spineHeight + neckHeight, 1))
    base.parent(jaw, "head_JNT")
    base.joint(n = "lowerlip_C_JNT", p = (0, 13 + spineHeight + neckHeight, 2))
    for i in range(0, base.intField(lipCount, query = True, value = True)):
        lowerlip = base.joint(n = "lowerLip" + str(i) + "_L_JNT", p = (.5 + (.5 * i), 13 + spineHeight + neckHeight, 2))
        base.parent(lowerlip, "jaw_C_JNT")
    
#Mirrors joints on the left side    
def mirrorLtoR():
    base.mirrorJoint('clavicle_L_JNT', sr = ('L_', 'R_'))
    base.mirrorJoint('hip_L_JNT', sr = ('L_', 'R_'))
    lips = []
    for i in range(0, base.intField(lipCount, query = True, value = True)):
        lipUStr = ("upperLip" + str(i) + "_L_JNT")
        lipLStr = ("lowerLip" + str(i) + "_L_JNT")
        lips.append(lipUStr)
        lips.append(lipLStr)
    for lip in lips:
        base.mirrorJoint(lip, sr = ('L_', 'R_' ))

#Orients the joints
def orientJoints():
    base.select("root_JNT")
    base.joint(e = True, ch = True, oj = 'xyz')

#Creates an IK handle on the left leg
def createIKHandlesLeg():
    spine = base.intField(spineCount, query = True, value = True)
    base.ikHandle(n = "IK_L_Leg", sj = "hip_L_JNT", ee = "ankle_L_JNT")
    
# Creates the IK handles on the arms    
def createIKHandlesArm():
    base.ikHandle(n = "IK_L_Arm", sj = "shoulder_L_JNT", ee = "wrist_L_JNT")
    base.ikHandle(n = "IK_R_Arm", sj = "shoulder_R_JNT", ee = "wrist_R_JNT")
       
#Not used
def deleteLocators():
    nodes = base.ls("Loc_*")
    base.delete(nodes)

#Creates the base root handle
def createRootHandle():
    arrow = base.curve(n = "root_handle", degree = 1, p = [(1,0,2), (2, 0, 1), (3, 0, 1), (3,0,2), (5,0,0), (3,0,-2), (3, 0, -1), (2, 0, -1), \
    (1, 0, -2), (1, 0, -3), (2, 0, -3), (0, 0, -5), (-2, 0, -3), (-1, 0, -3), (-1, 0, -2), (-2, 0, -1), (-3, 0, -1), (-3, 0, -2), \
    (-5, 0, 0), (-3, 0, 2), (-3, 0, 1), (-2, 0, 1), (-1, 0, 2), (-1, 0, 3), (-2, 0, 3), (0, 0, 5), (2, 0, 3), (1, 0, 3), (1,0,2)])
    base.parent("root_JNT", arrow)

def createSpineNeckHandle():
    nurbsCircle = base.circle(c = (0,0,0), r = 1, nr = (1,0,0))
    spine = base.intField(spineCount, query = True, value = True)
    for i in range(0, base.intField(spineCount, query = True, value = True)):
        shaped = base.instance(nurbsCircle, lf = False)
        position = base.xform(base.ls("spine" + str(i) + "_JNT"), query = True, t = True, ws = True)
        base.move(position[0], position[1], position[2], shaped)
        base.parent("spine" + str(i) + "_JNT",shaped)
        if i == 0:
            base.parent(shaped, "root_JNT")
        else:
            base.parent(shaped, "spine" + str(i - 1) + "_JNT")
    for i in range(0, base.intField(neckCount, query = True, value = True)):
        shaped = base.instance(nurbsCircle, lf = False)
        position = base.xform(base.ls("neck" + str(i) + "_JNT"), query = True, t = True, ws = True)
        base.move(position[0], position[1], position[2], shaped)
        base.parent("neck" + str(i) + "_JNT",shaped)
        if i == 0:
            base.parent(shaped, "spine" + str(spine - 1) + "_JNT")
        else:
            base.parent(shaped, "neck" + str(i - 1) + "_JNT")
    base.delete(nurbsCircle)


# #In progress Nurbs parenting
# shaped = base.instance("nurbsCircleShape1", lf = False)

# position = base.xform(base.ls("joint1"), query = True, t = True, ws = True)
# #shape2 = base.listRelatives(shaped, s = True)
# base.move(position[0], position[1], position[2], shaped)
# base.parent('joint1',shaped)