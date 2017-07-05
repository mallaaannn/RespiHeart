# Code written by Malin Thunholm and Peter Thunholm for a project during Spring 2017
# regarding RespiHeart a new product under developement at Region Östergötland, Sweden.

#!/usr/bin/env python
import bluetooth
from time import sleep
import sys
import binascii
import struct
from socket import * 
import rhPython
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bd_addr="00:0B:CE:0C:0A:8D"
#bd_addr = "B8:27:EB:E2:06:E3"

respi=rhPython.RHclass()
bytefile=open("bytefile.bin","wb")

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

while replystart:
    try :
        replystart=respi.getBytedata()
        replystr = str(replystart)
        logger.debug('Byte_data from body: ' + replystart)
        bytefile.write(replystr.decode('hex'))
    except KeyboardInterrupt:
        respi.cmdStop()
        sleep(5)
        logger.debug( 'Stopping data collection, due to keyboardinterrupt ' )
        replystart=respi.getData()
        logger.debug('reply start ' + replystart)
        sleep(0.1)
        replystart1=respi.getData()
        logger.debug('reply start ' + replystart1)
        logger.debug('ack ')
        reply2=respi.cmdack()
        respi.sendsome_bytes(reply2)
        
	replystart=respi.getData()
        bytefile.close()


        respi.closesocket
        break
respi.closesocket
