#!/bin/bash

python ConvertNPYtoDAT.py

python ../kmeans.py -i 00000000.dat -nc 5 -c centers.dat -o membership.dat 
