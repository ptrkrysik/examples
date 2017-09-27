As input file use vf_call6_a725_d174_g5_Kc1EF00BAB3BAC7002.bursts.bz2 that is located in gr-gsm/test_data directory.
First unzip it with:
bzip2 -d vf_call6_a725_d174_g5_Kc1EF00BAB3BAC7002.bursts.bz2

Then in the "bursts source" set absolute path to the decompressed file.

The file was prepared for USRP B210. For other hardware some changes might have to be applied 
(like changes in subdev spec, adjusting gain or output sample rate to match capabilities of the transmitting device).

If the demo work correctly you should see at the stdout content of decoded messages.

