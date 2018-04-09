import os 
import sys, optparse

usage = "usage: %prog [options] "
parser = optparse.OptionParser(usage)

parser.add_option("-c", "--combine",  action="store_true",  dest="combine")
parser.add_option("-r", "--runcombo", action="store_true",  dest="runcombo")
parser.add_option("-T", "--runtt", action="store_true",  dest="runtt")
parser.add_option("-W", "--runww", action="store_true",  dest="runww")
parser.add_option("-G", "--rungg", action="store_true",  dest="rungg")
parser.add_option("-B", "--runbb", action="store_true",  dest="runbb")
parser.add_option("-I", "--runImpact", action="store_true",  dest="runImpact")
parser.add_option("-P", "--runPull", action="store_true",  dest="runPull")
parser.add_option("-S", "--submitJobs", action="store_true",  dest="submitJobs")
(options, args) = parser.parse_args()

## User Utility 
import config_combo as cc


def PrintAvailabilityStatus():
    textOut = open(cc.monohCombo['statusAll2HDM'],'w')
    firstline = 'mzp mdm gg ww tt bb \n'
    textOut.write(firstline)
    comboCardstxt = open(cc.monohCombo['combocards2HDM'],'w')
    gg2hdmCardstxt = open(cc.monohCombo['ggcards2HDM'],'w')
    tt2hdmCardstxt = open(cc.monohCombo['ttcards2HDM'],'w')
    ww2hdmCardstxt = open(cc.monohCombo['wwcards2HDM'],'w')
    bb2hdmCardstxt = open(cc.monohCombo['bbcards2HDM'],'w')
    for imass in open(cc.monohCombo['FSmasspoints2HDM']):
        gg_ = cc.monohCombo['ggpath2HDM'] + cc.monohCombo['gg_cardname2HDM']
        ww_ = cc.monohCombo['wwpath2HDM']+ cc.monohCombo['ww_cardname2HDM']
        tt_ = cc.monohCombo['tautaupath2HDM']+ cc.monohCombo['tautau_cardname2HDM']
        bb_ = cc.monohCombo['bbpath2HDM']+ cc.monohCombo['bb_cardname2HDM']
        
        x_ = imass.rstrip().split()[0]
        y_ = imass.rstrip().split()[1]
        
        print "running code for ", x_, y_
    ## gg
        gg_ = gg_.replace('XXX',x_).replace('YYY',y_)
        ggstatus_=True
        if not bool(os.path.exists(gg_)): 
            print gg_, 'does not exist'
            ggstatus_ = False
    ## ww
        ww_ = ww_.replace('XXX',x_).replace('YYY',y_)
        wwstatus_=True
        if not bool(os.path.exists(ww_)): 
            wwstatus_= False
            print ww_, 'does not exist'
            
    ## tautu
        tt_ = tt_.replace('XXX',x_).replace('YYY',y_)
        ttstatus_=True
        if not bool(os.path.exists(tt_)):
            ttstatus_=False
            print tt_, 'does not exist'
        

        bb_ = bb_.replace('XXX',x_).replace('YYY',y_)
        bbstatus_=True
        if not bool(os.path.exists(bb_)):
            bbstatus_=False
            print bb_, 'does not exist'

        iline = x_ + ' ' + y_ + ' '+ str(ggstatus_)  + ' ' + str(wwstatus_)  +' '+ str(ttstatus_)  +' '+ str(bbstatus_) + '\n'
        
        textOut.write(iline)
        print iline
        ## if all final state has the datacards then create the combine datacard
        outCardname = cc.monohCombo['combocardname2HDM']
        outCardname = outCardname.replace('XXX',x_).replace('YYY',y_)
        if (bool(ggstatus_) & bool(wwstatus_) & bool(ttstatus_) & bool(bbstatus_)):
            
            print 'status = ', bool(ggstatus_), bool(wwstatus_), bool(ttstatus_), bool(bbstatus_)
            ## write individual cards iff all of them are present, otherwise there is no use of running these cards. 
            gg2hdmCardstxt.write(gg_+'\n')
            tt2hdmCardstxt.write(tt_+'\n')
            ww2hdmCardstxt.write(ww_+'\n')
            bb2hdmCardstxt.write(bb_+'\n')
            
            prestr = 'combineCards.py '
            ggstr = 'gg=' + gg_ + ' '
            wwstr = 'ww=' + ww_ + ' '
            ttstr = 'tt=' + tt_ + ' '
            bbstr = 'bb=' + bb_ + ' '
            poststr = ' > '+ outCardname
            comboStr = prestr + ggstr + wwstr + ttstr + bbstr + poststr
            os.system(comboStr)
            
        ## Fix the lines related to WW
            tmp_outCardname = outCardname+'.bak'
            os.system('cp '+outCardname + ' ' + tmp_outCardname)
            combocard = open(outCardname,'w')
            for idline in open(tmp_outCardname):
                idline = idline.replace("combocards/datacards_combination/monoH_MVA_em/muccamva2HDMadaptFull_All_Bin800", "combocards/")
            ## File the line related to bb 2HDM 
                idline = idline.replace("combocards/bb_2HDM/datacards/combocards/bb_2HDM/","combocards/bb_2HDM/")
                combocard.write(idline)
            combocard.close()
            comboCardstxt.write(outCardname+'\n')


    textOut.close() ## close if one line has been written. Close it outside for loop
    comboCardstxt.close()
    return 0


