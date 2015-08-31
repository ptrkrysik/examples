def get_freqs_from_arfcns(arfcns,region):
    freqs = {}
    for ii in xrange(0,len(arfcns)):
        arfcns[ii] = get_freq_from_arfcn(arfcns[ii],region)
    
    return arfcns

def get_arfcns_from_freqs(freqs,region):
    arfcns = {}
    for ii in xrange(0,len(freqs)):
        arfcns[ii] = get_arfcn_from_freq(freqs[ii],region)
    
    return arfcns

def get_freq_from_arfcn(chan,region):
    #P/E/R-GSM 900
    if chan >= 1 and chan <= 124:
        freq = 890 + 0.2*chan + 45

    #GSM 850
    elif chan >= 128 and chan <= 251:
        freq = 824.2 + 0.2*(chan - 128) + 45
        
    #GSM 450
    elif chan >= 259 and chan <= 293:
        freq = 450.6 + 0.2*(chan - 259) + 10
        
    #GSM 480
    elif chan >= 306 and chan <= 340:
        freq = 479 + 0.2*(chan - 306) + 10
        
    #DCS 1800
    elif region is "e" and chan >= 512 and chan <= 885:
        freq = 1710.2 + 0.2*(chan - 512) + 95
        
    #DCS 1900
    elif region is "u" and chan >= 512 and chan <= 810:
        freq = 1850.2 + 0.2*(chan - 512) + 80

    #E/R-GSM 900
    elif chan >= 955 and chan <= 1024:
        freq = 890 + 0.2*(chan - 1024) + 45

    else:
        freq = 0

    return freq * 1e6

def get_arfcn_from_freq(freq,region):
    freq = freq / 1e6
    # GSM 450
    if freq <= 450.6 + 0.2*(293 - 259) + 10:
        arfcn = ((freq - (450.6 + 10)) / 0.2) + 259
    # GSM 480
    elif freq <= 479 + 0.2*(340 - 306) + 10:
        arfcn = ((freq - (479 + 10)) / 0.2) + 306
    # GSM 850
    elif freq <= 824.2 + 0.2*(251 - 128) + 45:
        arfcn = ((freq - (824.2 + 45)) / 0.2) + 128
    #E/R-GSM 900
    elif freq <= 890 + 45 and freq >=920:
        arfcn = ((freq - (890 + 45)) / 0.2) + 1023
    # GSM 900
    elif freq <= 890 + 0.2*124 + 45:
        arfcn = (freq - (890 + 45)) / 0.2
    else:
        if region is "u":
            if freq > 1850.2 + 0.2*(810 - 512) + 80:
                arfcn = 0;
            else:
                arfcn = (freq - (1850.2 + 80)) / 0.2 + 512
        elif region is "e":
            if freq > 1710.2 + 0.2*(885 - 512) + 95:
                arfcn = 255;
            else:
                arfcn = (freq - (1710.2 + 95) ) / 0.2 + 512
        else:
            arfcn = 255

    if arfcn<0:
        return 255
    else:
        return int(round(arfcn))
