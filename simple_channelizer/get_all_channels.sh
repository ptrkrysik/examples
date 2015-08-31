#!/bin/bash

channels="15 16 22 35 36 68 69 70 71 72 73 74 75 76 77 78"

for ch in $channels
do

./get_channel.py -c $ch --samp-rate 25e6

done

