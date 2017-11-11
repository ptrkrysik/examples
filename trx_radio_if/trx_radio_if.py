#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Trx radio interface
# Author: (C) Piotr Krysik 2017
# Description: Alpha version of trx radio interface
# Generated: Sat Nov 11 11:20:15 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grgsm import gsm_gmsk_mod
from optparse import OptionParser
import grgsm
import math
import time


class trx_radio_if(gr.top_block):

    def __init__(self, delay_correction=285.616e-6, fc_downlink=938600000, fc_uplink=938900000, gain_downlink=40, gain_uplink=60, osr=4, ppm=-1, samp_rate=13e6/12.0, samp_rate_downlink=13e6/12.0, timing_advance=0):
        gr.top_block.__init__(self, "Trx radio interface")

        ##################################################
        # Parameters
        ##################################################
        self.delay_correction = delay_correction
        self.fc_downlink = fc_downlink
        self.fc_uplink = fc_uplink
        self.gain_downlink = gain_downlink
        self.gain_uplink = gain_uplink
        self.osr = osr
        self.ppm = ppm
        self.samp_rate = samp_rate
        self.samp_rate_downlink = samp_rate_downlink
        self.timing_advance = timing_advance

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_clock_rate(26e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(fc_downlink, 0)
        self.uhd_usrp_source_0.set_gain(gain_downlink, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        	"packet_len",
        )
        self.uhd_usrp_sink_0.set_clock_rate(26e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_0.set_subdev_spec("A:B", 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(fc_uplink, 0)
        self.uhd_usrp_sink_0.set_gain(gain_uplink, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 125e3, 5e3, firdes.WIN_HAMMING, 6.76))
        self.gsm_txtime_setter_0 = grgsm.txtime_setter(None if (None is not None) else 0xffffffff, 0, 0, 0, 0, 0, 0)
        self.gsm_trx_burst_if_0 = grgsm.trx_burst_if("127.0.0.1", "5700")
        self.gsm_receiver_0 = grgsm.receiver(4, ([0]), ([4]), False)
        self.gsm_preprocess_tx_burst_0 = grgsm.preprocess_tx_burst()
        self.gsm_msg_to_tag_0_0 = grgsm.msg_to_tag()
        self.gsm_msg_to_tag_0 = grgsm.msg_to_tag()
        self.gsm_gmsk_mod_0 = gsm_gmsk_mod(
            BT=0.3,
            pulse_duration=4,
            sps=osr,
        )
        self.gsm_controlled_rotator_cc_0_0 = grgsm.controlled_rotator_cc(-ppm/1.0e6*2*math.pi*fc_downlink/samp_rate)
        self.gsm_controlled_rotator_cc_0 = grgsm.controlled_rotator_cc(ppm/1.0e6*2*math.pi*fc_downlink/samp_rate)
        self.gsm_burst_type_filter_0 = grgsm.burst_type_filter(([3]))
        self.gsm_burst_to_fn_time_0 = grgsm.burst_to_fn_time()
        self.digital_burst_shaper_xx_0 = digital.burst_shaper_cc((firdes.window(firdes.WIN_HANN, 16, 0)), 0, 20, False, "packet_len")
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gsm_burst_to_fn_time_0, 'fn_time_out'), (self.gsm_txtime_setter_0, 'fn_time'))    
        self.msg_connect((self.gsm_burst_type_filter_0, 'bursts_out'), (self.gsm_burst_to_fn_time_0, 'bursts_in'))    
        self.msg_connect((self.gsm_preprocess_tx_burst_0, 'bursts_out'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))    
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_burst_type_filter_0, 'bursts_in'))    
        self.msg_connect((self.gsm_receiver_0, 'C0'), (self.gsm_trx_burst_if_0, 'bursts'))    
        self.msg_connect((self.gsm_trx_burst_if_0, 'bursts'), (self.gsm_txtime_setter_0, 'bursts_in'))    
        self.msg_connect((self.gsm_txtime_setter_0, 'bursts_out'), (self.gsm_preprocess_tx_burst_0, 'bursts_in'))    
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.gsm_gmsk_mod_0, 0))    
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.gsm_msg_to_tag_0_0, 0))    
        self.connect((self.gsm_controlled_rotator_cc_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.gsm_controlled_rotator_cc_0_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.gsm_gmsk_mod_0, 0), (self.digital_burst_shaper_xx_0, 0))    
        self.connect((self.gsm_msg_to_tag_0, 0), (self.gsm_controlled_rotator_cc_0, 0))    
        self.connect((self.gsm_msg_to_tag_0_0, 0), (self.gsm_controlled_rotator_cc_0_0, 0))    
        self.connect((self.low_pass_filter_0_0, 0), (self.gsm_receiver_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.gsm_msg_to_tag_0, 0))    

    def get_delay_correction(self):
        return self.delay_correction

    def set_delay_correction(self, delay_correction):
        self.delay_correction = delay_correction

    def get_fc_downlink(self):
        return self.fc_downlink

    def set_fc_downlink(self, fc_downlink):
        self.fc_downlink = fc_downlink
        self.gsm_controlled_rotator_cc_0.set_phase_inc(self.ppm/1.0e6*2*math.pi*self.fc_downlink/self.samp_rate)
        self.gsm_controlled_rotator_cc_0_0.set_phase_inc(-self.ppm/1.0e6*2*math.pi*self.fc_downlink/self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.fc_downlink, 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request_t(self.fc_downlink, self.fc_uplink-self.fc_downlink), 1)

    def get_fc_uplink(self):
        return self.fc_uplink

    def set_fc_uplink(self, fc_uplink):
        self.fc_uplink = fc_uplink
        self.uhd_usrp_sink_0.set_center_freq(self.fc_uplink, 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request_t(self.fc_downlink, self.fc_uplink-self.fc_downlink), 1)

    def get_gain_downlink(self):
        return self.gain_downlink

    def set_gain_downlink(self, gain_downlink):
        self.gain_downlink = gain_downlink
        self.uhd_usrp_source_0.set_gain(self.gain_downlink, 0)
        	

    def get_gain_uplink(self):
        return self.gain_uplink

    def set_gain_uplink(self, gain_uplink):
        self.gain_uplink = gain_uplink
        self.uhd_usrp_sink_0.set_gain(self.gain_uplink, 0)
        	

    def get_osr(self):
        return self.osr

    def set_osr(self, osr):
        self.osr = osr
        self.gsm_gmsk_mod_0.set_sps(self.osr)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self.gsm_controlled_rotator_cc_0.set_phase_inc(self.ppm/1.0e6*2*math.pi*self.fc_downlink/self.samp_rate)
        self.gsm_controlled_rotator_cc_0_0.set_phase_inc(-self.ppm/1.0e6*2*math.pi*self.fc_downlink/self.samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.gsm_controlled_rotator_cc_0.set_phase_inc(self.ppm/1.0e6*2*math.pi*self.fc_downlink/self.samp_rate)
        self.gsm_controlled_rotator_cc_0_0.set_phase_inc(-self.ppm/1.0e6*2*math.pi*self.fc_downlink/self.samp_rate)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 125e3, 5e3, firdes.WIN_HAMMING, 6.76))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_samp_rate_downlink(self):
        return self.samp_rate_downlink

    def set_samp_rate_downlink(self, samp_rate_downlink):
        self.samp_rate_downlink = samp_rate_downlink

    def get_timing_advance(self):
        return self.timing_advance

    def set_timing_advance(self, timing_advance):
        self.timing_advance = timing_advance


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--delay-correction", dest="delay_correction", type="eng_float", default=eng_notation.num_to_str(285.616e-6),
        help="Set delay_correction [default=%default]")
    parser.add_option(
        "-d", "--fc-downlink", dest="fc_downlink", type="eng_float", default=eng_notation.num_to_str(938600000),
        help="Set fc_downlink [default=%default]")
    parser.add_option(
        "-u", "--fc-uplink", dest="fc_uplink", type="eng_float", default=eng_notation.num_to_str(938900000),
        help="Set fc_uplink [default=%default]")
    parser.add_option(
        "-g", "--gain-downlink", dest="gain_downlink", type="eng_float", default=eng_notation.num_to_str(40),
        help="Set gain_downlink [default=%default]")
    parser.add_option(
        "-r", "--gain-uplink", dest="gain_uplink", type="eng_float", default=eng_notation.num_to_str(60),
        help="Set gain_uplink [default=%default]")
    parser.add_option(
        "", "--osr", dest="osr", type="intx", default=4,
        help="Set OSR [default=%default]")
    parser.add_option(
        "", "--ppm", dest="ppm", type="eng_float", default=eng_notation.num_to_str(-1),
        help="Set Clock offset correction [default=%default]")
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(13e6/12.0),
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "", "--samp-rate-downlink", dest="samp_rate_downlink", type="eng_float", default=eng_notation.num_to_str(13e6/12.0),
        help="Set samp_rate_downlink [default=%default]")
    parser.add_option(
        "", "--timing-advance", dest="timing_advance", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set timing_advance [default=%default]")
    return parser


def main(top_block_cls=trx_radio_if, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(delay_correction=options.delay_correction, fc_downlink=options.fc_downlink, fc_uplink=options.fc_uplink, gain_downlink=options.gain_downlink, gain_uplink=options.gain_uplink, osr=options.osr, ppm=options.ppm, samp_rate=options.samp_rate, samp_rate_downlink=options.samp_rate_downlink, timing_advance=options.timing_advance)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
