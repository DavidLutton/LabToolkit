#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import _serial_helper

def siggen_set(port,freq):
    try:
        import serial
        from serial import SerialException
    except ImportError:
        print( "Import Error: Did you pip install the serial module?" )
        # print( "In a command prompt run:  pip3 install pyserial" )

    try:
        ser = serial.Serial(port, 57600, timeout=1)
    except SerialException:
        print( 'Port is not ready' )
    else:
        ser.write( b'\x8F' )
        ser.write( b'f' + freq.encode() )
        ser.read( 1 )
        ser.close()


def main(argv):
    print( argv )
    _serial_helper.dump_port_list()
    port = _serial_helper.set_port()
    #port="COM4"
 
    while(1):
        print( '\n--- Frequency in MHz:')   #, file=sys.stderr,flush=True )
        freq = sys.stdin.readline().strip()
        if(freq!=""):
           freq = "{:0>10d}".format( int(float(freq+"e6")) )
           print( freq + " Hz" )
           siggen_set( port, freq )


''' This block allows you to escape the code with Ctrl-c '''
if __name__ == "__main__":
    try:
        main( sys.argv )
    except KeyboardInterrupt:
        print( 'Received Ctrl-c' )
