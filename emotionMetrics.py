# -*- coding: utf-8 -*-
import sys
import os
import platform
import time
import ctypes
import numpy as np
import pandas as pd
import random
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

global consolidarPerformance
global guardarPerformance
global identificador

consolidarPerformance = False
guardarPerformance = False
identificador = ""

# long term excitement
IS_PerformanceMetricGetExcitementLongTermScore = libEDK.IS_PerformanceMetricGetExcitementLongTermScore
IS_PerformanceMetricGetExcitementLongTermScore.restype = c_float
IS_PerformanceMetricGetExcitementLongTermScore.argtypes = [c_void_p]

# short term excitement
IS_PerformanceMetricGetInstantaneousExcitementScore = libEDK.IS_PerformanceMetricGetInstantaneousExcitementScore
IS_PerformanceMetricGetInstantaneousExcitementScore.restype = c_float
IS_PerformanceMetricGetInstantaneousExcitementScore.argtypes = [c_void_p]

# relaxation
IS_PerformanceMetricGetRelaxationScore = libEDK.IS_PerformanceMetricGetRelaxationScore
IS_PerformanceMetricGetRelaxationScore.restype = c_float
IS_PerformanceMetricGetRelaxationScore.argtypes = [c_void_p]

# stress
IS_PerformanceMetricGetStressScore = libEDK.IS_PerformanceMetricGetStressScore
IS_PerformanceMetricGetStressScore.restype = c_float
IS_PerformanceMetricGetStressScore.argtypes = [c_void_p]

# boredom/engagement
IS_PerformanceMetricGetEngagementBoredomScore = libEDK.IS_PerformanceMetricGetEngagementBoredomScore
IS_PerformanceMetricGetEngagementBoredomScore.restype = c_float
IS_PerformanceMetricGetEngagementBoredomScore.argtypes = [c_void_p]

# interest
IS_PerformanceMetricGetInterestScore = libEDK.IS_PerformanceMetricGetInterestScore
IS_PerformanceMetricGetInterestScore.restype = c_float
IS_PerformanceMetricGetInterestScore.argtypes = [c_void_p]

# focus
IS_PerformanceMetricGetFocusScore = libEDK.IS_PerformanceMetricGetFocusScore
IS_PerformanceMetricGetFocusScore.restype = c_float
IS_PerformanceMetricGetFocusScore.argtypes = [c_void_p]


def changeStateConsolidadoPerformance():
    global consolidarPerformance
    if consolidarPerformance == False:
        consolidarPerformance = True
    else:
        consolidarPerformance = False


def changeStateGuardarPerformance():
    global guardarPerformance
    global consolidarPerformance
    if guardarPerformance == False:
        guardarPerformance = True
    else:
        guardarPerformance = False

def obtenerValorPerformance(identificadorLocal):
    global identificador
    identificador = identificadorLocal

def logPerformanceMetrics(userID, eState):
    random.seed()
    rand_stress = random.uniform(0.99,1.01)
    stress = IS_PerformanceMetricGetStressScore(eState)*rand_stress
    if (stress >= 1):
        stress = IS_PerformanceMetricGetStressScore(eState)

    rand_relax = random.uniform(0.99,1.01)
    relax = IS_PerformanceMetricGetRelaxationScore(eState)*rand_relax
    if (relax >= 1):
        relax = IS_PerformanceMetricGetRelaxationScore(eState)

    rand_engag = random.uniform(0.99,1.01)
    engag = IS_PerformanceMetricGetEngagementBoredomScore(eState)*rand_engag
    if (engag >= 1):
        engag = IS_PerformanceMetricGetEngagementBoredomScore(eState)

    rand_interes = random.uniform(0.99,1.01)
    interes = IS_PerformanceMetricGetInterestScore(eState)*rand_interes
    if (interes >= 1):
        interes = IS_PerformanceMetricGetInterestScore(eState)

    rand_focus = random.uniform(0.99,1.01)
    focus = IS_PerformanceMetricGetFocusScore(eState)*rand_focus
    if (focus >= 1):
        focus = IS_PerformanceMetricGetFocusScore(eState)

    return stress, relax, engag, interes ,focus

def data_gen(user,userID,eEvent,eState,arrayFinalPerformance):
    global IEE_EmoEngineEventCreate
    global IEE_EmoEngineEventGetEmoState
    global IEE_EmoStateCreate
    global ready
    global state
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
    global consolidarPerformance
    global guardarPerformance
    global stress
    global focus
    global engag
    global interes
    global relax
    global contrador
    global headerPerformance

    contador=0
    headerPerformanceP =['tiempo','stress', 'focus', 'interes', 'realx', 'engag']
    stress = 0.0
    focus = 0.0
    engag = 0.0
    interes = 0.0
    relax =0.0
    t = 0
    cnt = 0
    while True:
        cnt+=1
        t += 0.05
        state = libEDK.IEE_EngineGetNextEvent(eEvent)
        if state == 0:
            eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
            libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
            if eventType == 16:  # libEDK.IEE_Event_enum.IEE_UserAdded
                ready = 1
                libEDK.IEE_FFTSetWindowingType(userID, 1);  # 1: libEDK.IEE_WindowingTypes_enum.IEE_HAMMING
                print "User added"
            if eventType == 64:  # libEDK.IEE_Event_enum.IEE_EmoStateUpdated
                libEDK.IEE_EmoEngineEventGetEmoState(eEvent, eState)
                stress, relax, engag, interes, focus = logPerformanceMetrics(userID, eState)
        elif state != 0x0600:
            print "Internal error in Emotiv Engine ! "
        time.sleep(0.1)
        if (consolidarPerformance):
            arregloTempP = [t, stress, focus, interes, relax, engag]
            arrayFinalPerformance.append(arregloTempP)
        if (guardarPerformance):
            dataFramePerformance = pd.DataFrame(arrayFinalPerformance)
            dataFramePerformance.to_csv('D:/Users/Andres/Documents/Vera/community-sdk-master/examples_basic/Python/datos/perfomance_'+str(identificador)+'.csv',header=headerPerformanceP)
            guardarPerformance = False
            consolidarPerformance = False
            arrayFinalPerformance = []
            ve.mensajeGrabado()
        yield t, stress, focus, interes, relax, engag

def run(data,arrayScale,arrayLine,arrayData,ax1):
    t, y1, y2, y3, y4, y5 = data
    arrayScale[0].set(y2)
    arrayScale[1].set(y3)
    arrayScale[2].set(y4)
    arrayScale[3].set(y1)
    arrayScale[4].set(y5)
    arrayData[0].append(t)
    arrayData[1].append(y1)
    arrayData[2].append(y2)
    arrayData[3].append(y3)
    arrayData[4].append(y4)
    arrayData[5].append(y5)
    if len(arrayData[0])>100:
        arrayData[0].pop(0)#xdata
        arrayData[1].pop(0)
        arrayData[2].pop(0)
        arrayData[3].pop(0)
        arrayData[4].pop(0)
        arrayData[5].pop(0)
    xmin, xmax = ax1.get_xlim()
    if t >= xmax:
        ax1.set_xlim(xmin+0.3, xmax+0.3)
        ax1.figure.canvas.draw()
    ymin, ymax = ax1.get_ylim()
    arrayLine[0].set_data(arrayData[0], arrayData[1])
    arrayLine[1].set_data(arrayData[0], arrayData[2])
    arrayLine[2].set_data(arrayData[0], arrayData[3])
    arrayLine[3].set_data(arrayData[0], arrayData[4])
    arrayLine[4].set_data(arrayData[0], arrayData[5])
    return arrayLine
