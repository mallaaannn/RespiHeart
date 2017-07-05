# Code written by Malin Thunholm and Peter Thunholm for a project during Spring 2017
# regarding RespiHeart a new product under developement at Region Östergötland, Sweden.

#!/usr/bin/env python
from __future__ import division
from scipy.signal import savgol_filter
from operator import truediv
from scipy.signal import butter, lfilter
from scipy.signal import freqs
from threading import Thread
import math
import io
import array
import os
import Image
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import matplotlib.pyplot as plt
import binascii
import bluetooth
from time import sleep
import time
import sys
import binascii
import struct
from socket import * 
import rhPython
import logging
import numpy as np

plt.ion()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bd_addr="00:0B:CE:0C:0A:8D"
#bd_addr = "B8:27:EB:E2:06:E3"

#global readingdata
readingdata = False

respi=rhPython.RHclass()
bytefile=open("bytefile.bin","wb")
valuebytefile=open("valuebytefile.bin","wb")
intfile = open('valueintfile.txt', 'wb')
reply = ''

respi.sockconnect(bd_addr,1)

#TILLAGT 
logger.info('Trying to get right ack')
sleep(5)

correct_answer = False

#while not correct_answer:
 #   sleep(1)
  #  logger.info('Trying again')
   # reply=respi.cmdack()
#    logger.debug(reply)
 #   respi.sendsome_bytes(reply)
  #  replystart=respi.getData()
   # logger.debug('new ack ' + replystart)
#    if replystart[-4:] == '0101':
 #       correct_answer = True
  #      logger.debug('Correct ack' + replystart)


sleep(1)
#setup settings respi
logger.info('setting to respi ')
reply = respi.cmdsettings()
logger.debug(reply)
respi.sendsome_bytes(reply)
replystart=respi.getData()
logger.debug('reply settings ' + replystart)
sleep(0.1)
replystart1=respi.getData()
logger.debug('reply settings ' + replystart1)

sleep(1)
#ack reply
#logger.debug('ack ') 
#reply1=respi.cmdack()
#respi.sendsome_bytes(reply1)
#replystart=respi.getData()
#logger.debug('reply ack %s ' % replystart)

sleep(1)
#setup sensor respi
logger.info('sensor setup ')
reply = respi.cmdsensor()
logger.debug(reply)
respi.sendsome_bytes(reply)
replystart=respi.getData()
logger.debug('reply sensor ' + replystart)
sleep(0.1)
replystart1=respi.getData()
logger.debug('reply sensor ' + replystart1)
sleep(1)

#ack reply
#logger.debug('ack ') 
#reply1=respi.cmdack()
#respi.sendsome_bytes(reply1)
#replystart=respi.getData()
#logger.debug('reply ack %s ' % replystart)

sleep(1)
#setup sensor1 respi
logger.info('sensor setup1 ')
reply = respi.cmdsensor1()
logger.debug(reply)
respi.sendsome_bytes(reply)
replystart=respi.getData()
logger.debug('reply sensor1 ' + replystart)
replystart1=respi.getData()
logger.debug('reply sensor1 ' + replystart1)
sleep(1)

#ack reply
#logger.debug('ack ') 
#reply1=respi.cmdack()
#respi.sendsome_bytes(reply1)
#replystart=respi.getData()
#logger.debug('reply ack %s ' % replystart)

sleep(1)
#startcommand
logger.info('startcommand ')
reply = respi.cmdstart()
logger.debug(reply)
respi.sendsome_bytes(reply)
replystart=respi.getData()
logger.debug('reply start ' + replystart)
sleep(0.1)
replystart1=respi.getData()
logger.debug('reply start ' + replystart1)

start_time = time.time()
max_time = 10
#ack reply
logger.debug('ack ') 
#reply1 = respi.cmd('01','00','03','00','01','00')
reply2=respi.cmdack()
respi.sendsome_bytes(reply2)


