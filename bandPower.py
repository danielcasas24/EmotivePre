# -*- coding: utf-8 -*-
import sys
import os
import platform
import time
import ctypes
import numpy as np
import pandas as pd
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

global consolidarPowerBand
global guardarPowerBand
global identificador

consolidarPowerBand = False
guardarPowerBand = False
identificador = ""

def changeStateConsolidadoPowerband():
    global consolidarPowerBand
    if consolidarPowerBand == False:
        consolidarPowerBand = True
    else:
        consolidarPowerBand = False


def changeStateGuardarPowerband():
    global guardarPowerBand
    global consolidarPowerBand
    if guardarPowerBand == False:
        guardarPowerBand = True
    else:
        guardarPowerBand = False

def obtenerValorPowerband(identificadorLocal):
    global identificador
    identificador = identificadorLocal

def data_gen3(user,userID,eEvent,eState,channelList, theta, alpha, low_beta, high_beta, gamma, thetaValue, alphaValue, low_betaValue, high_betaValue, gammaValue, arrayFinalPowerBand):
    global IEE_EmoEngineEventCreate
    global IEE_EmoEngineEventGetEmoState
    global IEE_EmoStateCreate
    global ready
    global state
    global headerPerformance
    global promedio_theta
    global promedio_alpha
    global promedio_gamma
    global promedio_low_beta
    global promedio_high_beta
    global consolidarPowerBand
    global guardarPowerBand

    headerPerformance = ['theta', 'alpha', 'low beta', 'high beta', 'gamma']
    promedio_theta = 0
    promedio_alpha = 0
    promedio_gamma = 0
    promedio_low_beta = 0
    promedio_high_beta = 0
    contadorPowerBand=0
    t = 0
    cnt = 0

    while True:
        cnt+=1
        t += 0.05
        state = libEDK.IEE_EngineGetNextEvent(eEvent)
        if state == 0:
            eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
            libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
            ready = 1
            if ready == 1:
                promedio_theta = 0
                promedio_alpha = 0
                promedio_gamma = 0
                promedio_low_beta = 0
                promedio_high_beta = 0
                for i in channelList:
                    result = c_int(0)
                    result = libEDK.IEE_GetAverageBandPowers(userID, i, theta, alpha, low_beta, high_beta, gamma)
                    if result == 0:
                        promedio_theta += thetaValue.value
                        promedio_alpha += alphaValue.value
                        promedio_gamma += gammaValue.value
                        promedio_low_beta += low_betaValue.value
                        promedio_high_beta += high_betaValue.value

                promedio_theta = psdToDb(promedio_theta/len(channelList))
                promedio_alpha = psdToDb(promedio_alpha/len(channelList))
                promedio_gamma = psdToDb(promedio_gamma/len(channelList))
                promedio_low_beta = psdToDb(promedio_low_beta/len(channelList))
                promedio_high_beta = psdToDb(promedio_high_beta/len(channelList))
        elif state != 0x0600:
            print "Internal error in Emotiv Engine ! "
        time.sleep(0.1)
        if (consolidarPowerBand):
            arregloTemp = [promedio_theta, promedio_alpha, promedio_low_beta, promedio_high_beta, promedio_gamma]
            arrayFinalPowerBand.append(arregloTemp)
        if (guardarPowerBand):
            dataFramePowerBand = pd.DataFrame(arrayFinalPowerBand)
            dataFramePowerBand.to_csv('D:/Users/Andres/Documents/Vera/community-sdk-master/examples_basic/Python/datos/powerband_'+str(identificador)+'.csv',header=headerPerformance)
            guardarPowerBand = False
            consolidarPowerBand = False
            arrayFinalPowerBand = []
        yield promedio_theta, promedio_alpha, promedio_low_beta, promedio_high_beta, promedio_gamma

def data_gen2(n):
    return 10,10,10,10,10

def generarBarcollection(ax2):
    x=range(1,6)
    barcollection = ax2.bar(x,data_gen2(1), tick_label=['Theta\n(4-8 Hz)','Alpha\n(8-12 Hz)','Low Beta\n(12-16 Hz)','High Beta\n(16-25 Hz)','Gamma\n(25-45 Hz)'],
                            color=['#ff3333','#ff4d4d','#ff6666','#ff8080','#ff9999'], zorder=3, width=0.6)
    return barcollection

def animate(data, barcollection, conditional):
    v = conditional
    y = data
    for i, b in enumerate(barcollection):
        b.set_height(y[i])

def psdToDb(voltage):
    if (voltage == 0):
        valueDB = 1
    else:
        valueDB=10*np.log10(voltage)
    if (valueDB < 0):
        valueDB = -(valueDB)
    return valueDB
