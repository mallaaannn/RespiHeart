# Code written by Malin Thunholm and Peter Thunholm for a project during Spring 2017
# regarding RespiHeart a new product under developement at Region Östergötland, Sweden.

#!/usr/bin/env python
#from sh import tail
import bluetooth
from time import sleep
import sys
import binascii
import struct
from socket import * 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import os
import numpy as np
logger.info('reading bluetooth')


class RHclass:

    bd_addr = "B8:27:EB:E2:06:E3"
#    bd_addr = "00:0B:CE:0C:0A:8D"
    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
     
    def __init__(self):
        self.x=10
       # self.sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )     

    def sockconnect( self, BTaddress, port):
        logger.info('connecting bluetooth to %s ' % BTaddress)
        self.sock.connect((BTaddress, port))
        self.sock.settimeout(20.0)
    
    def closesocket(self):
        self.sock.close

    def sendsome_bytes(self, sendbyte):
        i=0
        while (i<len(sendbyte)):
   #         self.sock.settimeout(20.0)
            try:
                logger.debug('send bytes s% ')
                self.sock.sendall(sendbyte[i])
                logger.debug('Byte %s sent ' % i)
                i+=1
                sleep(0.005)
                # Receive data
                count = 0
            except timeout:
                print 'send/received failed'
                sys.exit()



    def cmdid(self):
        
        sendbyte = []
        
        inputdata1 = '01'
        inputdata2 = '00'
        inputdata3 = '02'
        inputdata4 = '00'
        inputdata5 = '05'
        inputdata6 = None
        inputdata7 = None
        inputdata8 = None
        inputdata9 = None
         

        #Decode to Hex
        sendbyte.append(inputdata1.decode('hex'))
        sendbyte.append(inputdata2.decode('hex'))
        sendbyte.append(inputdata3.decode('hex'))
        sendbyte.append(inputdata4.decode('hex'))
        sendbyte.append(inputdata5.decode('hex'))
        if inputdata6:
            sendbyte.append(inputdata6.decode('hex'))

        if inputdata7:
            sendbyte.append(inputdata7.decode('hex'))

        if inputdata8:
            sendbyte.append(inputdata8.decode('hex'))

        if inputdata9:
            sendbyte.append(inputdata9.decode('hex'))
        logger.debug('send bytes ')		         
        return sendbyte

    def cmdack(self):
