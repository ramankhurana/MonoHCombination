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
print nargv
print sys.argv[2]
regions=[]
for iargv in range(0,nargv):
    if sys.argv[iargv+2] != 'runlimit':
        if sys.argv[iargv+2] != 'obs':
            regions.append(sys.argv[iargv+2])
    
#regions = ['signal', 'zj', 'wt']

print regions
massvec=['600','800','1000','1200','1400','1700','2000','2500']
a0massvec=['300']#,'400','500','600','700','800']




#os.system('mkdir -p oneplustwo')
for imass in range(len(massvec)):
    for ia0mass in a0massvec:
        datacards={
            'WW': 'WW/Datacards.txt ',
            'gg': 'gg/Datacards.txt ',
            'tt': 'tt/Datacards.txt ',
            'bb': 'bb/Datacards.txt ', 
            'ZZ': 'ZZ/Datacards.txt '
            }
        
        allregions=[]
        for iregion in regions:
            tmpname = iregion+'='+datacards[iregion]
            print (massvec[imass], ia0mass, tmpname)
            allregions.append(tmpname)
        

        allcards = ''.join(allregions)
        print allcards
        splusbFitdir = dirname
        datacardnamefit=splusbFitdir+'/DataCard_2HDM_M'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHCombo_13TeV.txt'
        tmpdcard = 'tmpcard.txt'
        if (len(sys.argv) >= 2) & (not ('runlimit' in sys.argv )) :
            
            print "os.system('combineCards.py  '+allcards+' >& '+tmpdcard)"
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

