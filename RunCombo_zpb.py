import os 
import sys, optparse

usage = "usage: %prog [options] "
parser = optparse.OptionParser(usage)

parser.add_option(      "--myhelp", action="store_true", dest="myhelp")
parser.add_option("-t", "--thdm", action="store_true", dest="thdm")
parser.add_option("-b", "--zpb", action="store_true", dest="zpb")
parser.add_option("-c", "--combine",  action="store_true",  dest="combine")
parser.add_option("-r", "--runcombo", action="store_true",  dest="runcombo")

parser.add_option("-T", "--runtt", action="store_true",  dest="runtt")
parser.add_option("-W", "--runww", action="store_true",  dest="runww")
parser.add_option("-G", "--rungg", action="store_true",  dest="rungg")
parser.add_option("-B", "--runbb", action="store_true",  dest="runbb")
parser.add_option("-Z", "--runzz", action="store_true",  dest="runzz")

parser.add_option(      "--runbbgg", action="store_true",  dest="runbbgg")
parser.add_option(      "--runbbtt", action="store_true",  dest="runbbtt")
parser.add_option(      "--runbbww", action="store_true",  dest="runbbww")
parser.add_option(      "--runggtt", action="store_true",  dest="runggtt")
parser.add_option(      "--runggww", action="store_true",  dest="runggww")
parser.add_option(      "--runttww", action="store_true",  dest="runttww")
parser.add_option(      "--runbbggtt", action="store_true",  dest="runbbggtt")
parser.add_option(      "--runbbggttww", action="store_true",  dest="runbbggttww")


parser.add_option("-I", "--runImpact", action="store_true",  dest="runImpact")
parser.add_option("-P", "--runPull", action="store_true",  dest="runPull")
parser.add_option("-S", "--submitJobs", action="store_true",  dest="submitJobs")


parser.add_option("--scalelimits", action="store_true", dest="scalelimits")
parser.add_option("--scalegglimits", action="store_true", dest="scalegglimits")
parser.add_option("--scalebblimits", action="store_true", dest="scalebblimits")
parser.add_option("--scalewwlimits", action="store_true", dest="scalewwlimits")
parser.add_option("--scalettlimits", action="store_true", dest="scalettlimits")

parser.add_option("--oned", action="store_true", dest="oned")
parser.add_option("--SI", action="store_true", dest="SI")


(options, args) = parser.parse_args()



if options.myhelp:
    helpmessage='''
-c, --combine:        combine datacards. This will also produce text files for each final state listing the available mass points. 
                      The available mass points for combination is also listed in the text file. The list of combined datacards are 
                      also prepare in a text file which will be used later for running the combination. 

-r, --runcombo:       Run the combine datacards. The list of datacards are in the already in bin/.txt file. 

-T, --runtt:          Run only tau tau limits 

-W, --runww:          Run only WW limits 

-G, --rungg:          Run only gamma gamma limits

-B, --runbb:          Run only bbbar limits

-I, --runImpact:      Run impacts also 

-P, --runPull:        Run the pulls also 

-S, --submitJobs:     Submit the jobs on lxplus batch system. 

--scalelimits:        scale the limits with theory cross-section value stored in crosssection text file in the bin. 

--scalegglimits:      scale gamma gamma limits 

--scalebblimits:      scale bbbar limits 

--scalewwlimits:      scale ww limits

--scalettlimits:      scale tau tau limits

'''

    print helpmessage



## User Utility 
import config_combo as cc




model_ = ""
if options.thdm:     model_ =  "2HDM"
if options.zpb:      model_ =  "ZPB"


print "combination is now running for ", model_
formatters = {             
    'red': '\033[91m',     
    'green': '\033[92m',   
    'black':'\033[30m',
    'green':'\033[32m',
    'orange':'\033[33m',
    'blue':'\033[34m',
    'purple':'\033[35m',
    'cyan':'\033[36m',
    'lightgrey':'\033[37m',
    'darkgrey':'\033[90m',
    'lightred':'\033[91m',
    'lightgreen':'\033[92m',
    'yellow':'\033[93m',
    'lightblue':'\033[94m',
    'pink':'\033[95m',
    'lightcyan':'\033[96m',
    'END': '\033[0m',
    'end': '\033[0m',
    }


