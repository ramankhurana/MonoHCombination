import os
import sys



def ListToStr(list_):
    str_ = ""
    for i, iele in enumerate(list_):
        str_ = str_ + iele 
        if (i<len(list_)-1): str_ = str_ + " "
        if (i==len(list_)-1): str_ = str_ + "\n"
    print str(str_ )
    return str(str_ )
def sortlimits(limitfile):
    fin = open(limitfile)
    limits=[]
    
    for iline in fin:
        a = iline.rstrip().split()
        limits.append(a)
        
    limits_sorted = sorted(limits, key=lambda element: int(element[0]))
    
    fout = open(limitfile.replace(".txt", "_sorted.txt"),'w')
    for iline in limits_sorted:
        iline_str = ListToStr(iline)
        fout.write(iline_str)


textfiles = []
textfiles.append("bin/plotsLimitcombo2hdm/limits_2hdm_combo.txt")
textfiles.append("bin/plotsLimitcombo2hdm/limits_2hdm_bb.txt")
textfiles.append("bin/plotsLimitcombo2hdm/limits_2hdm_gg.txt")
textfiles.append("bin/plotsLimitcombo2hdm/limits_2hdm_tt.txt")
textfiles.append("bin/plotsLimitcombo2hdm/limits_2hdm_ww.txt")
'''
#textfiles.append("bin/plotsLimitcombo2hdm/limits_2hdm_zz.txt") this is for ZZ
textfiles.append("bin/plotsLimitcombozpb/limits_zpb_combo.txt")
textfiles.append("bin/plotsLimitcombozpb/limits_zpb_bb.txt")
textfiles.append("bin/plotsLimitcombozpb/limits_zpb_gg.txt")
textfiles.append("bin/plotsLimitcombozpb/limits_zpb_tt.txt")
textfiles.append("bin/plotsLimitcombozpb/limits_zpb_ww.txt")
#textfiles.append("bin/plotsLimitcombozpb/limits_zpb_zz.txt") this is for ZZ
'''
for itextfile in textfiles:
    sortlimits(itextfile)
