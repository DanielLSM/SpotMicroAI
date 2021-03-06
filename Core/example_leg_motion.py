"""
Simulation of SpotMicroAI and it's Kinematics 
Use a Gamepad to see how it works
In this example the Bot has a fixed base
"""
import pybullet as p
import numpy as np
import pybullet_data
import time
import math
import datetime as dt
import matplotlib.animation as animation
import random
from inputs import devices, get_gamepad
from thinputs import ThreadedInputs
import spotmicroai
from kinematicMotion import KinematicMotion
import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation


robot=spotmicroai.Robot(False,False)
speed1=240
speed2=170
speed3=300
spurWidth=robot.W/2+20
stepLength=0
stepHeight=72
iXf=120
iXb=-132
IDspurWidth = p.addUserDebugParameter("spur width", 0, robot.W, spurWidth)
IDstepLength = p.addUserDebugParameter("step length", -70, 115, stepLength)
IDstepHeight = p.addUserDebugParameter("step height", 0, 150, stepHeight)
IDspeed1 = p.addUserDebugParameter("speed 1", 100, 1000, speed1)
IDspeed2 = p.addUserDebugParameter("speed 2", 100, 1000, speed2)
IDspeed3 = p.addUserDebugParameter("speed 3", 100, 1000, speed3)
IDixf = p.addUserDebugParameter("iXf", 0, 400, iXf)
IDixb = p.addUserDebugParameter("iXb", -200, 200, iXb)

walk=False

# Gamepad Initialisation
# Dictionary of game controller buttons we want to include.
gamepadInputs = {'ABS_X': 128, 'ABS_RZ': 127, 'ABS_Y': 126, 'ABS_Z': 125,
                 'BTN_TIGGER': 124, 'BTN_THUMB': 123, 'BTN_THUMB2': 122, 'BTN_TOP': 121, # right side of gamepad
                 'ABS_HAT0X': 120, 'ABS_HAT0Y': 119, # left
                 'BTN_TOP2': 118, 'BTN_BASE': 117, # left top
                 'BTN_PINKIE': 116, 'BTN_BASE2': 115 # right top
                 }

def resetPose():
    # TODO: globals are bad
    global joy_x, joy_z, joy_y, joy_rz,joy_z
    joy_x, joy_y, joy_z, joy_rz = 128, 128, 128, 128

def func(p,LLp):
#    LLp[1]+=stepHeight*math.sin(math.pi*math.sin(math.pi/2*p))
    LLp[1]+=stepHeight*math.sin(math.pi*p)
    return LLp

def func3(p,LLp):
    LLp[0]+=0*math.sin(math.pi*p)
    return LLp

def func2(p,LLp):
    LLp[0]-=0*math.sin(math.pi*p)
    return LLp

def action():
    return motion.moveLegTo(0,Lpa[0],speed2,func=func) and motion.moveLegTo(3,Lpa[3],speed2,func=func) \
            and motion.moveLegTo(1,Lpf[1],speed1,func=func3) \
            and motion.moveLegTo(2,Lpf[2],speed1,func=func2)
    

def action2():
    motion.moveLegsTo(Lp,400)

def action3():
    return \
    motion.moveLegTo(0,Lpf[0],speed1,func=func3) and \
    motion.moveLegTo(3,Lpf[3],speed1,func=func2) and \
    motion.moveLegTo(1,Lpa[1],speed2,func=func) and \
    motion.moveLegTo(2,Lpa[2],speed2,func=func)

def handleGamepad():
    # TODO: globals are bad
    global joy_x, joy_z, joy_y, joy_rz,walk
    commandInput, commandValue = gamepad.read()
    # Gamepad button command filter
    if commandInput == 'ABS_X':
        joy_x = commandValue
    if commandInput == 'ABS_Y':
        joy_y = commandValue
    if commandInput == 'ABS_Z':
        joy_z = commandValue
    if commandInput == 'ABS_RZ':
        joy_rz = commandValue
    if commandInput == 'BTN_TOP2':
        resetPose()
    if commandInput == 'BTN_PINKIE':
        if commandValue:
            walk=not walk
    if commandInput == 'BTN_BASE':
        action2()
    if commandInput == 'BTN_BASE2':
        action3()



IDheight = p.addUserDebugParameter("height", -40, 90, 40)

Lp = np.array([[iXf, -100,spurWidth, 1], [iXf, -100, -spurWidth, 1],
[-50, -100, spurWidth, 1], [-50, -100, -spurWidth, 1]])

motion=KinematicMotion(Lp)
resetPose()

# Initialise the gamepad object using the gamepad inputs Python package
gamepad = ThreadedInputs()
for gamepadInput in gamepadInputs:
    gamepad.append_command(gamepadInput, gamepadInputs[gamepadInput])
gamepad.start()