def PrintAvailabilityStatus():
    textOut = open(cc.monohCombo['statusAll'+model_],'w')
    firstline = 'mzp mdm gg ww tt bb \n'
    textOut.write(firstline)
    
    
    comboCardstxt = open(cc.monohCombo['combocards'+model_],'w')
    gg2hdmCardstxt = open(cc.monohCombo['ggcards'+model_],'w')
    tt2hdmCardstxt = open(cc.monohCombo['ttcards'+model_],'w')
    ww2hdmCardstxt = open(cc.monohCombo['wwcards'+model_],'w')
    bb2hdmCardstxt = open(cc.monohCombo['bbcards'+model_],'w')
    #for imass in open(cc.monohCombo['FSmasspoints2HDM']):
    for imass in open(cc.monohCombo['allAvailable'+model_]):
        print "                        "
        print "                        "
        print ("{blue}-----------------------------------------------------------------------------------{END}".format(**formatters))
        print ("{blue}--------                                                                     ------{END}".format(**formatters))
        print ("--------                          "+ imass.rstrip() + "                                    ------")
        print ("{blue}--------                                                                     ------{END}".format(**formatters))
        print ("{blue}-----------------------------------------------------------------------------------{END}".format(**formatters))
        
        gg_ = cc.monohCombo['ggpath'+model_] + cc.monohCombo['gg_cardname'+model_]
        ww_ = cc.monohCombo['wwpath'+model_]+ cc.monohCombo['ww_cardname'+model_]
        tt_ = cc.monohCombo['tautaupath'+model_]+ cc.monohCombo['tautau_cardname'+model_]
        bb_ = cc.monohCombo['bbpath'+model_]+ cc.monohCombo['bb_cardname'+model_]
        
        x_ = imass.rstrip().split()[0]
        y_ = imass.rstrip().split()[1]
        
        print "running code for ", x_, y_
    ## gg
        gg_ = gg_.replace('XXX',x_).replace('YYY',y_)
        ggstatus_=True
        if not bool(os.path.exists(gg_)): 
            print gg_, '{red}does not exist{END}'.format(**formatters)
            ggstatus_ = False


    ## ww
        ww_ = ww_.replace('XXX',x_).replace('YYY',y_)
        wwstatus_=True

        if not bool(os.path.exists(ww_)): 
            wwstatus_= False
            print ww_, '{red}does not exist{end}'.format(**formatters)
        
        if bool(os.path.exists(ww_)): 
        ## remove auto stats from WW cards from now. 
            tmp_ww_ = ww_+'.bak'
            os.system('cp '+ww_ + ' ' + tmp_ww_)
            tmp_ww_card_ = open(tmp_ww_,'w')
            for idline in open(ww_):
                ## mc stats are not working with present setup 
                #idline = idline.replace("* autoMCStats", "#* autoMCStats")
                tmp_ww_card_.write(idline)
                
            tmp_ww_card_.close()
            os.system('cp '+tmp_ww_ + ' ' + ww_)
            


    ## tautu
        tt_ = tt_.replace('XXX',x_).replace('YYY',y_)
        ttstatus_=True
        if not bool(os.path.exists(tt_)):
            ttstatus_=False
            print tt_, '{red}does not exist{end}'.format(**formatters)
        

        bb_ = bb_.replace('XXX',x_).replace('YYY',y_)
        bbstatus_=True
        if not bool(os.path.exists(bb_)):
            bbstatus_=False
            print bb_, '{red}does not exist{end}'.format(**formatters)
            #print bb_, '{red} does not exist {end}'.format(**formatters)

        iline = x_ + ' ' + y_ + ' '+ str(ggstatus_)  + ' ' + str(wwstatus_)  +' '+ str(ttstatus_)  +' '+ str(bbstatus_) + '\n'
        
        textOut.write(iline)
        print iline
        ## if all final state has the datacards then create the combine datacard
        outCardname = cc.monohCombo['combocardname'+model_]
        outCardname = outCardname.replace('XXX',x_).replace('YYY',y_)
        ## general conditiona, combine irrespective of other final states, e.g. if only one of them is missing. But bb should be present. 
        cond1 = (bool(ggstatus_) & bool(wwstatus_) & bool(ttstatus_) & bool(bbstatus_))
        cond2 = (not (bool(ggstatus_))) & bool(wwstatus_) & bool(ttstatus_) & bool(bbstatus_)
        cond3 = (bool(ggstatus_) & (not bool(wwstatus_)) & bool(ttstatus_) & bool(bbstatus_))
        cond4 = (bool(ggstatus_) & bool(wwstatus_) & (not bool(ttstatus_)) & bool(bbstatus_))
        
        ## when mzp is < 800 then bb is not important 
        cond5 = bool (float(x_)<800) & (bool(ggstatus_) & bool(wwstatus_) & bool(ttstatus_))
        cond6 = bool (float(x_)<800) & (bool(ggstatus_) & bool(wwstatus_) & (not bool(ttstatus_)))
        cond7 = bool (float(x_)<800) & (not bool(ggstatus_)) & bool(wwstatus_) & bool(ttstatus_)

        ## for very high masses consider only bb
        cond8 = bool (float(x_)>2500) &  (bool(bbstatus_))
        cond9 = bool (float(y_)>800)  &  (bool(bbstatus_))

        cond10 = bool (float(x_)<600) & (bool(ggstatus_) & bool(ttstatus_) & (not bool(wwstatus_) ) )
        cond11 = bool (float(x_)<600) & (bool(ggstatus_) & (not bool(ttstatus_))  & (not bool(wwstatus_) ) )
        cond12 = bool (float(x_)<600) & (not bool(ggstatus_)) & (bool(ttstatus_)  & (not bool(wwstatus_) ) )

        ## adding WW also
        cond13 = bool (float(x_)<600) & (bool(ggstatus_) & bool(ttstatus_)  & bool(wwstatus_)  )
        cond14 = bool (float(x_)<600) & (bool(ggstatus_) & (not bool(ttstatus_))  & bool(wwstatus_) )
        cond15 = bool (float(x_)<600) & (not bool(ggstatus_)) & (bool(ttstatus_)  & bool(wwstatus_) )

        cond16 = bool (options.zpb)
        print cond1 , cond2 , cond3 , cond4 , cond5 , cond6 , cond7 , cond8 , cond9 , cond10 , cond11 , cond12 , cond13 , cond14 , cond15
        
        #if (bool(ggstatus_) & bool(wwstatus_) & bool(ttstatus_) & bool(bbstatus_)):
        if cond1 | cond2 | cond3 | cond4 | cond5 | cond6 | cond7 | cond8 | cond9 | cond10 | cond11 | cond12 | cond13 | cond14 | cond15 | cond16 :
            
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
            comboStr = ''
            
            if cond1:     comboStr = prestr + ggstr + wwstr + ttstr + bbstr + poststr
            if cond2:     comboStr = prestr         + wwstr + ttstr + bbstr + poststr
            if cond3:     comboStr = prestr + ggstr         + ttstr + bbstr + poststr
            if cond4:     comboStr = prestr + ggstr + wwstr         + bbstr + poststr
            if cond5:     comboStr = prestr + ggstr + wwstr + ttstr +         poststr
            if cond6:     comboStr = prestr + ggstr + wwstr +                 poststr
            if cond7:     comboStr = prestr +         wwstr + ttstr +         poststr
            if cond8:     comboStr = prestr +                         bbstr + poststr
            if cond9:     comboStr = prestr +                         bbstr + poststr
            if cond10:    comboStr = prestr + ggstr +         ttstr         + poststr
            if cond11:    comboStr = prestr + ggstr                         + poststr
            if cond12:    comboStr = prestr +       +         ttstr         + poststr
            if cond13:    comboStr = prestr + ggstr + wwstr + ttstr         + poststr
            if cond14:    comboStr = prestr + ggstr + wwstr                 + poststr
            if cond15:    comboStr = prestr +         wwstr + ttstr         + poststr

            
            if cond16:    comboStr = prestr + ggstr + wwstr + ttstr + bbstr + poststr
            #comboStr = prestr + ggstr + wwstr + ttstr + bbstr + poststr
            
            ''' various options in which this combination can run on ''' 
            ''' this will make the cards and then later can be run using -r option for any combination '''

            if options.rungg:                   comboStr = prestr + ggstr +  poststr
            if options.runww:                   comboStr = prestr + wwstr +  poststr
            if options.runtt:                   comboStr = prestr + ttstr +  poststr
            if options.runbb:                   comboStr = prestr + bbstr +  poststr
            
            if options.runbbgg:                 comboStr = prestr + bbstr +  ggstr +  poststr
            if options.runbbtt:                 comboStr = prestr + bbstr +  ttstr +  poststr
            if options.runbbww:                 comboStr = prestr + bbstr +  wwstr +  poststr
            if options.runggtt:                 comboStr = prestr + ggstr +  ttstr +  poststr
            if options.runggww:                 comboStr = prestr + ggstr +  wwstr +  poststr
            if options.runttww:                 comboStr = prestr + ttstr +  wwstr +  poststr
            if options.runbbggtt:               comboStr = prestr + bbstr +  ggstr +  ttstr +  poststr
            if options.runbbggttww:             comboStr = prestr + bbstr +  ggstr +  ttstr + wwstr +  poststr
            
            
            
            print "comboStr ", comboStr
            os.system(comboStr)
            
        ## Fix the lines related to WW
            tmp_outCardname = outCardname+'.bak'
            os.system('cp '+outCardname + ' ' + tmp_outCardname)
            combocard = open(outCardname,'w')
            for idline in open(tmp_outCardname):
                ## mc stats are not working with present setup 
            
                if options.thdm:
                    #idline = idline.replace("* autoMCStats", "#* autoMCStats")
                    idline = idline.replace("combocards/datacards_combination/monoH_MVA_em/muccamva2HDMadaptFull_All_Bin800", "combocards/")
                    ## File the line related to bb 2HDM 
                    idline = idline.replace("combocards/bb_2HDM/datacards/combocards/bb_2HDM/","combocards/bb_2HDM/")
                    idline = idline.replace("combocards/bb_2HDM/datacards/workspace/","combocards/bb_2HDM/workspace/")
                if options.zpb:
                    #combocards/datacards_combination/monoH_MVA_em/muccamvaZbaradaptFull_All_Bin100/datacards_combination
                    idline = idline.replace("combocards/datacards_combination/monoH_MVA_em/muccamvaZbaradaptFull_All_Bin100/", "combocards/")
                                
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
            print "logfile = ", logfile
            print " icard = ", icard.rstrip()
            logfile = 'bin/temp_'+logfile+'.log'
            
            # prepare the command
            if options.thdm:
                command_ = './scan.sh '+icard.rstrip()
            if options.zpb:
                command_ = './scan_zpb.sh '+icard.rstrip()
            print 'command_ = ', command_

            ''' following command_ is not needed, just check and remove them if not needed'''
            
            if options.rungg:
                command_ = command_.replace("scan.sh", "scan_gg.sh")
            if options.runtt:
                command_ = command_.replace("scan.sh", "scan_tt.sh")
            if options.runww:
                command_ = command_.replace("scan.sh", "scan_ww.sh")
            if options.runbb:
                command_ = command_.replace("scan.sh", "scan_bb.sh")
            #command_  = 'combine -M Asymptotic '+icard.rstrip()+' | tee '+logfile
            
            # run it
            os.system(command_)
            
            # extract limit in oe line to fill the text file.
            #limits = ExtractLimits(logfile)
            #print icard, limits
            
        
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
    tempshell7='''
#!/bin/sh                                                                                                                                                                           
export SCRAM_ARCH=slc6_amd64_gcc491
currentpath=$PWD
cd /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_7/src/
eval `scram runtime -sh`
cd /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/
/afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/scan.sh DATACARDNAME
'''

    tempshell='''
#!/bin/sh                                                                                                                                                                           
export SCRAM_ARCH=slc6_amd64_gcc530
currentpath=$PWD
cd /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_8_1_0/src/
eval `scram runtime -sh`
cd /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_8_1_0/src/MonoHCombination/
/afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_8_1_0/src/MonoHCombination/scan.sh DATACARDNAME
'''

    
    ''' following might not be needed '''
    if options.rungg:
        tempshell = tempshell.replace("scan.sh", "scan_gg.sh")
    if options.runtt:
        tempshell = tempshell.replace("scan.sh", "scan_tt.sh")
    if options.runww:
        tempshell = tempshell.replace("scan.sh", "scan_ww.sh")
    if options.runbb:
        tempshell = tempshell.replace("scan.sh", "scan_bb.sh")
    ''' upto this might not be needed '''


    if options.zpb:
        tempshell = tempshell.replace("scan.sh", "scan_zpb.sh")

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

