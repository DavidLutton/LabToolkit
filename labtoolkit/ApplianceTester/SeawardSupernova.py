#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

try:
 import serial
except ImportError:
 print("Import Error: did pip install the module correcly")

'''try:
' import sys
except ImportError:
 print("Import Error")
'''
try:
 from serial.tools.list_ports import comports
except ImportError:
 print("Import Error: did pip install the module correcly")
 comports = None

 

def dump_port_list():
 if comports:
  print('\n--- Available ports:',file=sys.stderr,flush=True)
  for port, desc, hwid in sorted(comports()):
   print('--- %-20s %s' % (port, desc),file=sys.stderr,flush=True)

def set_port():
 print('--- Enter port name: ',file=sys.stderr,flush=True)
 try:
  port = sys.stdin.readline().strip()
 except KeyboardInterrupt:
  port = None
 return(port)



''' This module handles the summary data output of a Seaward Supernova PAT Tester over serial
@ 19200 baud
With the supplied cable
To a generic usb serial device

Some of this code could be used in part for generic serial input handlers

'''
def serialget(port):
 ''' input is expect to be blank until data starts ariving at baudrate
     and it will cut out after blank b'' reads  '''
 ser = serial.Serial(port, 19200, timeout=1)
 buffer = b""
 waiting = 0
 while(1):
  read = ser.read(82)  ## 82 is the line length of the pat tester hardware
  if read == b'' :
   if buffer == b'':
    ''' No input yet '''
    if (waiting == 0):
     print("Waiting for Data")
     waiting = 1
    else:
     print(".")
    

    
   elif buffer != b'':
    ''' Ran out of inbound data so return the cumlitave buffer for processing '''
    return buffer
  elif read != b'':
   ''' Have input to add to the buffer '''
   buffer = buffer + read
   
   ''' Just for assuring user something is going thrugh , print the buffer length out '''
   print(str(len(buffer)))
   #print(read.decode("utf-8"),end="")
 ser.close()


def linehandle(line):
 ''' mostly a check for the line length and string termination '''
 n = 1
 a = ""
 buffer = b""
 while( 1 ):
  a, line = line[:n], line[n:]
  buffer = buffer + a
  if  a == b"\n" :
   return(buffer)
   #break

def handleinput(ser):
 linelength = len(linehandle(ser))
 ser = ser[linelength*3:] # strip out the initial headers
 
 length = len(ser)
 while ( length != 0 ) :

#  leng = int( len( linehandle(ser) ) ) * 3
  #leng = linelength * 3

  string = ser[:linelength * 3]
#  target = string[:linelength*2]
#  line = target

  line = string[:linelength*2]
  line = line.translate(None, b'\n\r')
  
  line = handleline(line)
  handleprint(line)
  #handlestore(line)

  ser = ser[linelength * 3:]  # removes the length of data that has been handled
  length = len(ser) # Feeds back into the while loop 


def handleline(line):
 target = {
#  ''' This asserts that the target window is consistant '''
#  ''' This is a byte alignment to dict() transform block ''' 
  'Appliance' 	: line[0:17],
  'Date'		: line[17:25],
  'Site'		: line[27:44],
  'Location'	: line[44:61],
  'User'		: line[61:76],
  'OverStatus'	: line[76:80],
  'Earth'		: line[80:89],
  'Insulation'	: line[90:101],
  'Sub-Leak'	: line[103:113],
  'Flash'		: line[113:123],
  'Leakage'		: line[123:133],
  'Tch-Leak'	: line[133:143],
  'Load'		: line[143:156],
  'Polarity'	: line[156:160],
}
 for facts in target:
  target[facts] = target[facts].decode("utf-8") 
  ''' finally decode binary data to utf-8 '''
  target[facts] = str.rstrip(target[facts])
  target[facts] = str.lstrip(target[facts])
  ''' Strip out the whitespace to the left and right of facts '''
 return target

def handleprint(target):
 pad = ","
 #print(repr(target)) 
 #pat = target['Appliance'],target['Date'],target['Site'],target['Location'],target['User'],target['OverStatus'],target['Earth'],target['Insulation'],target['Sub-Leak'],target['Flash'],target['Leakage'],target['Tch-Leak'],target['Load'],target['Polarity']
 output = [
  target['Appliance'],
  target['Site'],
  target['Date'],
  target['Earth'],
  target['Insulation'],
  target['Polarity'],
  "...",
  #target['Location'],
  target['User'],
  target['OverStatus'],
  
  ]
 pat = ",".join(output) + "\n"

 #V2,SITE S,01/06/2015,0.05Ohm,>99.99MOhm,Pole,comment,ID,overall

''' with open("data.csv", "a") as myfile:
    myfile.write(pat)
                
            
    
 output = [
  target['Appliance'],
  target['Date'],
  target['Site'],
  target['Location'],
  target['User'],
  target['OverStatus'],
  target['Earth'],
  target['Insulation'],
  target['Sub-Leak'],
  target['Flash'],
  target['Leakage'],
  target['Tch-Leak'],
  target['Load'],
  target['Polarity'],
  ]
 pat = ",".join(output) + ""

 print(pat)
'''
  
#   with open('pat.txt', 'at') as f:
#    f.write("%s\n" % pat)




def main(argv):


 testdata = b"Appliance        Date      Site             Location         Utestdata Overall-Status\r\nEarth     Insulation   Sub-Leak  Flash     Leakage   Tch-Leak  Load     Polarity\r\n--------------------------------------------------------------------------------\r\n"
 testdata = testdata + b"3333             27/08/14  A                TEST             Utestdata 1         PASS\r\n 0.05Ohm  >99.99MOhm   SKIP      SKIP      SKIP      SKIP      SKIP         GOOD\r\n--------------------------------------------------------------------------------\r\n"
 testdata = testdata + b"4444             27/08/14  A                TEST             Utestdata 1         PASS\r\n 0.05Ohm  >99.99MOhm   SKIP      SKIP      SKIP      SKIP      SKIP         GOOD\r\n--------------------------------------------------------------------------------\r\n"
 testdata = testdata + b"5555             27/08/14  A                TEST             Utestdata 1         PASS\r\n 0.05Ohm  >99.99MOhm   SKIP      SKIP      SKIP      SKIP      SKIP         GOOD\r\n--------------------------------------------------------------------------------\r\n"
 #_patdata.handleinput(testdata)
 
 dump_port_list()
 port = set_port()
 data = serialget(port)
 print(type(data))
 with open("datalive.txt", "bw") as fh:
  fh.write(data)
  

 with open("datalive.txt", "br") as fh:
  datum  = fh.read()
  print(len(datum))
  print(type(datum))
  
  #import pathlib
  #pathlib.Path('data.csv').touch()
  #with open("data.csv", 'a'):
   # os.utime(fname, times)
      
  _patdata.handleinput(datum)
                                                           
  shutil.move("data.csv", 'Z:\\Calibration data\PAT Testing\data.csv')  

