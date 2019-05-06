# -*- coding: utf-8 -*-
import sys
import os
import platform
import time
import ctypes
import matplotlib.animation as animation
import emotionMetrics as em
import bandPower as bp
import vistaEmotiv as ve
from array import *
from ctypes import *
from __builtin__ import exit

if sys.platform.startswith('win32'):
    import msvcrt
elif sys.platform.startswith('linux'):
    import atexit
    from select import select

from ctypes import *

try:
    if sys.platform.startswith('win32'):
        libEDK = cdll.LoadLibrary("../../bin/win64/edk.dll")
    elif sys.platform.startswith('linux'):
        srcDir = os.getcwd()
	if platform.machine().startswith('arm'):
            libPath = srcDir + "/../../bin/armhf/libedk.so"
	else:
            libPath = srcDir + "/../../bin/linux64/libedk.so"
        libEDK = CDLL(libPath)
    else:
        raise Exception('System not supported.')
except Exception as e:
    print 'Error: cannot load EDK lib:', e
    exit()


global arrayFinalPerformance
global arrayFinalPowerBand
global tipoEstudio
global arrayData
global v
global animationBandpower
global animationPerformance
global contadorPowerBand
global fig
global fig1
global ax1
global ax2
global line
global root
global size
global bg_label
global w
global h
global scalesArray
global userID
global user
global eState
global alphaValue
global low_betaValue
global high_betaValue
global gammaValue
global thetaValue
global alpha
global low_beta
global high_beta
global gamma
global theta


IEE_EmoEngineEventCreate = libEDK.IEE_EmoEngineEventCreate
IEE_EmoEngineEventCreate.restype = c_void_p
eEvent = IEE_EmoEngineEventCreate()


IEE_EmoStateCreate = libEDK.IEE_EmoStateCreate
IEE_EmoStateCreate.restype = c_void_p
eState = IEE_EmoStateCreate()


IEE_EmoEngineEventGetEmoState = libEDK.IEE_EmoEngineEventGetEmoState
IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
IEE_EmoEngineEventGetEmoState.restype = c_int



IS_GetWirelessSignalStatus = libEDK.IS_GetWirelessSignalStatus
IS_GetWirelessSignalStatus.restype = c_int
IS_GetWirelessSignalStatus.argtypes = [c_void_p]

userID = c_uint(0)
user   = pointer(userID)
ready  = 0
state  = c_int(0)

batteryLevel     = c_long(0)
batteryLevelP    = pointer(batteryLevel)
maxBatteryLevel  = c_int(0)
maxBatteryLevelP = pointer(maxBatteryLevel)


alphaValue     = c_double(0)
low_betaValue  = c_double(0)
high_betaValue = c_double(0)
gammaValue     = c_double(0)
thetaValue     = c_double(0)

alpha     = pointer(alphaValue)
low_beta  = pointer(low_betaValue)
high_beta = pointer(high_betaValue)
gamma     = pointer(gammaValue)
theta     = pointer(thetaValue)

arrayFinalPerformance = []
arrayFinalPowerBand = []
tipoEstudio = ""
arrayData=[[], [], [], [], [], []]
channelList = array('I',[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])   # IED_AF3, IED_AF4, IED_T7, IED_T8, IED_Pz

# ------Extra----------------------------------------------------------------
RawScore = c_double(0)
MinScale = c_double(0)
MaxScale = c_double(0)

Raw = pointer(RawScore)
Min = pointer(MinScale)
Max = pointer(MaxScale)

PM_EXCITEMENT = 0x0001,
PM_RELAXATION = 0x0002,
PM_STRESS     = 0x0004,
PM_ENGAGEMENT = 0x0008,

PM_INTEREST   = 0x0010,
PM_FOCUS      = 0x0020


# -------------------------------------------------------------------------
print "==================================================================="
print "EMOTIVPRE"
print "==================================================================="

# -------------------------------------------------------------------------
if libEDK.IEE_EngineConnect("Emotiv Systems-5") != 0:
        print "Emotiv Engine start up failed."
        exit();

line, fig, fig1, ax1, ax2 = ve.generarGraficos()
root, size = ve.definirRaiz()
bg_label, width, height= ve.definirFondo(root, size)
root.geometry("%dx%d+50+30" % (width, height))
scalesArray = ve.zonaAnalisis(bg_label, fig, fig1)
ve.zonaDatos(bg_label)
ve.zonaBotones(bg_label, root, ax1)
barcollection = bp.generarBarcollection(ax2)
animationPerformance = animation.FuncAnimation(fig, em.run, em.data_gen(user,userID,eEvent,eState,arrayFinalPerformance), fargs=(scalesArray,line,arrayData,ax1),blit=True, interval=50, repeat=False)
animationBandpower=animation.FuncAnimation(fig1, bp.animate ,bp.data_gen3(user, userID, eEvent, eState, channelList, theta, alpha, low_beta, high_beta, gamma, thetaValue, alphaValue, low_betaValue, high_betaValue, gammaValue,arrayFinalPowerBand),fargs=(barcollection,True),repeat=False,blit=False,interval=50)
root.mainloop()
# -------------------------------------------------------------------------
libEDK.IEE_EngineDisconnect()
libEDK.IEE_EmoStateFree(eState)
libEDK.IEE_EmoEngineEventFree(eEvent)
