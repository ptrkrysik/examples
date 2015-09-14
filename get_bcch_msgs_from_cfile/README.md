This program processes files containing complex data - interleaved float IQ samples. 
To generate python file that can be used from commandline do:

grcc get_bcch_msgs_from_cfile.grc -d .

Example of the usage:
get_bcch_msgs_from_cfile.py --samp-rate=1M --fc=940M -i input_file 

where:

--samp-rate - sampling frequency of the data stored in the file,
--fc - central frequency of the recorded data - it is needed for frequency offset correction,
-i - the file containing the complex data.