rtime=time.time()
s=False
while True:
    """
    # Read temperature (Celsius) from TMP102
    temp_c = round(random.randint(9,10), 2)

    # Add x and y to lists
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    #ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]
    x, y = rw.__next__()
    # Draw x and y lists
    ax.clear()
    ax.plot(x, y)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('SpotMicroAI Telemetry')
    plt.ylabel('IMU Pitch')

    # update the xy data
 #   x, y = rw.__next__()
    points.set_data(x, y)

    if doblit:
        # restore background
        fig.canvas.restore_region(background)

        # redraw just the points
        ax.draw_artist(points)
        #ax.draw_list(points)
        
        # fill in the axes rectangle
        fig.canvas.blit(ax.bbox)

    else:
        # redraw everything
        fig.canvas.draw()
    """
    stepHeight = p.readUserDebugParameter(IDstepHeight)
    spurWidth = p.readUserDebugParameter(IDspurWidth)
    #stepLength = p.readUserDebugParameter(IDstepLength)
    speed1=p.readUserDebugParameter(IDspeed1)
    speed2=p.readUserDebugParameter(IDspeed2)
    speed3=p.readUserDebugParameter(IDspeed3)
    iXf=p.readUserDebugParameter(IDixf)
    iXb=p.readUserDebugParameter(IDixb)

    stepLength=-(joy_rz-128)*1.5
    if(stepLength<0):
        stepLength=stepLength/3
    else:
        stepLength=stepLength/2
    if stepLength==0:
        stepHeight=0


    bodyPos=robot.getPos()
    bodyOrn,_,_=robot.getIMU()
    xr,yr,_= p.getEulerFromQuaternion(bodyOrn)
    distance=math.sqrt(bodyPos[0]**2+bodyPos[1]**2)
    if distance>5:
        robot.resetBody()

    Lpa = np.array([[iXf+stepLength, -100,spurWidth, 1], [iXf+stepLength, -100, -spurWidth, 1],
    [iXb+stepLength, -100, spurWidth, 1], [iXb+stepLength, -100, -spurWidth, 1]])

    Lpf = np.array([[iXf-stepLength, -100, spurWidth, 1], [iXf-stepLength, -100, -spurWidth, 1],
    [iXb-stepLength, -100, spurWidth, 1], [iXb-stepLength, -100, -spurWidth, 1]])
    q = p.getQuaternionFromEuler((0,0,math.pi/180*1))
    orn=p.getMatrixFromQuaternion(q)

    psi=0
    omega=0
    phi=-math.pi/180*-(joy_z-128)/10
    Rx = np.array([[1,0,0,0],
                [0,np.cos(omega),-np.sin(omega),0],
                [0,np.sin(omega),np.cos(omega),0],[0,0,0,1]])
    Ry = np.array([[np.cos(phi),0,np.sin(phi),0],
                [0,1,0,0],
                [-np.sin(phi),0,np.cos(phi),0],[0,0,0,1]])
    Rz = np.array([[np.cos(psi),-np.sin(psi),0,0],
                [np.sin(psi),np.cos(psi),0,0],[0,0,1,0],[0,0,0,1]])
    Rxyz = Rx.dot(Ry.dot(Rz))
    Lpa=[Rxyz.dot(x) for x in Lpa]

    phi=math.pi/180*-(joy_z-128)/10
    Rx = np.array([[1,0,0,0],
                [0,np.cos(omega),-np.sin(omega),0],
                [0,np.sin(omega),np.cos(omega),0],[0,0,0,1]])
    Ry = np.array([[np.cos(phi),0,np.sin(phi),0],
                [0,1,0,0],
                [-np.sin(phi),0,np.cos(phi),0],[0,0,0,1]])
    Rz = np.array([[np.cos(psi),-np.sin(psi),0,0],
                [np.sin(psi),np.cos(psi),0,0],[0,0,1,0],[0,0,0,1]])
    Rxyz = Rx.dot(Ry.dot(Rz))
    Lpf=[Rxyz.dot(x) for x in Lpf]

    handleGamepad()
    d=time.time()-rtime
    if d>speed3/1000 and walk:
        if(s):
            if action3():
                s=False
        else:
            if action():
                s=True
        rtime=time.time()


    height = p.readUserDebugParameter(IDheight)

    # map the Gamepad Inputs to Pose-Values. Still very hardcoded ranges. 
    # TODO: Make ranges depend on height or smth to keep them valid all the time
    robot.feetPosition(motion.step())
    roll=-xr-math.pi/180*((joy_x)-128)/3
    #roll=0
    robot.bodyRotation((roll,math.pi/180*((joy_z-128)/20),-(1/256*joy_y-0.5)))
    bodyX=50+yr*10
    robot.bodyPosition((bodyX, 40+height, 10*xr-(joy_z-128)*0.3))
    robot.step()
gamepad.stop()
