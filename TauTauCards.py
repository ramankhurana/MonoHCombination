import sys 
import os 
import optparse 
#massvec=['600','800','1000','1200','1400','1700','2000','2500']
#a0massvec=['300','400','500','600','700','800']                                                                                                                                          
usage = "usage: %prog [options] "
parser = optparse.OptionParser(usage)

#massvec=['1000']
#a0massvec=['300']

parser.add_option("-t", "--thdm", action="store_true", dest="thdm")
parser.add_option("-b", "--zpb", action="store_true", dest="zpb")

(options, args) = parser.parse_args()


#mzp_ = []
#mdm_ = []
#
#for iline in open("bin/tautauZpBAll.txt"):
#    mzp_.append(iline.rstrip().split()[0])
#    mdm_.append(iline.rstrip().split()[1])
#
#    
#print mzp_ 
#print mdm_    
#

#for imass in range(450,4050,50):
#    for ia0mass in range(300,1025,25):
for imass in (1,10,20,50):
    for ia0mass in (1, 10):
        basename=''
        if options.thdm:
            basename='combocards/MB_2HDM_tt/Zprime'+(str(imass))+'A'+str(ia0mass)+'/cmb/'+str(ia0mass)+'/'
        
        if options.zpb:
            basename='combocards/MB_ZpB_tt/Baryonic'+(str(imass))+'A'+str(ia0mass)+'/cmb/'+str(ia0mass)+'/'
        
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
            print (imass, ia0mass, tmpname)
            allregions.append(tmpname)
        

        allcards = ''.join(allregions)
        print allcards
        splusbFitdir = basename
        #datacardnamefit=splusbFitdir+'/DataCard_2HDM_M'+(str(imass))+'_'+ia0mass+'GeV_MonoHTauTau_13TeV.txt'
        datacardnamefit=''
        if options.thdm:
            datacardnamefit='DataCard_2HDM_M'+(str(imass))+'_'+str(ia0mass)+'GeV_MonoHTauTau_13TeV.txt'
        if options.zpb:
            datacardnamefit='DataCard_ZpB_M'+(str(imass))+'_'+str(ia0mass)+'GeV_MonoHTauTau_13TeV.txt'

        print 'writing datacards', datacardnamefit
        
        # save present path
        c_cw = os.getcwd()
        
        # go to the datacards dir and  combine the cards 
        if not os.path.exists(basename):
            print 'path of tt datacards does not exist'
            quit()
        print "entering dir",basename
        os.chdir(basename)
        
        print ('combineCards.py  '+allcards+' >& tmpcard.txt')
        os.system ('combineCards.py  '+allcards+' >& tmpcard.txt')
        #os.system ('combineCards.py  '+allcards+' ')
        
        # do some text replacements        
        outcard = open(datacardnamefit,'w')
        card_ = open('tmpcard.txt')
        
        
        print datacardnamefit
        
        for line in card_:
            line = line.replace('$MASS', str(ia0mass))
            outcard.write(line)
        outcard.close()
        
        #return to the original sirectory
        os.chdir(c_cw)
        



'''
for imass in range(len(massvec)):
    for ia0mass in a0massvec:
        basename='tt/tt_36fb_update/Baryonic'+(str(imass))+'A'+ia0mass+'/cmb/'+ia0mass+'/'
        if not bool(os.path.exists(basename)): continue 
        datacards={
            'et':basename+'xtt_et_1_13TeV.txt ',
            'mt':basename+'xtt_mt_1_13TeV.txt ',
            'tt':basename+'xtt_tt_1_13TeV.txt '}
        
        regions = ['et','mt','tt']
        allregions=[]
        for iregion in regions:
            tmpname = iregion+'='+datacards[iregion]
            print (imass, ia0mass, tmpname)
            allregions.append(tmpname)
        

        allcards = ''.join(allregions)
        print allcards
        splusbFitdir = basename
        datacardnamefit=splusbFitdir+'/DataCard_ZpB_M'+(str(imass))+'_'+ia0mass+'GeV_MonoHTauTau_13TeV.txt'
        os.system ('combineCards.py  '+allcards+' >& tmpcard.txt')
        
        print(os.path.exists(basename))
        outcard = open(datacardnamefit,'w')
        card_ = open('tmpcard.txt')
        
        for line in card_:
            line = line.replace('$MASS', str(ia0mass))
            outcard.write(line)
        outcard.close()
'''