def ExtractLimits(logfile):
    for ilongline in open(logfile):
        if "Observed Limit: r < " in ilongline:
            observed_ = ilongline.replace("Observed Limit: r < ","")
        if "Expected  2.5%: r < " in ilongline:
            expected25_ = ilongline.replace("Expected  2.5%: r < ","")
        if "Expected 16.0%: r < " in ilongline:
            expected16_ = ilongline.replace("Expected 16.0%: r < ","")
        if "Expected 50.0%: r < " in ilongline:
            expected50_ = ilongline.replace("Expected 50.0%: r < ","")
        if "Expected 84.0%: r < " in ilongline:
            expected84_ = ilongline.replace("Expected 84.0%: r < ","")
        if "Expected 97.5%: r < " in ilongline:
            expected975_ = ilongline.replace("Expected 97.5%: r < ","")
    return [expected25_, expected16_, expected50_, expected84_, expected975_]

    
def RunLimits(cardList):
    
    ## if code has to be run locally
    ## no jobs will be submitted 
    print "running the limits for cards inside ", cardList
    for icard in open(cardList):
        if options.submitJobs is None: 
            print "the limits will be running in interactive mode, no jobs will be submitted. " 
            
            # prepare the name of log file
            logfile = icard.rstrip().split("/")[-1]
            logfile = 'bin/temp_'+logfile+'.log'
            
            # prepare the command
            command_  = 'combine -M Asymptotic '+icard.rstrip()+' | tee '+logfile
            
            # run it
            os.system(command_)
            
            # extract limit in oe line to fill the text file.
            limits = ExtractLimits(logfile)
            print icard, limits
            
        
        ## if one ask to submit the job for a given datacard list. 
        if options.submitJobs:
            print "submitting batch jobs for cards listed in ", cardList
            SubmitBatchJobs(icard.rstrip())
            
            ## impact willl be run only in the batch mode
            if options.runImpact:
                print "Running impacts for this mass point."
        
            ## pulls will be run only in the batch mode
            if options.runPull:
                print "Runnign pulls for this mass point."



def SubmitBatchJobs(cardname):
    print "routine to submit batch job has been called. "
    print "one job for each data card will be submitted now"
    print "submitting jobs for ", cardname 
    SubmitJobfunc(cardname)
    



def SubmitJobfunc(cardname):
    tempshell='''
#!/bin/sh                                                                                                                                                                           
export SCRAM_ARCH=slc6_amd64_gcc491
currentpath=$PWD
cd /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_7/src/
eval `scram runtime -sh`
cd /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/
/afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/scan.sh DATACARDNAME
'''
    shellfilename = 'temporary_'+cardname.rstrip().split("/")[-1].replace(".txt",".sh")
    
    if bool(os.path.exists(shellfilename)):
        os.system('rm '+shellfilename)
        
    fileshell = open(shellfilename,'w')
    tempshell = tempshell.replace("DATACARDNAME",cardname)
    fileshell.write(tempshell)
    
    #pwd_ = os.getcwd()
    #os.chdir(pwd_ + '/shcards')
    os.system('chmod 777 '+shellfilename)
    tmpcmnd = 'bsub  -q 8nh '+' '+shellfilename+';'
    command =  tmpcmnd
    
    print command
    os.system(command)
    #os.chdir(pwd_)
    return 0


        
    

if __name__ == "__main__":
    
        
    if options.combine:
        PrintAvailabilityStatus()
    
    if options.runcombo:
        RunLimits(cc.monohCombo['combocards2HDM'])
    
    if options.rungg:
        RunLimits(cc.monohCombo['ggcards2HDM'])

    if options.runtt:
        RunLimits(cc.monohCombo['ttcards2HDM'])

    if options.runww:
        RunLimits(cc.monohCombo['wwcards2HDM'])

    if options.runbb:
        RunLimits(cc.monohCombo['bbcards2HDM'])

                
# python  RunCombo.py -c -r -B -W -T -G -I -P 