#        sleep(1)
        sendbyte = []
        
        inputdata1 = '01'
        inputdata2 = '00'
        inputdata3 = '03'
        inputdata4 = '00'
        inputdata5 = '01'
        inputdata6 = '00'
        inputdata7 = None
        inputdata8 = None
        inputdata9 = None
         

        #Decode to Hex
        sendbyte.append(inputdata1.decode('hex'))
        sendbyte.append(inputdata2.decode('hex'))
        sendbyte.append(inputdata3.decode('hex'))
        sendbyte.append(inputdata4.decode('hex'))
        sendbyte.append(inputdata5.decode('hex'))
        if inputdata6:
            sendbyte.append(inputdata6.decode('hex'))

        if inputdata7:
            sendbyte.append(inputdata7.decode('hex'))

        if inputdata8:
            sendbyte.append(inputdata8.decode('hex'))

        if inputdata9:
            sendbyte.append(inputdata9.decode('hex'))
        logger.debug('send bytes ')		         
        return sendbyte

    def cmdstart(self):
        
        sendbyte = []
        
        inputdata1 = '01'
        inputdata2 = '00'
        inputdata3 = '02'
        inputdata4 = '00'
        inputdata5 = '06'
        inputdata6 = None
        inputdata7 = None
        inputdata8 = None
        inputdata9 = None
         

        #Decode to Hex
        sendbyte.append(inputdata1.decode('hex'))
        sendbyte.append(inputdata2.decode('hex'))
        sendbyte.append(inputdata3.decode('hex'))
        sendbyte.append(inputdata4.decode('hex'))
        sendbyte.append(inputdata5.decode('hex'))
        if inputdata6:
            sendbyte.append(inputdata6.decode('hex'))

        if inputdata7:
            sendbyte.append(inputdata7.decode('hex'))

        if inputdata8:
            sendbyte.append(inputdata8.decode('hex'))

        if inputdata9:
            sendbyte.append(inputdata9.decode('hex'))
        logger.debug('send bytes ')		         
        return sendbyte

    def cmdsettings(self):
        
        sendbyte = []
        
        inputdata1 = '01'
        inputdata2 = '00'
        inputdata3 = '05'
        inputdata4 = '00'
        inputdata5 = '0B'
        inputdata6 = '00'
        inputdata7 = '47'
        inputdata8 = '05' 
        inputdata9 = None
        #test byte 
        inputdata10 = None 
        #Decode to Hex
        sendbyte.append(inputdata1.decode('hex'))
        sendbyte.append(inputdata2.decode('hex'))
        sendbyte.append(inputdata3.decode('hex'))
        sendbyte.append(inputdata4.decode('hex'))
        sendbyte.append(inputdata5.decode('hex'))
        if inputdata6:
            sendbyte.append(inputdata6.decode('hex'))

        if inputdata7:
            sendbyte.append(inputdata7.decode('hex'))

        if inputdata8:
            sendbyte.append(inputdata8.decode('hex'))

        if inputdata9:
            sendbyte.append(inputdata9.decode('hex'))
        logger.debug('send bytes ')		         
        return sendbyte

    def cmdsensor(self):
        
       sendbyte = []
        
       inputdata1 = '01'
       inputdata2 = '00'
       inputdata3 = '09'
       inputdata4 = '00'
       inputdata5 = '0D'
       inputdata6 = '00'
       inputdata7 = '50'
       inputdata8 = '03'
       inputdata9 = '03'
       inputdata10 = '00' 
       inputdata11 = '00'
       #svarsbit vid test 
       inputdata12 = '00' 

       #Decode to Hex
       sendbyte.append(inputdata1.decode('hex'))
       sendbyte.append(inputdata2.decode('hex'))
       sendbyte.append(inputdata3.decode('hex'))
       sendbyte.append(inputdata4.decode('hex'))
       sendbyte.append(inputdata5.decode('hex'))
       sendbyte.append(inputdata6.decode('hex'))
       sendbyte.append(inputdata7.decode('hex'))
       sendbyte.append(inputdata8.decode('hex'))
       sendbyte.append(inputdata9.decode('hex'))
       sendbyte.append(inputdata10.decode('hex'))
       sendbyte.append(inputdata11.decode('hex'))
       if inputdata12:
          sendbyte.append(inputdata12.decode('hex'))

       logger.debug('send bytes ')		         
       return sendbyte

    def cmdsensor1(self):
        
        sendbyte = []
        
        inputdata1 = '01'
        inputdata2 = '00'
        inputdata3 = '09'
        inputdata4 = '00'
        inputdata5 = '0D'
        inputdata6 = '01'
        inputdata7 = '50'
        inputdata8 = '03'
        inputdata9 = '03'
        inputdata10 = '00' 
        inputdata11 = '00'
        #svarsbit vid test 
        inputdata12 = '00' 

        #Decode to Hex
        sendbyte.append(inputdata1.decode('hex'))
        sendbyte.append(inputdata2.decode('hex'))
        sendbyte.append(inputdata3.decode('hex'))
        sendbyte.append(inputdata4.decode('hex'))
        sendbyte.append(inputdata5.decode('hex'))
        sendbyte.append(inputdata6.decode('hex'))
        sendbyte.append(inputdata7.decode('hex'))
        sendbyte.append(inputdata8.decode('hex'))
        sendbyte.append(inputdata9.decode('hex'))
        sendbyte.append(inputdata10.decode('hex'))
        sendbyte.append(inputdata11.decode('hex'))
        if inputdata12:
           sendbyte.append(inputdata12.decode('hex'))
        logger.debug('send bytes ')		         
        return sendbyte
     
    def cmd(self, byte1, byte2, byte3, byte4,byte5, byte6=None, byte7=None ,byte8=None, byte9=None):
        
       sendbyte = []
       
       inputdata1 = byte1
       inputdata2 = byte2
       inputdata3 = byte3
       inputdata4 = byte4
       inputdata5 = byte5
       inputdata6 = byte6
       inputdata7 = byte7
       inputdata8 = byte8
       inputdata9 = byte9
         

       #Decode to Hex
       sendbyte.append(inputdata1.decode('hex'))
       sendbyte.append(inputdata2.decode('hex'))
       sendbyte.append(inputdata3.decode('hex'))
       sendbyte.append(inputdata4.decode('hex'))
       sendbyte.append(inputdata5.decode('hex'))
       if inputdata6:
           sendbyte.append(inputdata6.decode('hex'))

       if inputdata7:
           sendbyte.append(inputdata7.decode('hex'))

       if inputdata8:
           sendbyte.append(inputdata8.decode('hex'))

       if inputdata9:
           sendbyte.append(inputdata9.decode('hex'))
       logger.debug('send bytes ')		         
       return sendbyte


    def getData(self): 
        sleep(0.1)
        self.sock.settimeout(20.0)
        try:
           count = 0
           # Code for starting sampling
           reply = self.sock.recv(1024)
           reply = binascii.hexlify(reply)
          # replyint = struct.unpack(">L",reply)[0]
          # replyint = ord(reply)    
          # replyint = int(reply.encode('hex'), 16)       
          
          #print repr(replyint)
           #print "Recived data: " +  reply 
        except error:
           print 'send/received failed'
           sys.exit()
        return reply
      # Send bytes    

    def getBytedata(self):
       # sleep(0.1)
        self.sock.settimeout(20.0)
        try:
           count = 0
           # Code for starting sampling
           reply = self.sock.recv(1024)
          # replyint = int(reply.encode('hex'), 16)
           #reply = binascii.hexlify(reply)
           reply = bytearray(reply) 
        except error:
           print 'send/received failed'
           sys.exit()
        return reply
      # Send bytes    



             
             
    def cmdPoweroff(self):

        sendbyte = []

        inputdata1 = '01'
        inputdata2 = '00'
        inputdata3 = '02'
        inputdata4 = '00'
        inputdata5 = '09'
        inputdata6 = None
        inputdata7 = None
        inputdata8 = None
        inputdata9 = None


        #Decode to Hex
        sendbyte.append(inputdata1.decode('hex'))
        sendbyte.append(inputdata2.decode('hex'))
        sendbyte.append(inputdata3.decode('hex'))
        sendbyte.append(inputdata4.decode('hex'))
        sendbyte.append(inputdata5.decode('hex'))
        if inputdata6:
            sendbyte.append(inputdata6.decode('hex'))

        if inputdata7:
            sendbyte.append(inputdata7.decode('hex'))

        if inputdata8:
            sendbyte.append(inputdata8.decode('hex'))

        if inputdata9:
            sendbyte.append(inputdata9.decode('hex'))
        logger.debug('send bytes ')
        return sendbyte


    def cmdStop(self):

        sendbyte = []

        inputdata1 = '01'
        inputdata2 = '00'
        inputdata3 = '02'
        inputdata4 = '00'
        inputdata5 = '07'
        inputdata6 = None
        inputdata7 = None
        inputdata8 = None
        inputdata9 = None


        #Decode to Hex
        sendbyte.append(inputdata1.decode('hex'))
        sendbyte.append(inputdata2.decode('hex'))
        sendbyte.append(inputdata3.decode('hex'))
        sendbyte.append(inputdata4.decode('hex'))
        sendbyte.append(inputdata5.decode('hex'))
        if inputdata6:
            sendbyte.append(inputdata6.decode('hex'))

        if inputdata7:
            sendbyte.append(inputdata7.decode('hex'))

        if inputdata8:
            sendbyte.append(inputdata8.decode('hex'))

        if inputdata9:
            sendbyte.append(inputdata9.decode('hex'))
        logger.debug('send bytes ')
        return sendbyte

    def cmdAbort(self):

        sendbyte = []

        inputdata1 = '01'
        inputdata2 = '00'
        inputdata3 = '02'
        inputdata4 = '00'
        inputdata5 = '08'
        inputdata6 = None
        inputdata7 = None
        inputdata8 = None
        inputdata9 = None


        #Decode to Hex
        sendbyte.append(inputdata1.decode('hex'))
        sendbyte.append(inputdata2.decode('hex'))
        sendbyte.append(inputdata3.decode('hex'))
        sendbyte.append(inputdata4.decode('hex'))
        sendbyte.append(inputdata5.decode('hex'))
        if inputdata6:
            sendbyte.append(inputdata6.decode('hex'))

        if inputdata7:
            sendbyte.append(inputdata7.decode('hex'))

        if inputdata8:
            sendbyte.append(inputdata8.decode('hex'))

        if inputdata9:
            sendbyte.append(inputdata9.decode('hex'))
        logger.debug('send bytes ')
        return sendbyte

            

                                
    def cmdfile(self, values):
        self.sock.settimeout(20.0)
        try :
           # valuebytefile=open("valuebytefile.bin","wb")
            #valmat = []       
            values = bytes(values)
            length = len(values)
            logger.debug('Length of Values %s'  % length)
            i = 0
            a = []
            c = ''
