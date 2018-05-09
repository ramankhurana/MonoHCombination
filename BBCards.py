import sys 
import os 

#massvec=['600','800','1000','1200','1400','1700','2000','2500']
#a0massvec=['300','400','500','600','700','800']                                                                                                                                          

import config_combo as cc 
#massvec=['1000']
#a0massvec=['300']


cardspath = 'combocards/bb_2HDM/datacards/'
os.system('ls -1 combocards/bb_2HDM/datacards/*.txt | grep monoHnn_MZ > ' + cc.monohCombo['bbcards2HDM'])

bbcardsfilename=cc.monohCombo['bbcards2HDM']
for icard in open (cc.monohCombo['bbcards2HDM']):
    ## take a backup of the cards
    os.system('cp '+icard.rstrip()+ ' '+ icard.rstrip()+'.bak')
    
    ## change the rate line from 1.000  to 1000.0 
    newcard= icard.rstrip()+'.bak'
    finalcard = icard.rstrip() ## same name as initial card
    fout_ = open(finalcard,'w')
    for iline in open(newcard):
        ## change the rate line from 1.000  to 1000.0 
        if 'rate' in iline:
            #b_  = iline.rstrip().split()[1]
            #bb_ = iline.rstrip().split()[5]
            iline =  iline.replace('1.0000','588.0')

        ## change the rootfile path
        iline = iline.replace('combocards/bb_2HDM/combocards/bb_2HDM/','combocards/bb_2HDM/')
        fout_.write(iline)
    fout_.close()

'''

#os.system('mkdir -p oneplustwo')
for imass in range(len(massvec)):
    for ia0mass in a0massvec:
        
        basename='combocards/bb_2HDM/datacards/monoHnn_MZXXX_MAYYY.txt'

        print basename
        if not bool(os.path.exists(basename)): continue 
        datacards={
            'et':'xtt_et_1_13TeV.txt ',
            'mt':'xtt_mt_1_13TeV.txt ',
            'tt':'xtt_tt_1_13TeV.txt '}
        
        regions = ['et','mt','tt']
        allregions=[]
        for iregion in regions:
            tmpname = iregion+'='+datacards[iregion]
            print (massvec[imass], ia0mass, tmpname)
            allregions.append(tmpname)
        

        allcards = ''.join(allregions)
        print allcards
        splusbFitdir = basename
        #datacardnamefit=splusbFitdir+'/DataCard_2HDM_M'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHTauTau_13TeV.txt'
        datacardnamefit='DataCard_2HDM_M'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHTauTau_13TeV.txt'
        print 'writing datacards', datacardnamefit
        
        # save present path
        c_cw = os.getcwd()
        
        # go to the datacards dir and  combine the cards 
        if not os.path.exists(basename):
            print 'path of tt datacards does not exist'
            quit()
        print "entering dir",basename
        os.chdir(basename)
        os.system ('combineCards.py  '+allcards+' >& tmpcard.txt')
        
        # do some text replacements        
        outcard = open(datacardnamefit,'w')
        card_ = open('tmpcard.txt')
        
        for line in card_:
            line = line.replace('$MASS', str(ia0mass))
            outcard.write(line)
        outcard.close()
        
        #return to the original sirectory
        os.chdir(c_cw)
        


'''
