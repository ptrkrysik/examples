import os
import sys

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from receiver_with_decoder import receiver_with_decoder
from gnuradio import blocks

class wideband_receiver(gr.hier_block2):

    def __init__(self, OSR=4, fc=939.4e6, samp_rate=0.4e6):
        gr.hier_block2.__init__(
            self, "Wideband receiver",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_in("bursts")
        self.message_port_register_hier_in("msgs")
        self.__init(OSR, fc, samp_rate)
    
    def __init(self, OSR=4, fc=939.4e6, samp_rate=0.4e6):
        ##################################################
        # Parameters
        ##################################################
        self.OSR = OSR
        self.fc = fc
        self.samp_rate = samp_rate
        self.channels_num = int(samp_rate/0.2e6)
        self.OSR_PFB = 2
        
        ##################################################
        # Blocks
        ##################################################
        self.pfb_channelizer_ccf_0 = pfb.channelizer_ccf(
            self.channels_num,
            (),
            self.OSR_PFB,
            100)
        self.pfb_channelizer_ccf_0.set_channel_map(([]))
        self.create_receivers()

        ##################################################
        # Connections
        ##################################################
        self.connect((self, 0), (self.pfb_channelizer_ccf_0, 0))
        for chan in xrange(0,self.channels_num):
            self.connect((self.pfb_channelizer_ccf_0, chan), (self.receivers_with_decoders[chan], 0))
            self.msg_connect(self.receivers_with_decoders[chan], 'bursts', self, 'bursts')
            self.msg_connect(self.receivers_with_decoders[chan], 'msgs', self, 'msgs')

    def create_receivers(self):
        self.receivers_with_decoders = {}
        for chan in xrange(0,self.channels_num):
            self.receivers_with_decoders[chan] = receiver_with_decoder(fc=self.fc, OSR=self.OSR, chan_num=chan, samp_rate=self.OSR_PFB*0.2e6)

    def get_OSR(self):
        return self.OSR

    def set_OSR(self, OSR):
        self.OSR = OSR
        self.create_receivers()

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.create_receivers()

    def get_samp_rate(self):
        return self.samp_rate