def ScaleLimits(limits):
    xsec_dict={}
    for iline in open(cc.monohCombo["xsec"+model_]):
        mzp = str(iline.rstrip().split()[0])
        ma0 = str(iline.rstrip().split()[1])
        xsec = str(iline.rstrip().split()[2])
        key_ = mzp + '_'+ ma0
        xsec_dict[key_] = xsec
    print xsec_dict
    
    limitsscaled = limits.replace(".txt","_scaled.txt")

    
    flimitout = open(limitsscaled, "w")
    for ilimit in open(limits):
        print "scaling limits for ", ilimit
        mzp = str(ilimit.rstrip().split()[0])
        ma0 = str(ilimit.rstrip().split()[1])
        key_ = mzp + '_'+ ma0
        print key_, (key_ in xsec_dict)
        if key_ in xsec_dict:
            print "found match "
            xsec = float(xsec_dict[key_] )

            twolo_ = str(float(ilimit.rstrip().split()[2])/xsec)
            onelo_ = str(float(ilimit.rstrip().split()[3])/xsec)
            mid_   = str(float(ilimit.rstrip().split()[4])/xsec)
            onehi_ = str(float(ilimit.rstrip().split()[5])/xsec)
            twohi_ = str(float(ilimit.rstrip().split()[6])/xsec)
            obs_   = str(float(ilimit.rstrip().split()[7])/xsec)
            
            newlimit = mzp + ' '+ ma0 + ' '+ twolo_ + ' '+ onelo_ + ' '+ mid_ + ' '+ onehi_ + ' '+ twohi_ + ' '+ obs_ + '\n'
            print newlimit
            flimitout.write(newlimit)
    flimitout.close()


