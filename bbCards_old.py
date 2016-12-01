import sys 
import os 


def MakebbDecision(threshold, Zpmass, A0Massvec):     ## > threshold is boosted analysis
    threshold = float(threshold)
    bb=''
    if float(Zpmass) > threshold:
        bb='boostedHbb/DataCard_S_Plus_B_M'+(str(Zpmassvec[izpmass]))+'_'+A0Massvec+'GeV_MonoHbb_13TeV.txt'
    if float(Zpmass) <= threshold:
        bb='resolvedHbb/ZprimeToA0hToA0chichihbb_2HDM_MZp'+(str(Zpmassvec[izpmass]))+'_MA0'+A0Massvec+'_13TeVmadgraphDatacards/ZprimeToA0hToA0chichihbb_2HDM_MZp'+(str(Zpmassvec[izpmass]))+'_MA0'+A0Massvec+'_13TeVmadgraph_comb_v2.txt'
                
    print (threshold, Zpmass, A0Massvec,bb)
