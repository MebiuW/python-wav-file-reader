#!/usr/bin/python
#    File:	prwav.py
#    Author:	Yinpeng Chen
#    Date:	2016/01/13
#    Version:	1.0
#    Purpose:	Read the wave file and take the informations.

import os.path
import sys
import struct
import numpy as np
import matplotlib.pyplot as plt

#RIFF_SECTION
riff_sec = "<4ci"
riff_str1 = "RIFF"
riff_str2 = "WAVE"

#FORMAT_SECTION
format_sec = "<8ci2h2i2h"
format_str = "fmt "

#DATA_SECTION
data_sec = "<4ci"
data_str = "data"

#DATA_TYPE
data_8bits = "B"
data_16bits = "h"

#READ_SIZE
read_s = 4096

#Normal_information_lengt
infor_len = 92

#BYTE_SIZE one byte equal 8 bits
group_s = 4

def checkpara(bps, bla, pcm,ch):
    if bps != 8 and bps != 16:
	print "bits per sample should be 8 or 16!"
	sys.exit(8)
    if bla != (ch * bps / 8):
	print "block does not aligned!"
	sys.exit(9)
    if pcm != 1:
	print "pcm format is not 1, error!"
	sys.exit(10)


def main():
    if len(sys.argv) != 2:
        print "Usage: command inputfile.wav"
        sys.exit(1)
    try:
	infile = open(sys.argv[1], 'r')
    except:
	sys.stderr.write("File error: %s: cannot be open!\n" % (sys.argv[1]))	
	sys.exit(2)
    #Store file in 3 sections
    riff = infile.read(8)
    form = infile.read(28)
    data = infile.read(8)
    #Check wav file format
    if riff[0:4] != 'RIFF' or form[:8] != 'WAVEfmt ' or\
       data[0:4] != 'data':
	print "Format shows this file is not a wav file!"
	sys.exit(5)
    try:
	riff = struct.unpack(riff_sec, riff)
	form = struct.unpack(format_sec, form)
	data = struct.unpack(data_sec, data)
    except:
	print "meta data information error, not wav file!"
	sys.exit(6)

    #Get meta data informations
    chunk_size = riff[4]
    print "chunk_size is", chunk_size

    fmt_size = form[8]
    print "fmt_size is", fmt_size

    num_channel = form[10]
    print "channel number is", num_channel
    
    sample_rate = form[11]
    print "sample rate is", sample_rate

    byte_rate = form[12]
    print "bytes per sec is", byte_rate

    block_align = form[13]
    print "block align is", block_align

    bits_psample = form[14]
    print "bits per sample is", bits_psample

    data_size = data[4]
    print "data size is", data_size
    
    checkpara(bits_psample, block_align, form[9],num_channel)

    #read whole data into rawdata
    i = 0
    if (bits_psample == 16):
	data_type = "<" + 'h'
	print data_type
    elif (bits_psample == 8):
	data_type = "<" + str(1) + 'B' 
    
    readable_data = []
    for i in range(data_size/2):
	datablock = infile.read(2)
	transfer = struct.unpack(data_type,datablock)
	readable_data.append(transfer[0])
	i = i + 1
	
    #print (readable_data)
    print len(readable_data)
    readable_data = readable_data[:5000]
    plt.plot(readable_data) 
    plt.show()
    

if __name__ == "__main__":
    main()
     	
    