if __name__ == "__main__":
    
    
    #model_ = ""
    #if options.thdm:     model_ =  "2HDM"
    #if options.zpb:      model_ =  "ZPB"
    
    
    if options.combine:
        PrintAvailabilityStatus()
    
    if options.runcombo:
        string_ = 'combocards'+ model_
        print " string_ = ", string_
        RunLimits(cc.monohCombo['combocards'+model_])
        
    '''        
    if options.rungg:
        RunLimits(cc.monohCombo['combocards'+model_])

    if options.runtt:
        RunLimits(cc.monohCombo['ttcards'+model_])

    if options.runww:
        RunLimits(cc.monohCombo['wwcards'+model_])

    if options.runbb:
        RunLimits(cc.monohCombo['bbcards'+model_])

    '''

    
    ''' Followinf function calls are for scaling the limits text files'''
    ''' Once the text files are scaled, one can remove the duplicate elements from them'''
    
    ## for one limits of 2HDM 
    if options.scalelimits and options.thdm and options.oned:
        ScaleLimits('bin/plotsLimitcombo2hdm/limits_2hdm_combo.txt')
    
    
    ## for 2d limits of 2HDM and ZPB both models 
    if options.scalelimits and (not options.oned) :
        ScaleLimits(cc.monohCombo["limits"+model_])


    ## for 2d limits of ZPB both models for SI limits 
    if options.scalelimits and (not options.oned) and options.SI and options.thdm :
        ScaleLimits(cc.monohCombo["limits"+model_])

    ## for one limits of ZPB
    if options.scalelimits and options.zpb and options.oned :
        ScaleLimits('bin/plotsLimitcombozpb/limits_zpb_combo_mchi1.txt')

    #@ for one d limits of gg for ZPB model
    if options.scalegglimits and options.zpb:
        ScaleLimits("bin/plotsLimitcombozpb/limits_zpb_gg.txt")
    
    ## for one d limits of gg for 2HDM model
    if options.scalegglimits and options.thdm:
        ScaleLimits("bin/plotsLimitcombo2hdm/limits_2hdm_gg.txt")
        
    ## for two d limits of bb for spin independednt results
    if options.scalebblimits and options.zpb and options.SI:
        #ScaleLimits("bin/limits_"+model_+"_bb.txt")
        #ScaleLimits("bin/plotsLimitcombozpb/limits_zpb_bb.txt")
        ScaleLimits("/afs/cern.ch/work/k/khurana/public/AnalysisStuff/plotsLimitZpBarApprovalMonoHbb/limits_barzp_monohbb_90C_cleaned.txt")
    
    ## for one d limits of bb for 2hdm
    if options.scalebblimits and options.thdm:
        #ScaleLimits("bin/limits_"+model_+"_bb.txt")
        ScaleLimits("bin/plotsLimitcombo2hdm/limits_2hdm_bb.txt")

    ## for one d limits of bb for zpb
    if options.scalebblimits and options.zpb:
        #ScaleLimits("bin/limits_"+model_+"_bb.txt")
        ScaleLimits("bin/plotsLimitcombozpb/limits_zpb_bb.txt")

    ## for one d limits of ww for zpb
    if options.scalewwlimits and options.zpb:
        #ScaleLimits("bin/limits_"+model_+"_ww.txt")
        ScaleLimits("bin/plotsLimitcombozpb/limits_zpb_ww.txt")

    ## for one d limits of ww for 2hdm
    if options.scalewwlimits and options.thdm:
        #ScaleLimits("bin/limits_"+model_+"_ww.txt")
        ScaleLimits("bin/plotsLimitcombo2hdm/limits_2hdm_ww.txt")
    
    ## for one d limits of tt for zpb
    if options.scalettlimits and options.zpb:
        ScaleLimits("bin/plotsLimitcombozpb/limits_zpb_tt.txt")
    
    ## for one d limits of tt for 2HDM
    if options.scalettlimits and options.thdm:
        ScaleLimits("bin/plotsLimitcombo2hdm/limits_2hdm_tt.txt")

        
    
# python  RunCombo.py -c -r -B -W -T -G -I -P 
