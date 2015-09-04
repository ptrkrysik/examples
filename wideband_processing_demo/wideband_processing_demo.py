#!/usr/bin/env python


from optparse import OptionParser
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option

from gnuradio import blocks
from gnuradio import gr

import grgsm

from wideband_receiver import *


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-s", "--samp-rate", dest="samp_rate", type="float", default=2e6,
        help="Set sample rate [default=%default] - allowed values even_number*0.2e6")
    parser.add_option("-f", "--carrier-freq", dest="carrier_freq", type="float", default=935e6,
        help="Set carrier frequency [default=%default]")
    parser.add_option("-i", "--ifile-name", dest="ifile_name", type="string", default="input.cfile",
        help="Set input file name [default=%default]")

    (options, args) = parser.parse_args()

    topblock = gr.top_block()
    file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, options.ifile_name, False)
    wideband_receiver_0 = wideband_receiver(OSR=4, fc=options.carrier_freq, samp_rate=options.samp_rate)
    gsm_extract_system_info_0 = grgsm.extract_system_info()

    #making connections in the topblock
    topblock.connect((file_source_0, 0), (wideband_receiver_0, 0))
    topblock.msg_connect(wideband_receiver_0, 'msgs', gsm_extract_system_info_0, 'msgs')

    topblock.start()
    topblock.wait()