#                a = valuebytefile.read(2)
            while i < length :
                a = values[i:i+2]
               
                b = int(a.encode('hex'), 16)
              #  c.append(b)
                c =  c + ','+ str(b)  
                logger.debug('Only A  %s'  % a)
                logger.debug('Length of a %s'  % len(a))
              #  logger.debug('Length of C %s'  % len(c))
             #   intfile.write(str('hejsan'))
                i = i + 2
        except error:
            print 'send/received failed'
            sys.exit()
       # intfile.close 
       # valuebytefile.close
#        d = np.array(c).reshape(len(c)/4,4)
        logger.debug('This is C %s'  % c)
        return c



    def cmdfilter(self, data):
        ero = 442
        erd = 4345.2
        eiro = 840
        eird = 733.58
        def div(a,b):
            return a/b 
        
    def cmdplot(self, filename):
        infile = open(filename, 'rb')
        data = np.fromfile(infile, dtype = np.int16)
#        infile.close()
        length = len(data)
        i = 0 
        while i < length:
            a = infile.read(2)
            b = int(a.encode('hex'), 16)
            c.append(b)
            i = i + 2
        d = np.array(c).reshape(len(c)/4,4)
        print d 
        infile.close()


    def follow(self, thefile):
        self.sock.settimeout(20.0)
        thefile.seek(0,2)
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    if __name__ == '__main__':
        logfile = open('valuebytefile.bin', 'r')
        loglines = follow(logfile)
        for line in loglines:
            print line,


    def tail(f, n, offset=0):
#    """Reads a n lines from f with an offset of offset lines."""
    #avg_line_length = len(f) #74
        f = list(str(f))
        n = list(str(n))
        offset = list(str(offset))
        to_read = n + offset
        while 1:
            try:
                val = f.seek(to_read, 0)
            except IOError:
            # woops.  apparently file is smaller than what we want
            # to step back, go to the beginning instead
                f.seek(0)
            pos = f.tell()
            lines = f.read().splitlines()
            if len(lines) >= to_read or pos == 0:
                return lines[-to_read:offset and -offset or None]
        return val
