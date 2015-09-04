##################################################
# GNU Radio Python Flow Graph
# Title: Receiver With Decoder
# Author: Piotr Krysik
# Generated: Fri Sep  4 08:42:15 2015
##################################################

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import grgsm


class receiver_with_decoder(gr.hier_block2):

    def __init__(self, OSR=4, chan_num=0, fc=939.4e6, samp_rate=1e6):
        gr.hier_block2.__init__(
            self, "Receiver With Decoder",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_in("bursts")
        self.message_port_register_hier_in("msgs")

        ##################################################
        # Parameters
        ##################################################
        self.OSR = OSR
        self.chan_num = chan_num
        self.fc = fc
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_out = samp_rate_out = 1625000.0/6.0*OSR

        ##################################################
        # Blocks
        ##################################################
        self.gsm_receiver_0 = grgsm.receiver(OSR, ([chan_num]), ([]))
        self.gsm_control_channels_decoder_0 = grgsm.control_channels_decoder()
        self.gsm_bcch_ccch_demapper_0 = grgsm.universal_ctrl_chans_demapper(0, ([2,6,12,16,22,26,32,36,42,46]), ([1,2,2,2,2,2,2,2,2,2]))
        self.fractional_resampler_xx_0 = filter.fractional_resampler_cc(0, samp_rate/samp_rate_out)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_CLIENT", "127.0.0.1", "4729", 10000, False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gsm_bcch_ccch_demapper_0, 'bursts'), (self, 'bursts'))    
        self.msg_connect((self.gsm_bcch_ccch_demapper_0, 'bursts'), (self.gsm_control_channels_decoder_0, 'bursts'))    
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self, 'msgs'))    
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_bcch_ccch_demapper_0, 'bursts'))    
        self.connect((self.fractional_resampler_xx_0, 0), (self.gsm_receiver_0, 0))    
        self.connect((self, 0), (self.fractional_resampler_xx_0, 0))    


    def get_OSR(self):
        return self.OSR

    def set_OSR(self, OSR):
        self.OSR = OSR
        self.set_samp_rate_out(1625000.0/6.0*self.OSR)

    def get_chan_num(self):
        return self.chan_num

    def set_chan_num(self, chan_num):
        self.chan_num = chan_num

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.fractional_resampler_xx_0.set_resamp_ratio(self.samp_rate/self.samp_rate_out)

    def get_samp_rate_out(self):
        return self.samp_rate_out

    def set_samp_rate_out(self, samp_rate_out):
        self.samp_rate_out = samp_rate_out
        self.fractional_resampler_xx_0.set_resamp_ratio(self.samp_rate/self.samp_rate_out)