def read_fromrespi():
    global readingdata
    readingdata = True
    logger.info('Get data from respi ')
    replystart=respi.getData()
    #logger.debug('data ' + replystart)
    #logger.debug('reply ack %s ' % replystart)
    respi_measuring = True
    restreply=bytearray()
    max_time = 10
    start_time = time.time()
    while (time.time() - start_time) < max_time:
      #  if (time.time() - start_time) > max_time:
     #       print 'Time finished'
    #        break
        while replystart: 
    #     else :
           
            try :
                replystart=respi.getBytedata()
                #replystr = str(replystart) 
                replyhex = restreply + replystart
                logger.debug('Byte_data from body: ' + replyhex)
                totlength = len(replyhex)
                if respi_measuring:
                    restbyte = 24
                if totlength>restbyte+2:
                    #reset to short message
                    restreply=bytearray()
                    logger.debug('totlength: %s' % totlength)
                    # store first values
                    replyvalues = replyhex[0:restbyte]
                    # store rest of the values
                    mess_end = restbyte + 2
                    logger.debug('mess_end: %s' % mess_end)
                    lengthbyte = replyhex[mess_end]
                    startbyte = mess_end +1
                    endbyte = startbyte + lengthbyte
                    respi_measuring = False
                    logger.debug('endbyte  %s ' % endbyte)
                    logger.debug('totlength  %s ' % totlength)
                    if endbyte > totlength:
                        restbyte = endbyte - totlength
                        endbyte = totlength
                        logger.debug('short message %s ' % totlength)
                        logger.debug('short message restbyte %s ' % restbyte)
                    replyvalues = replyvalues + replyhex[startbyte:endbyte]
                    while (endbyte < totlength):
                        mess_end = endbyte +2
                        logger.debug('mess_end: %s' % mess_end)
                        lengthbyte = replyhex[mess_end]
                        startbyte = mess_end +1
                        endbyte = startbyte + lengthbyte
                        logger.debug('lengthbyte  %s ' % lengthbyte)
                        if endbyte > totlength:
                            restbyte = endbyte - totlength 
                            endbyte = totlength
                        replyvalues = replyvalues + replyhex[startbyte:endbyte]
                    intvalues = respi.cmdfile(replyvalues)
                    valuebytefile.write(bytes(replyvalues))
                    valuebytefile.flush()
                    intfile.write(str(intvalues))
#                    respi.cmdtest(replyvalues)
                    replyhexstr = binascii.hexlify(replyvalues)
                    logger.debug('bytes written to file')
                    logger.debug('restbyte  %s ' % restbyte)
                    logger.debug('endbyte  %s ' % endbyte)
                    logger.debug('startbyte  %s ' % startbyte)
                    #print int(lengthbyte)
                    logger.debug(lengthbyte) 
                    #print(replyhexstr)
                    #sys.stdout.write(replyhexstr)
                    #logger.debug(lengthint)
                    #if replystart
                    bytefile.write(bytes(replyhex))
                # if message i to short store message and get more bytes
                else:
                     restreply=replyhex
                     logger.debug('short added reply  %s ' % restreply)
    #        respi.cmdfile(replyvalues)       
           #valuebytefile.write(bytes(replyvalues))
            except KeyboardInterrupt:
                respi.cmdStop()
                sleep(5)
                logger.debug( '\nStopping data collection, due to keyboardinterrupt \n ' ) 
                replystart=respi.getData()
                logger.debug('reply start ' + replystart)
                sleep(0.1)
                replystart1=respi.getData()
                logger.debug('reply start ' + replystart1)

