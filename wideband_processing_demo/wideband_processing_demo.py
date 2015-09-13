#!/usr/bin/env python

from optparse import OptionParser
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option

from gnuradio import blocks
from gnuradio import gr

from math import pi

import osmosdr
import grgsm

from wideband_receiver import *


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-s", "--samp-rate", dest="samp_rate", type="float", default=2e6,
        help="Set sample rate [default=%default] - allowed values even_number*0.2e6")
    parser.add_option("-f", "--channel-central-freq", dest="channel_central_freq", type="float", default=939e6,
        help="Central frequecny of GSM channel that is in the middle [default=%default]")
    parser.add_option("-i", "--ifile-name", dest="ifile_name", type="string", default="",
        help="Set input file name [default=%default]")
    parser.add_option("-p", "--ppm", dest="ppm", type="intx", default=0,
        help="Set frequency correction in ppm [default=%default]")
        
    (options, args) = parser.parse_args()
    
    socket_pdu_0_0 = blocks.socket_pdu("UDP_SERVER", "127.0.0.1", "4729", 10000, False)
    
    topblock = gr.top_block()

    wideband_receiver_0 = wideband_receiver(OSR=4, fc=options.channel_central_freq, samp_rate=options.samp_rate)
    gsm_extract_system_info_0 = grgsm.extract_system_info()

    #creating signal source and connecting it to the wideband receiver
    if options.ifile_name != "": 
        file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, options.ifile_name, False) #if file name is given process data from file
        topblock.connect((file_source_0, 0), (wideband_receiver_0,0))
    else:
        rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" ) #if no file name is given process data from rtl_sdr source
        rtlsdr_source_0.set_sample_rate(options.samp_rate)
        rtlsdr_source_0.set_center_freq(options.channel_central_freq-0.1e6, 0) #capture half of GSM channel lower than channel center (-0.1MHz) - this is needed when even number of channels is captured in order to process full captured bandwidth
        rtlsdr_source_0.set_freq_corr(options.ppm, 0)  #correction of central frequency - if the receiver has large frequency offset value of this variable should be set close to that offset in ppm
        rtlsdr_source_0.set_dc_offset_mode(2, 0)
        rtlsdr_source_0.set_iq_balance_mode(0, 0)
        rtlsdr_source_0.set_gain_mode(True, 0)
        rtlsdr_source_0.set_bandwidth(options.samp_rate, 0)
          
        blocks_rotator_cc_0 = blocks.rotator_cc(-2*pi*0.1e6/options.samp_rate) #shift again by -0.1MHz in order to align channel center in 0Hz
        topblock.connect((rtlsdr_source_0, 0), (blocks_rotator_cc_0, 0))
        topblock.connect((blocks_rotator_cc_0, 0),(wideband_receiver_0,0))

    topblock.msg_connect(wideband_receiver_0, 'msgs', gsm_extract_system_info_0, 'msgs')

    topblock.start()
    topblock.wait()

