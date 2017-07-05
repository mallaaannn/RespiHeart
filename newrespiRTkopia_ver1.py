# Code written by Malin Thunholm and Peter Thunholm for a project during Spring 2017
# regarding RespiHeart a new product under developement at Region Östergötland, Sweden.

#!/usr/bin/env python
from __future__ import division
from scipy.signal import butter, lfilter
from scipy.signal import freqs
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
logger.setLevel(logging.DEBUG)

bd_addr="00:0B:CE:0C:0A:8D"
#bd_addr = "B8:27:EB:E2:06:E3"

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


#ack reply
logger.debug('ack ') 
#reply1 = respi.cmd('01','00','03','00','01','00')
reply2=respi.cmdack()
respi.sendsome_bytes(reply2)
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
                intfile.write(str(intvalues))
                replyhexstr = binascii.hexlify(replyvalues)
                logger.debug('bytes written to file')
                logger.debug('restbyte  %s ' % restbyte)
                logger.debug('endbyte  %s ' % endbyte)
                logger.debug('startbyte  %s ' % startbyte)
                #print int(lengthbyte)
                logger.debug(lengthbyte) 
                #print(replyhexstr)
                sys.stdout.write(replyhexstr)
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

#        logger.debug('ack ')
 #       reply2=respi.cmdack()
  #      respi.sendsome_bytes(reply2)
#	replystart=respi.getData()
    #    respi.cmdPoweroff()
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
        #replystart=respi.getData()  #new
        #logger.debug('reply start ' + replystart)  #new
        #logger.debug('ack ')  # new
            bytefile.close()
            valuebytefile.close()
            intefile.close()

            respi.closesocket
   
            break
        if (time.time() - start_time) > max_time:
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
        #replystart=respi.getData()  #new
        #logger.debug('reply start ' + replystart)  #new
        #logger.debug('ack ')  # new
            bytefile.close()
            valuebytefile.close()
            intfile.close()

            respi.closesocket
        break        
respi.closesocket

respi.cmdplot('valuebytefile.bin')

#data = open('valuebytefile.bin', 'rb')
#length = os.path.getsize("valuebytefile.bin")



#length1 = len(c)
#lengthc = len(c)/4

#def follow(thefile)
   # thefile.seek(0,2)
  #  while True:
    #    line = thefile.readline()
   #     if not line: 
  #          time.sleep(0.1)
 #           continue
#        yield line

#if __name__ == '__main__':
 #   logfile = open(valuebytefil
#while (1):
   
 #   while count < length/2:
  #      a = data.read(2)
   #     b = a.encode("hex")
    #    c.append(b)    
   # mat1 = np.reshape(mat,(lengthc,4))
     #   for k in c: 
      #      ma   t1.append(int(k,16))
       # print mat1   
        #count = count + 1
     

#dcir = mat1[:,0]
#acir = mat1[:,1]
#dcr = mat1[:,2]
#acr = mat1[:,3]
#sh = acir.shape
#print '\n Shape:', sh

#np.array(mat1)
#for list in array:
   # print(list)
   # for item in list:    
# da = np.fromstring(line, dtype = float, sep = ',')
       # print(item)
#count1 = 0
#length1 = len(c)
#lengthc = len(c)/4

#mat = []
#for k in c:
#    mat.append(int(k, 16))
#mat1 = np.reshape(mat, (lengthc,4))

#dcir = mat1[2000:4000,0]
#acir = mat1[2000:4000,1]
#dcr = mat1[2000:4000,2]
#acr = mat1[2000:4000,3]


#dcir = mat1[:,0]
#acir = mat1[:,1]
#dcr = mat1[:,2]
#acr = mat1[:,3]
#sh = acir.shape
#print '\n Shape:', sh

#plt.figure(1)
#plt.subplot(311)
#plt.plot(acir)
#plt.xlabel('Samples')
#plt.ylabel('Amplitude')
#plt.saveplot()
#plt.show(block=True)




def div(a,b):
    return a/b

ero = 442
erd = 4345.2
eiro = 840
eird = 733.58

#print acir
Ra = map(div, acr, dcr)
Ra = sum(Ra)/len(acr)
#print Ra
Ra2 = map(div, acir, dcir)
Ra2 = sum(Ra2)/len(dcir)

#print Ra2 

R = div(Ra,Ra2)
#print '%.4f, %.4f, %.4f ' % (R, Ra, Ra2)
OS = (erd - R*eird)/((R*(eiro-eird))-(ero - erd));
print '\nOxygen saturation = ', OS*100, ' Procents \n'
osfile=open("osfile.txt","w")
#os = type(OS)
#print os
OS = str(OS)
osfile.write(OS)
osfile.close()

#print dcir
#print acir
#print dcr
#print acr

Fs = 100
fs = 100
Fc = 12
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

#T = len(acir)/Fs
#N = int(T * fs)
#t = np.linspace(0, T, N , endpoint = False)
#w = t.shape
#w1 = acir.shape
#print w, w1
plt.figure(1)
#t = np.linspace(0,np.size(acir)/Fs,Fs, endpoint = False)
y = butter_lowpass_filter(acir, cutOff, fs, order)
plt.subplot(311)
plt.plot(acir,'b-',linewidth=2, label='Unfiltered data')
plt.xlabel('Samples')
plt.ylabel('Amplitude')

plt.subplot(312)
plt.plot(y,'g-',linewidth=2, label='Filtered data - lowpass')
plt.xlabel('Samples')
plt.ylabel('Amplitude')

plt.subplot(313)
y1 = butter_bandpass_filter(acir, lowcut, highcut, fs, order=2)
plt.plot(y1,'b-', linewidth=2, label='Filtered data - bandpass')
plt.xlabel('Samples')
plt.ylabel('Amplitude')

plt.grid()
plt.legend()
plt.subplots_adjust(hspace=0.35)
plt.show(block = True)

#fo = open('valuebytefile.bin', 'rw+')
#print ('Name of file: ' fo.name)

line = fo.readline()
#print 'Read line: %s ' % (line)

line = fo.readline(5)
#print 'Read line: %s ' % (line)

#fo.close()
