#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Get Channel
# Generated: Fri Jun  5 00:19:32 2015
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from optparse import OptionParser
import arfcn
import math

class get_channel(gr.top_block):

    def __init__(self, channel_num=22, decim=50, directory="./", f_offset=0, fc=947.4e6, out_directory="./", samp_rate=25e6):
        gr.top_block.__init__(self, "Get Channel")

        ##################################################
        # Parameters
        ##################################################
        self.channel_num = channel_num
        self.decim = decim
        self.directory = directory
        self.f_offset = f_offset
        self.fc = fc
        self.out_directory = out_directory
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.SDCCH = SDCCH = 6
        self.RACH = RACH = 3
        self.PCH = PCH = 5
        self.CHANNEL_UNKNOWN = CHANNEL_UNKNOWN = 0
        self.CCCH = CCCH = 2
        self.BCCH = BCCH = 1
        self.AGCH = AGCH = 4

        ##################################################
        # Blocks
        ##################################################
        self.pfb_decimator_ccf_0 = pfb.decimator_ccf(
        	  decim,
        	  (),
        	  0,
        	  100,
                  True,
                  True)
        self.pfb_decimator_ccf_0.declare_sample_delay(0)
        	
        self.blocks_rotator_cc_0 = blocks.rotator_cc(-2*math.pi*(arfcn.get_freq_from_arfcn(channel_num,'e')-fc+f_offset)/samp_rate)
        self.blocks_interleaved_short_to_complex_1 = blocks.interleaved_short_to_complex(False, False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, "/home/piotr/Odbiornik_gsm/Hopping/test_data/nagranie_hopping_4", False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, ""+out_directory+"/fc_"+ str(channel_num) +".cfile", False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_interleaved_short_to_complex_1, 0))    
        self.connect((self.blocks_interleaved_short_to_complex_1, 0), (self.blocks_rotator_cc_0, 0))    
        self.connect((self.blocks_rotator_cc_0, 0), (self.pfb_decimator_ccf_0, 0))    
        self.connect((self.pfb_decimator_ccf_0, 0), (self.blocks_file_sink_0, 0))    


    def get_channel_num(self):
        return self.channel_num

    def set_channel_num(self, channel_num):
        self.channel_num = channel_num
        self.blocks_file_sink_0.open(""+self.out_directory+"/fc_"+ str(self.channel_num) +".cfile")
        self.blocks_rotator_cc_0.set_phase_inc(-2*math.pi*(arfcn.get_freq_from_arfcn(self.channel_num,'e')-self.fc+self.f_offset)/self.samp_rate)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_directory(self):
        return self.directory

    def set_directory(self, directory):
        self.directory = directory

    def get_f_offset(self):
        return self.f_offset

    def set_f_offset(self, f_offset):
        self.f_offset = f_offset
        self.blocks_rotator_cc_0.set_phase_inc(-2*math.pi*(arfcn.get_freq_from_arfcn(self.channel_num,'e')-self.fc+self.f_offset)/self.samp_rate)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.blocks_rotator_cc_0.set_phase_inc(-2*math.pi*(arfcn.get_freq_from_arfcn(self.channel_num,'e')-self.fc+self.f_offset)/self.samp_rate)

    def get_out_directory(self):
        return self.out_directory

    def set_out_directory(self, out_directory):
        self.out_directory = out_directory
        self.blocks_file_sink_0.open(""+self.out_directory+"/fc_"+ str(self.channel_num) +".cfile")

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_rotator_cc_0.set_phase_inc(-2*math.pi*(arfcn.get_freq_from_arfcn(self.channel_num,'e')-self.fc+self.f_offset)/self.samp_rate)

    def get_SDCCH(self):
        return self.SDCCH

    def set_SDCCH(self, SDCCH):
        self.SDCCH = SDCCH

    def get_RACH(self):
        return self.RACH

    def set_RACH(self, RACH):
        self.RACH = RACH

    def get_PCH(self):
        return self.PCH

    def set_PCH(self, PCH):
        self.PCH = PCH

    def get_CHANNEL_UNKNOWN(self):
        return self.CHANNEL_UNKNOWN

    def set_CHANNEL_UNKNOWN(self, CHANNEL_UNKNOWN):
        self.CHANNEL_UNKNOWN = CHANNEL_UNKNOWN

    def get_CCCH(self):
        return self.CCCH

    def set_CCCH(self, CCCH):
        self.CCCH = CCCH

    def get_BCCH(self):
        return self.BCCH

    def set_BCCH(self, BCCH):
        self.BCCH = BCCH

    def get_AGCH(self):
        return self.AGCH

    def set_AGCH(self, AGCH):
        self.AGCH = AGCH


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-c", "--channel-num", dest="channel_num", type="eng_float", default=eng_notation.num_to_str(22),
        help="Set channel_num [default=%default]")
    parser.add_option("", "--decim", dest="decim", type="intx", default=50,
        help="Set decim [default=%default]")
    parser.add_option("-d", "--directory", dest="directory", type="string", default="./",
        help="Set ./ [default=%default]")
    parser.add_option("-e", "--f-offset", dest="f_offset", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set f_offset [default=%default]")
    parser.add_option("-f", "--fc", dest="fc", type="eng_float", default=eng_notation.num_to_str(947.4e6),
        help="Set fc [default=%default]")
    parser.add_option("-o", "--out-directory", dest="out_directory", type="string", default="./",
        help="Set ./ [default=%default]")
    parser.add_option("-s", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(25e6),
        help="Set samp_rate [default=%default]")
    (options, args) = parser.parse_args()
    tb = get_channel(channel_num=options.channel_num, decim=options.decim, directory=options.directory, f_offset=options.f_offset, fc=options.fc, out_directory=options.out_directory, samp_rate=options.samp_rate)
    tb.start()
    tb.wait()
