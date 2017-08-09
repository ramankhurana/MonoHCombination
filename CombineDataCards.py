import sys 
import os 
if len(sys.argv) < 2 :
    print "insufficient options provided see help function "
    exit (1)

if len(sys.argv) > 1 :
    print ('You are running limits for ')
    for i in range(len(sys.argv)):
        print sys.argv[i]




dirname=sys.argv[1]


nargv = len(sys.argv) -2

regions=[]
for iargv in range(0,nargv):
    if sys.argv[iargv+2] != 'runlimit':
        if sys.argv[iargv+2] != 'obs':
            regions.append(sys.argv[iargv+2])

print 'regions= ', regions

def MakebbDecision(threshold, Zpmass, A0Mass):     ## > threshold is boosted analysis
    threshold = float(threshold)
    bb=''
    print ('float(Zpmass) > threshold', float(Zpmass) > threshold)
    if float(Zpmass) > threshold:
        bb='bb/boostedAK8/DataCard_S_Plus_B_M'+str(Zpmass)+'_'+str(A0Mass)+'GeV_MonoHbb_13TeV.txt'
    if float(Zpmass) <= threshold:
        bb= 'bb/resolved/ZprimeToA0hToA0chichihbb_2HDM_MZp'+str(Zpmass)+'_MA0'+str(A0Mass)+'_13TeVmadgraphDatacards/ZprimeToA0hToA0chichihbb_2HDM_MZp'+str(Zpmass)+'_MA0'+str(A0Mass)+'_13TeVmadgraph_comb_v2.txt '
                
    #print (threshold, Zpmass, A0Mass,bb)
    return bb

massvec=['600','800','1000','1200','1400','1700','2000','2500']
a0massvec=['300']#,'400','500','600','700','800']


for imass in range(len(massvec)):
    for ia0mass in a0massvec:
        datacards={
            ## this string should have trailing space
            'WW': 'WW/datacards/monoH_Alberto_comb/events/datacard_monoHWW'+str(massvec[imass])+'_'+str(ia0mass)+'.txt ',
            'gg': 'gg/DataCard_2HDM_mZP'+str(massvec[imass])+'_mA0'+str(ia0mass)+'.txt ',
            'tt': 'tt/Jul3_CardsForCombo/Zprime'+str(massvec[imass])+'A'+str(ia0mass)+'/cmb/'+str(ia0mass)+'/DataCard_2HDM_M'+str(massvec[imass])+'_'+str(ia0mass)+'GeV_MonoHTauTau_13TeV.txt ',
            'bb': 'bb/datacards_2HDM/ZpA0-'+str(massvec[imass])+'-'+str(ia0mass)+'/combined.txt ',
            'ZZ': 'ZZ/datacards_4l_2016/hhxx_Fall15_card_4l_ZprimeToA0hToA0chichihZZTo4l_2HDM_MZp-'+str(massvec[imass])+'_MA0-'+str(ia0mass)+'_13TeV-madgraph.txt'
            }
        
        allregions=[]
        for iregion in regions:
            datacard_name_ = str(datacards[iregion]).replace(' ','')
            print datacard_name_
            if not bool(os.path.exists(datacard_name_)) : continue
            os.system('cp '+str(datacards[iregion])+' '+str(iregion)+'.txt')
            if (str(iregion) == 'ZZ') | (str(iregion) == 'WW'):
                tmpname = iregion+'='+iregion+'.txt '

            if  (str(iregion) == 'bb') | (str(iregion) == 'gg') | (str(iregion) == 'tt'):
                tmpname = iregion+'='+datacards[iregion]+' '
            
            allregions.append(tmpname)
            
            
        allcards = ''.join(allregions)
        print allcards
        splusbFitdir = dirname
        datacardnamefit=splusbFitdir+'/DataCard_2HDM_M'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHCombo_13TeV.txt'
        tmpdcard = 'tmpcard.txt'
        if (len(sys.argv) >= 2) & (not ('runlimit' in sys.argv )) :
            
            print    ('combineCards.py  -S '+allcards+' >& tmpcard.txt')
            os.system('combineCards.py  -S '+allcards+' >& tmpcard.txt')
            
            
            outcard = open(datacardnamefit,'w')
            card_ = open('tmpcard.txt')

            for line in card_:
                line = line.replace('AnalysisHistograms_MergedSkimmedV12_Puppi_V7', '')
                line = line.replace('DataCards_AllRegions', '')
                outcard.write(line)
            outcard.close()

            #os.system('cat '+tmpdcard+' '+rateparm+' >& '+  datacardnamefit)
            
        nargv = len(sys.argv)
        if sys.argv[nargv-1] == 'runlimit':
            print ('combine -M Asymptotic '+datacardnamefit+' -t -1')
            os.system('combine -M Asymptotic '+datacardnamefit+' -t -1')
            os.system('mv higgsCombineTest.Asymptotic.mH120.root '+dirname+'/higgsCombineTest_Asymptotic_'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHbb_13TeV.root')

        if ((str(sys.argv[nargv-1]) == 'runlimit') & (str(sys.argv[nargv-2]) == 'obs')) | ((str(sys.argv[nargv-2]) == 'runlimit') & (str(sys.argv[nargv-1]) == 'obs')) :
            print ('combine -M Asymptotic '+datacardnamefit)
            os.system('combine -M Asymptotic '+datacardnamefit)
            os.system('mv higgsCombineTest.Asymptotic.mH120.root '+dirname+'/higgsCombineTest_Asymptotic_'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHbb_13TeV.root')

        
        
        '''
        tmpdcard = 'tmpcard.txt'
        dcard = open(datacardname,'r')
        dcardnew = open(tmpdcard ,'w')
        
        for line in dcard:
            line = line.replace(dirname+'/','')
            line = line.replace('kmax 45','kmax 45')
            dcardnew.write(line)
            
            
        dcard.close()
        dcardnew.close()
        

        
        
        print ('combine -M Asymptotic '+datacardnamefit)
        os.system('combine -M Asymptotic '+datacardnamefit)
        os.system('mv higgsCombineTest.Asymptotic.mH120.root '+dirname+'/higgsCombineTest_Asymptotic_'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHbb_13TeV.root')
        '''
    #os.system('mv ')