#NYTT
                if replystart:
                    replystart=respi.getData()
                    logger.debug('reply start ' + replystart)
                    sleep(0.1)
                    replystart1=respi.getData()
                    logger.debug('reply start ' + replystart1)
                else :
                    logger.debug('ack ')
                    reply2=respi.cmdack()
                    respi.sendsome_bytes(reply2)
                    replystart=respi.getData()

                logger.info('Power off')
                reply = respi.cmdPoweroff()
                logger.debug(reply)
                respi.sendsome_bytes(reply)
                replystart=respi.getData()
                logger.debug('reply settings ' + replystart)
                replystart=respi.getData()
                logger.debug('reply settings ' + replystart)
                logger.info('Ack ')
                reply = respi.cmdack()
                logger.debug(reply)
                respi.sendsome_bytes(reply)
    #new
                bytefile.close()
                valuebytefile.close()
                intefile.close()

                respi.closesocket
   
                break
            if (time.time() - start_time) > max_time:
#                global readingdata
 #               readingdata = False
                print '\n Time finished \n'
                respi.cmdStop()
                sleep(5)
                logger.debug( '\n Stopping data collection, due to no time left \n')
                replystart=respi.getData()
                logger.debug('reply start ' + replystart)
                sleep(0.1)
                replystart1=respi.getData()
                logger.debug('reply start ' + replystart1)      
                if replystart:
                    replystart=respi.getData()
                    logger.debug('reply start ' + replystart)
                    sleep(0.1)
                    replystart1=respi.getData()
                    logger.debug('reply start ' + replystart1)
                else :
                    logger.debug('ack ')
                    reply2=respi.cmdack()
                    respi.sendsome_bytes(reply2)
                    replystart=respi.getData()

                logger.info('Power off')
                reply = respi.cmdPoweroff()
                logger.debug(reply)
                respi.sendsome_bytes(reply)
                replystart=respi.getData()
                logger.debug('reply settings ' + replystart)
                replystart=respi.getData()
                logger.debug('reply settings ' + replystart)
                logger.info('Ack ')
                reply = respi.cmdack()
                logger.debug(reply)
                respi.sendsome_bytes(reply)
#new
                bytefile.close()
                valuebytefile.close()
                intfile.close()
                global readingdata
                readingdata = False
                respi.closesocket
            break     
    global readingdata
    readingdata = False   
    respi.closesocket


