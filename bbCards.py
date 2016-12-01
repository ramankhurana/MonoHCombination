import sys 
import os 

massvec=['600','800','1000','1200','1400','1700','2000','2500']
a0massvec=['300','400','500','600','700','800']
basename = 'bb/combined'



#os.system('mkdir -p oneplustwo')
for imass in range(len(massvec)):
    for ia0mass in a0massvec:
        basename_res='bb/resolved/ZprimeToA0hToA0chichihbb_2HDM_MZp'+(str(massvec[imass]))+'_MA0'+str(ia0mass)+'_13TeVmadgraphDatacards/ZprimeToA0hToA0chichihbb_2HDM_MZp'+(str(massvec[imass]))+'_MA0'+str(ia0mass)+'_13TeVmadgraph_comb_v2.txt'
        basename_boost='bb/boostedAK8/DataCard_S_Plus_B_M'+(str(massvec[imass]))+'_'+str(ia0mass)+'GeV_MonoHbb_13TeV.txt'
        
        print basename_res
        print basename_boost
        if not bool(os.path.exists(basename_res)): continue 
        if not bool(os.path.exists(basename_boost)): continue 
        
        datacards={
            'res': basename_res+' ',
            'boost': basename_boost+' '}
        
        regions = ['res','boost']
        allregions=[]
        for iregion in regions:
            tmpname = iregion+'='+datacards[iregion]
            print (massvec[imass], ia0mass, tmpname)
            allregions.append(tmpname)
        

        allcards = ''.join(allregions)
        print allcards
        splusbFitdir = basename
        datacardnamefit=splusbFitdir+'/DataCard_2HDM_M'+(str(massvec[imass]))+'_'+ia0mass+'GeV_MonoHbb_13TeV.txt'
        os.system ('combineCards.py  '+allcards+' >& tmpcard.txt')
        
        outcard = open(datacardnamefit,'w')
        card_ = open('tmpcard.txt')
        
        for line in card_:
            line = line.replace('DataCards_AllRegions', '')
            outcard.write(line)
        outcard.close()
