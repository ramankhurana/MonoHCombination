import os
from ROOT import *

os.system('rm data/monoHReweightedSignalShapes.root')

def SubmitJobfunc(mzp, ma0):
    mzp_ = str(mzp)
    ma0_ = str(ma0)
    postname=str(mzp_)+'_'+str(ma0_)
    shellfilename = 'temporary_Res_submit_'+postname+'.sh'
    os.system('rm '+shellfilename)

    
    fileshell = open(shellfilename,'a')
    for linesh in open('Template_submit_batch.sh','r'):
        linesh = linesh.replace('XXX',mzp_)
        linesh = linesh.replace('YYY',ma0_)
        fileshell.write(linesh)
    fileshell.close()
    os.system('chmod 777 '+shellfilename)
    tmpcmnd = 'bsub  -q 8nh '+' '+shellfilename+';'
    command =  tmpcmnd
    
    print command
    os.system(command)
    return 0



time=0
#for imass in open('refined.txt'):
for imass in open('test.txt'):
#for imass in open('zpbaryonicMass_private.txt'):
#for imass in open('zpbaryonicMass_official.txt'):
    mzp = imass.rstrip().split(" ")[0]
    ma0 = imass.rstrip().split(" ")[1]

#for mzp in range(600, 1850, 50):
#    for ma0 in range(300,825,25):
#ZpMass=[600., 800., 1000.,1200.,1400.,1700.,2000.,2500.]
#for imzp in ZpMass:
 #   for ma0 in range (400,450, 100):
        #mzp = int(imzp)
    print "submitting job for ", (mzp, ma0)
    SubmitJobfunc( mzp, ma0)
    time = time + 1 
    if (time%250) == 0:
        os.system('sleep 300')
#SubmitJobfunc( 1000,300)