#Malins plot file

    
def filtrering() :
    start = time.time()
    
    Fs = 100
    fs = 100
    Fc = 3
    cutOff = Fc
    order = 2
    def butter_lowpass(cutOff, fs, order):
        nyq = 0.5 * fs
        normalCutoff = cutOff / nyq
        b, a = butter(order, normalCutoff, btype='low', analog = True)
        return b, a

    def butter_lowpass_filter(data, cutOff, fs, order):
        b, a = butter_lowpass(cutOff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    lowcut = 0.1
    highcut = 3
    def butter_bandpass(lowcut, highcut, fs, order=2):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        y1 = lfilter(b, a, data)
        return y1
    
    sleep(0.5)
    data = open('valuebytefile.bin', 'rb')
    length = os.path.getsize("valuebytefile.bin")
    while True :
        where = data.tell()
        line = data.readline()
        if not line:
            time.sleep(0.05)
            file.seek(where)
        else: 
   
            count = 0    
            c = []
            d = []
            ero = 442
            erd = 4345.2
            eiro = 840
            eird = 733.58
        def div(a,b):
            if a.shape < b.shape:
                a = a[0:a.shape-1]
            if a.shape < a.shape:
                b = b[0:b.shape-1]
            else :
                divd = a/b        
            return divd
        maxtime = 10
   
        global readingdata
        while length > 8:       
#        while (time.time() - start_time) < max_time:    
            a = data.read(2)
            b = a.encode('hex')
            e = int(b, 16)    
            c.append(e)             
            d = c + d
            n = 0
            count = count + 1 
            lend = len(d)
            heltal = (int(lend/4))*4 
            n = 1
            #if heltal > 4:
            while lend > (800*n)  :
                dcir = d[0::4]
                acir = d[1::4]
                dcr = d[2::4]
                acr = d[3::4]
          
           # while time.time() 
                dcirt = dcir[200*(n-1):200*n]
                dcrt = dcr[200*(n-1):200*n]
                acrt = acr[200*(n-1):200*n]
                acirt = acir[200*(n-1):200*n]
#            dcir1 = respi.tail(dcirt,200)
 #           dcr1 = respi.tail(dcrt,200)
  #          acr1 = respi.tail(acrt,200)
   #         acir1 = respi.tail(acirt,200)

                print len(acirt)
       # print "inne i loop", acr, dcr, acir, dcir
                acr2 = np.sqrt(np.mean(acrt))
                dcir2 = np.mean(dcirt)
                dcr2 = np.mean(dcrt)  
                acir2 = np.sqrt(np.mean(acirt))
                Ra = Ra2 = R = 0 
           # Ra = map(div, acr2, dcr2)
                Ra = div(acr2,dcr2)           
     #Ra = sum(Ra)/len(acr1) 
          #  Ra2 = map(div, acir2, dcir2)
                Ra2 = div(acir2,dcir2)    
           #Ra2 = sum(Ra2)/len(dcir1)
                R = div(Ra,Ra2)
        
#            print (time.time() - start)                        
                OS = (erd - R*eird)/((R*(eiro-eird))-(ero - erd));
                print '\nOxygen saturation = ', OS*100, 'Procents \n'
                osfile=open("osfile.txt","w")       
                yir = butter_lowpass_filter(acirt, cutOff, fs, order)
                yr = butter_lowpass_filter(acrt, cutOff, fs, order)
            
                sgfir = savgol_filter(yir, 41, 1)
                sgfr = savgol_filter(yr, 41, 1)

                acr2 = np.sqrt(np.mean(sgfr))
                dcir2 = np.mean(dcirt)
                dcr2 = np.mean(dcrt)
                acir2 = np.sqrt(np.mean(sgfir))
            
                Ran = Ra2n = Rn = 0
             # Ran = map(div, yr, dcr2)
                Ran = div(acr2, dcr2)
#            Ran = sum(Ran)/len(yr)
                Ra2n = div(acir2, dcir2)
           #Ra2n = map(div, yir, dcir2)
 #           Ra2n = sum(Ra2n)/len(dcir)
                Rn = div(Ran,Ra2n)
                
                OSn = (erd - Rn*eird)/((Rn*(eiro-eird))-(ero - erd));
                print '\nFiltered oxygen saturation = ', OSn*100, 'Procents \n'
                osfile=open("osfile.txt","w")                
                OSn = str(OSn)
                osfile.write(OSn)
                osfile.close()
                n = n + 1
        

            count = count + 1
            valuebytefile.close()
   
   # plt.figure(1)
#t = np.linspace(0,np.size(acir)/Fs,Fs, endpoint = False)
    #y = butter_lowpass_filter(acir, cutOff, fs, order)
#    plt.subplot(311)
 #   plt.plot(acir,'b-',linewidth=2, label='Unfiltered data')
  #  plt.xlabel('Samples')
   # plt.ylabel('Amplitude')

#    plt.subplot(312)
 #   plt.plot(y,'g-',linewidth=2, label='Filtered data - lowpass')
  #  plt.xlabel('Samples')
   # plt.ylabel('Amplitude')

#    plt.subplot(313)
 #   y1 = butter_bandpass_filter(acir, lowcut, highcut, fs, order=2)
  #  plt.plot(y1,'b-', linewidth=2, label='Filtered data - bandpass')
   # plt.xlabel('Samples')
   # plt.ylabel('Amplitude')

#    plt.grid()
 #   plt.legend()
  #  plt.subplots_adjust(hspace=0.35)
   # plt.show(block = True)


def malintest():
    i = 0
    while i < 50:
        print 'hej'+ str(i)
        sleep(0.2)
        i = i + 1

if __name__ == '__main__': 
    p1 = Thread(target=read_fromrespi).start() 
    p2 = Thread(target = filtrering).start()
    #p2 = Thread(target = malintest).start()

#read_fromrespi()
#filtrering()
