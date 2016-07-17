#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Get Bcch Msgs From Cfile
# Generated: Sun Jul 17 22:19:42 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import grgsm
import pmt


class get_bcch_msgs_from_cfile(gr.top_block):

    def __init__(self, fc=937e6, input_file_name="input.cfile", samp_rate=100.0e6/174.0, osr=4):
        gr.top_block.__init__(self, "Get Bcch Msgs From Cfile")

        ##################################################
        # Parameters
        ##################################################
        self.fc = fc
        self.input_file_name = input_file_name
        self.samp_rate = samp_rate
        self.osr = osr

        ##################################################
        # Blocks
        ##################################################
        self.gsm_receiver_0 = grgsm.receiver(4, ([0]), ([]), False)
        self.gsm_message_printer_0 = grgsm.message_printer(pmt.intern(""), False,
            False, False)
        self.gsm_input_0 = grgsm.gsm_input(
            ppm=0,
            osr=osr,
            fc=fc,
            samp_rate_in=samp_rate,
        )
        self.gsm_control_channels_decoder_0 = grgsm.control_channels_decoder()
        self.gsm_clock_offset_control_0 = grgsm.clock_offset_control(fc, samp_rate, osr)
        self.gsm_bcch_ccch_demapper_0 = grgsm.gsm_bcch_ccch_demapper(
            timeslot_nr=0,
        )
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu("UDP_SERVER", "127.0.0.1", "4729", 10000, False)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_CLIENT", "127.0.0.1", "4729", 10000, False)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "/home/piotr/Odbiornik_gsm/gr-gsm/test_data/vf_call6_a725_d174_g5_Kc1EF00BAB3BAC7002.cfile", False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gsm_bcch_ccch_demapper_0, 'bursts'), (self.gsm_control_channels_decoder_0, 'bursts'))    
        self.msg_connect((self.gsm_clock_offset_control_0, 'ctrl'), (self.blocks_message_debug_0, 'print'))    
        self.msg_connect((self.gsm_clock_offset_control_0, 'ctrl'), (self.gsm_input_0, 'ctrl_in'))    
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.gsm_control_channels_decoder_0, 'msgs'), (self.gsm_message_printer_0, 'msgs'))    
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_bcch_ccch_demapper_0, 'bursts'))    
        self.msg_connect((self.gsm_receiver_0, 'measurements'), (self.gsm_clock_offset_control_0, 'measurements'))    
        self.connect((self.blocks_file_source_0, 0), (self.gsm_input_0, 0))    
        self.connect((self.gsm_input_0, 0), (self.gsm_receiver_0, 0))    

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.gsm_input_0.set_fc(self.fc)

    def get_input_file_name(self):
        return self.input_file_name

    def set_input_file_name(self, input_file_name):
        self.input_file_name = input_file_name

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.gsm_input_0.set_samp_rate_in(self.samp_rate)

    def get_osr(self):
        return self.osr

    def set_osr(self, osr):
        self.osr = osr
        self.gsm_input_0.set_osr(self.osr)


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "-f", "--fc", dest="fc", type="eng_float", default=eng_notation.num_to_str(937e6),
        help="Set fc [default=%default]")
    parser.add_option(
        "-i", "--input-file-name", dest="input_file_name", type="string", default="input.cfile",
        help="Set input.cfile [default=%default]")
    parser.add_option(
        "-s", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(100.0e6/174.0),
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "", "--osr", dest="osr", type="intx", default=4,
        help="Set OSR [default=%default]")
    return parser


def main(top_block_cls=get_bcch_msgs_from_cfile, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(fc=options.fc, input_file_name=options.input_file_name, samp_rate=options.samp_rate, osr=options.osr)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
