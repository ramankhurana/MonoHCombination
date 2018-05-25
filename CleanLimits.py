import os
import sys 
#fout = open('bin/limits_2hdm_combo_scaled_cleaned.txt','w')
#for iline in open('bin/limits_2hdm_combo_scaled.txt'):

fout = open('bin/limits_zpb_combo_cleaned.txt','w')
for iline in open('bin/limits_zpb_combo.txt'):
    lineList = iline.rstrip().split()
    if len(lineList) == 8:
        fout.write(iline)
fout.close()

    
