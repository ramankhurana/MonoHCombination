import sys 
import os 

massvec=['600','800', '1000', '1200', '1400', '1700', '2000', '2500']
a0massvec=['300']




#os.system('mkdir -p oneplustwo')
for imass in range(len(massvec)):
    for ia0mass in a0massvec:
        basename='tt/tt_36fb_update/Zprime'+(str(massvec[imass]))+'A'+ia0mass+'/cmb/'+ia0mass+'/'
        if not bool(os.path.exists(basename)): continue 
        datacards={
            'et':basename+'xtt_et_1_13TeV.txt ',
            'mt':basename+'xtt_mt_1_13TeV.txt ',
            'tt':basename+'xtt_tt_1_13TeV.txt '}
        
        regions = ['et','mt','tt']
        allregions=[]
        for iregion in regions:
            tmpname = iregion+'='+datacards[iregion]
            print (massvec[imass], ia0mass, tmpname)
            allregions.append(tmpname)
        

        allcards = ''.join(allregions)
        print allcards
        splusbFitdir = basename
        datacardnamefit=splusbFitdir+'/DataCard_2HDM_M'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHTauTau_13TeV.txt'
        os.system ('combineCards.py  '+allcards+' >& tmpcard.txt')
        
        print(os.path.exists(basename))
        outcard = open(datacardnamefit,'w')
        card_ = open('tmpcard.txt')
        
        for line in card_:
            line = line.replace('$MASS', str(ia0mass))
            outcard.write(line)
        outcard.close()
        os.system('combine -M Asymptotic '+datacardnamefit+' -t -1')
        os.system('mv higgsCombineTest.Asymptotic.mH120.root higgsCombineTest_Asymptotic_'+(str(massvec[imass]))+'_300GeV_MonoHbb_13TeV.root')

'''
massvec=['500','1000']
a0massvec=['1', '150', '500', '1000']

for imass in range(len(massvec)):
    for ia0mass in a0massvec:
        basename='tt/tt_36fb_update/Baryonic'+(str(massvec[imass]))+'A'+ia0mass+'/cmb/'+ia0mass+'/'
        if not bool(os.path.exists(basename)): continue 
        datacards={
            'et':basename+'xtt_et_1_13TeV.txt ',
            'mt':basename+'xtt_mt_1_13TeV.txt ',
            'tt':basename+'xtt_tt_1_13TeV.txt '}
        
        regions = ['et','mt','tt']
        allregions=[]
        for iregion in regions:
            tmpname = iregion+'='+datacards[iregion]
            print (massvec[imass], ia0mass, tmpname)
            allregions.append(tmpname)
        

        allcards = ''.join(allregions)
        print allcards
        splusbFitdir = basename
        datacardnamefit=splusbFitdir+'/DataCard_ZpB_M'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHTauTau_13TeV.txt'
        os.system ('combineCards.py  '+allcards+' >& tmpcard.txt')
        
        print(os.path.exists(basename))
        outcard = open(datacardnamefit,'w')
        card_ = open('tmpcard.txt')
        
        for line in card_:
            line = line.replace('$MASS', str(ia0mass))
            outcard.write(line)
        outcard.close()
'''
