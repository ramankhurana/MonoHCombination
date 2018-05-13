#!/usr/bin/env python                                                                                                                                                               
### 
###
# Created By : Raman Khurana
# Date       : 20:July:2017
# Time       : 22:20:30 
###
###
'''
- This macro take the rootfile with tree as input.
- The tree has a branch of Higgs pT and MET and event weight 
- Fill the MET histogram for each mass point after reweighting. 

'''

## import user defined modules
#from Utils import *
#import Utils
import sys
#sys.argv.append( '-b-' )

## this imports basics
from array import array
from ROOT import gROOT, gSystem, gStyle, gRandom
from ROOT import TFile, TChain, TTree, TCut, TH1F, TH2F, THStack, TGraph, TGaxis, TH1, TH2, TObject
from ROOT import TStyle, TCanvas, TPad, TLegend, TLatex, TText
import scipy 

import ROOT
import os
ROOT.gROOT.SetBatch(True)
import sys, optparse
## import helpers files 
import sys
## this will search for files in the previous directory
sys.path.append('../')
## this will search for files in 'Helpers'
#sys.path.append('/afs/hep.wisc.edu/cms/khurana/MonoH2016MCProduction/MonoHEfficiency/CMSSW_8_0_11/src/MonoH/MonoHbb/Helpers')
sys.path.append('/afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/CommonUtilities/Helpers')
import fileutils
from ReadXS import *

#os.system('rm monoHReweightedSignalShapes.root')
usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

## data will be true if -d is passed and will be false if -m is passed
parser.add_option("-s", "--savehisto",  action="store_true",  dest="savehisto")
parser.add_option("-w", "--saveweight", action="store_true",  dest="saveweight")


(options, args) = parser.parse_args()

ZpMass=[]
A0Mass=[]
ZpMass_=set()
A0Mass_=set()
for imass in open('zpbaryonicMass_official.txt'):
    masses = imass.split(' ')
    ZpMass_.add(int(masses[0]))
    A0Mass_.add(int(masses[1]))
    ZpMass=list(ZpMass_)
    A0Mass=list(A0Mass_)

ZpMass.sort()
A0Mass.sort()

#ZpMass=[10, 20, 50, 100, 200, 300, 500, 1000, 2000]
#A0Mass=[1]


class FillTrueHistograms:
    def __init__(self, rootfilename, treename, histname, outfile, weightfilename, xs_ratio, weighthistname):
        print "inside initialize function"
        
        self.rootfilename = rootfilename
        ''' The treename should be with full path'''
        self.monoHTree = TChain(treename)
        self.monoHTree.Add(filename)
        print type (self.monoHTree)
        self.NEntries = self.monoHTree.GetEntries()
        print ' self.NEntries = ', self.NEntries
        self.histname = histname
        self.outfile = outfile
        self.weighthistname = weighthistname
        
        self.weightfilename = weightfilename
        self.xs_ratio = xs_ratio
        self.hpT = []
    
#    def CheckTreeExistence():
        
    def DefineHisto(self):
        print "inside define histogram"
        nbins = 4
        binning = [200.0, 270.0, 350.0, 475.0, 1000.0]
        #print "inside Define Histo"
        
        ## define one higgs pT histogram for one set of cut values. 
        #for ihist in range(10):
         #   ihist_str = str(ihist)
        #self.hpT.append(TH1F(self.histname, self.histname, nbins, scipy.array(binning) ))
        self.hpT.append(TH1F(self.histname, self.histname, nbins, scipy.array(binning) ))
        self.hpT.append(TH1F(self.histname+"Base", self.histname, nbins, scipy.array(binning) ))

        #binhi = 1000
        #binlo = 200
        #nbins = int ((binhi - binlo )/ 80.0)
        #self.hpT.append(TH1F(self.histname, self.histname, nbins, binlo, binhi ))

        return 0
    

    def ExtractGenWeight(self, higgspT):
        weight = 1.0
        matchedBin = 1
        ''' open the weight file'''
        fin = fileutils.OpenRootFile(self.weightfilename)
        weighthist_ = fin.Get(self.weighthistname)
        print " weight histname = ", self.weighthistname
        print " integral of weight histograms is", weighthist_.Integral()
        #print " type = ", type(weighthist_) 
        if type(weighthist_) is TH1F: 
            try: 
                weighthist_.SetDirectory(0)
                print ' nbins = ', weighthist_.GetNbinsX()
                
                for ibin in range(1,weighthist_.GetNbinsX()+1):
                    #print ('ibin = ',ibin, ' bin content = ',weighthist_.GetBinContent(ibin))
                    lowedge  = weighthist_.GetBinLowEdge(ibin)
                    highedge = weighthist_.GetBinLowEdge(ibin) + weighthist_.GetBinWidth(ibin)
                    if ( higgspT > lowedge ) & ( higgspT < highedge):
                        matchedBin = ibin 
                        weight = weighthist_.GetBinContent(ibin)
                        break
            except ValueError:
                print 'the input weight histogram is not found in the rootifle ', self.weighthistname
        return weight
    
            
    
    ''' Loop over events and fill the required histograms, right now only hPT is filled  '''
    def Loop(self):
        
        print "inside Loop"
        for ievent in range(self.NEntries):
        #loop_events = min (10,self.NEntries)
        #for ievent in range(loop_events):
            print ' ievent = ', ievent
            self.monoHTree.GetEntry(ievent)
            higgspT_               =  self.monoHTree.__getattr__('fj1Pt')
            N2DDT_                 =  self.monoHTree.__getattr__('N2DDT')
            genBosonPt_            =  self.monoHTree.__getattr__('higgsPt')
            genMET_                =  self.monoHTree.__getattr__('genMet')
            met_                   =  self.monoHTree.__getattr__('met')
            weight_                =  self.monoHTree.__getattr__('weight')
            #=  self.monoHTree.__getattr__('')
            
            print 'N2DDT_ = ', N2DDT_
            if N2DDT_ > 0: continue 
            genweight = 1.0 
            
            #genweight = self.ExtractGenWeight(higgspT_)

            
            genweight = self.ExtractGenWeight(genBosonPt_)
            print ( 'higgs pT = ', higgspT_, ' genweight = ', genweight)
            #self.weighthistname
            
            totalweight = weight_ * genweight
            self.hpT[0].Fill(met_,totalweight)
            #self.hpT[0].Fill(higgspT_,totalweight)
            
        return 0

    '''Write histograms to file, only those which are created and filled in this class.'''
    def WriteHisto(self,  mode='update'):
        print "writing histo"
        fout = TFile(self.outfile,mode)
        fout.cd()
        self.hpT[0].Scale(self.xs_ratio)
        self.hpT[0].Write()
        fout.Close()
        return 0


    ''' Write histograms to file, only those which are copied/cloned from other rootfiles'''
    def WriteHistoCopied(self, histname,  mode='update'):
        print 'writing coped histo ',histname.GetName()
        fout = TFile(self.outfile,mode)
        fout.cd()
        histname.Write()
        fout.Close()
        return 0
    
    ''' Get histograms from a given rootfile. Function need rootfile name and histogram name as input and return the TH1F'''
    def GetRecoHisto(self, rootfilename, histname, mode='update'):
        print 'getting reco histo'
        fin = TFile(rootfilename, 'READ')
        higgspTReco =  fin.Get(histname)
        
        if type(higgspTReco) is TH1F: higgspTReco.SetDirectory(0)
        TH1.AddDirectory(0)
        TH2.AddDirectory(0)
        #print type(higgspTReco)
        return higgspTReco

    
    ''' Class ends here '''


def Genhistname(MZp, MA0):
    histname = 'gen_BarZp-'+MZp + '-' + MA0 +'_signal'
    return histname



def Recohistname(MZp, MA0):
    histname = 'category_monohiggs/signal_BarZp-'+MZp + '-' + MA0 +'_signal'
    return histname

def WriteHistoCopied(outfile, histname,  mode='update'):
    print ('type of hist in WriteHistoCopied = ' , type(histname))
    #print 'writing coped histo ',histname.GetName()
    if type(histname) is TH1F: 
        fout = TFile(outfile,mode)
        fout.cd()
        histname.Write()
        fout.Close()
    return 0


def findClosestA0(ma0):
    baseA0 =  min(A0Mass, key=lambda x:abs(x-int(ma0)))
    if baseA0 < ma0:
        baseA0 = baseA0
    if baseA0 > ma0:
        idx_a0 = A0Mass.index(baseA0)
        baseA0 = A0Mass[idx_a0-1]
    return baseA0


def findClosestZp(mzp):
    baseZp =  min(ZpMass, key=lambda x:abs(x-int(mzp)))
    if baseZp < mzp:
        baseZp = baseZp
    if baseZp > mzp:
        idx_zp = ZpMass.index(baseZp)
        baseZp = ZpMass[idx_zp-1]
    return baseZp


## This can be used to step down the Ma0 or MZp list entry.                                                                                                                        
def MassStepDown(baseZp, massList):
    if massList.index(baseZp) > 0:
        baseZp = massList[massList.index(baseZp)-1]
    return baseZp
'''

def FindNearestPoint(mzp, ma0):
    baseZp =  min(ZpMass, key=lambda x:abs(x-int(mzp)))
    baseA0 =  min(A0Mass, key=lambda x:abs(x-int(ma0)))

    if ((int(mzp) - int(baseZp)) ==0) & ((int(ma0) - int(baseA0)) ==0) :
   '''     '''keep the same reco histogram'''
'''
    if ((int(mzp) - int(baseZp)) ==0) & ((int(ma0) - int(baseA0)) !=0) :
        baseA0 = findClosestA0(int(ma0))
        baseZp = baseZp

    if ((int(ma0) - int(baseA0)) ==0) & ((int(mzp) - int(baseZp)) !=0):
        baseA0 = baseA0
        baseZp  = findClosestZp(int(mzp))


    if ((int(mzp) - int(baseZp)) !=0) & ((int(ma0) - int(baseA0)) !=0) :
        baseA0 = findClosestA0(int(ma0))
        baseZp  = findClosestZp(int(mzp))

    basePoint = [baseZp, baseA0]
    return basePoint
'''

def IsOfficialSample(massvec):
    ispresent = False
    for imass in open('zpbaryonicMass_official.txt'):
        #print imass                                                                                                                                                                 
        massstr  = str(massvec[0]) + ' ' + str(massvec[1])
        if massstr == imass.rstrip():
            ispresent = True
            break
    return ispresent


def FindNearestPoint(mzp, ma0):
    
    
    baseZp =  min(ZpMass, key=lambda x:abs(x-int(mzp)))
    baseA0 =  min(A0Mass, key=lambda x:abs(x-int(ma0)))
    
    

    ## if mzp is matched but mdm is not
    if ((int(mzp) - int(baseZp)) ==0) :  
        
        A0MassSkim=[]
        for imass in open('zpbaryonicMass_official.txt'):
            masses_ = imass.split(' ')
            if int(masses_[0]) == mzp:
                A0MassSkim.append(int(masses_[1]))
            
        
        baseZp = baseZp
        A0MassSkim.sort()
        baseA0 = min(A0MassSkim, key=lambda x:abs(x-int(ma0)))
        
        
    #########################
    if ((int(ma0) - int(baseA0)) ==0) :
        ZpMassSkim=[]
        for imass in open('zpbaryonicMass_official.txt'):
            masses_ = imass.split(' ')
            if int(masses_[1]) == ma0:
                ZpMassSkim.append(int(masses_[0]))
            
        
        ZpMassSkim.sort()
        baseZp = min(ZpMassSkim, key=lambda x:abs(x-int(mzp)))
        baseA0 = baseA0
        
    #########################
    if ( ((int(mzp) - int(baseZp)) != 0 ) & ((int(ma0) - int(baseA0)) !=0) ):
        baseZp = baseZp 
        print 'basezp before', baseZp, ZpMass
        if ( baseZp > int(mzp) ) & ( baseZp > 1400):
            baseZp = ZpMass[ZpMass.index(baseZp)-1]

        #if baseZp > int(mzp): 
        #    baseZp = ZpMass[ZpMass.index(baseZp)-1]
        
        A0MassSkim=[]
        for imass in open('zpbaryonicMass_official.txt'):
            masses_ = imass.split(' ')
            if int(masses_[0]) == baseZp:
                A0MassSkim.append(int(masses_[1]))

        A0MassSkim.sort()
        print 'A0MassSkim = ',A0MassSkim 
        baseA0 = min(A0MassSkim, key=lambda x:abs(x-int(ma0)))
        if baseA0>ma0:
            baseA0 = A0MassSkim[A0MassSkim.index(baseA0)-1]
        


    ## following code is for the validation purpose. validating interpolation along mDM 
    '''
    if ((int(mzp) - int(baseZp)) ==0) & ((int(ma0) - int(baseA0)) ==0) :
        baseZp = baseZp
        baseA0 = A0Mass[A0Mass.index(baseA0)-1]

    '''
    

    ## following code is for the validation purpose. validating interpolation along mZp
    '''
    if ((int(mzp) - int(baseZp)) ==0) & ((int(ma0) - int(baseA0)) ==0) :
    '''
    ''' this is for higher base sample
        if ZpMass.index(baseZp)+1 < len(ZpMass):
            baseZp = ZpMass[ZpMass.index(baseZp)+1]
            if ZpMass.index(baseZp)+1 >= len(ZpMass):
            baseZp = ZpMass[ZpMass.index(baseZp)-1]
    '''
        
        ## this is for lower base sample. 
        #baseZp = ZpMass[ZpMass.index(baseZp)-1]
        #baseA0 = baseA0



    basePoint = [baseZp, baseA0]
    return basePoint



def SaveHisto(filename, mzp, ma0, postfix=""):
    
# weights are saved in this file
    weightfilename = 'monoHSignalShapes.root'

# reweighted histograms are saved in this file
    #outputfilename = 'monoHReweightedSignalShapes.root'
    outputfilename = 'weightfiles_combo/monoHReweightedSignalShapes'+str(mzp)+'_'+str(ma0)+'.root'
    
    massvalue = [mzp,ma0]
    isinOfficalSample = IsOfficialSample(massvalue)
    print " This is an official sample ", isinOfficalSample

    # Following code is for actual setup
  #  for testing don't use this condition

    if isinOfficalSample==True:
        massValueBase = massvalue

    if isinOfficalSample==False:
        massValueBase = FindNearestPoint(int(massvalue[0]), int(massvalue[1]))
        

    
##    massValueBase = FindNearestPoint(int(massvalue[0]), int(massvalue[1]))
    
## extract histname with weights 
    tmpname = Genhistname(str(int(mzp)), str(int(ma0)) )
    weighthistname = tmpname.replace('gen_', 'weight_')
    
    

    print ' weight histo is= ', weighthistname
    '''
    mzpTree = min(ZpMass, key=lambda x:abs(x-int( mzp)))
    if (int(mzp) - int(mzpTree)) ==0:
        mzpTree = ZpMass[ZpMass.index(mzpTree)-1]
    
    ma0Tree = min(A0Mass, key=lambda x:abs(x-int( ma0)))
    if (int(ma0) - int(ma0Tree)) ==0:
        ma0Tree = A0Mass[A0Mass.index(ma0Tree)-1]

    '''
    mzpTree = str(massValueBase[0])
    ma0Tree = str(massValueBase[1])
    treename = 'BarZp_'+ str((mzpTree)) +'_'+ str((ma0Tree)) +'_signal'+postfix
    print ' treename= ', treename
## extract histname to be saved in the output rootfiles. 
    recohistname = weighthistname.replace('weight_', 'signal_')
    recohistname = recohistname + postfix
    xsobj = crosssection('crosssectionZpBaryonic.txt')
    xs_base_ = xsobj.xs(mzpTree, ma0Tree)
    xs_target_ = xsobj.xs(int(mzp), int(ma0))
    xs_ratio_ = float(xs_target_/xs_base_)
        
    fillhisto = FillTrueHistograms (filename, treename, recohistname, outputfilename, weightfilename, xs_ratio_, weighthistname)
    
## Deifne histograms 
    fillhisto.DefineHisto()

## Loop over events 
    fillhisto.Loop()
## Write histogram to rootfile
    fillhisto.WriteHisto()
    
    return (recohistname,recohistname)


if __name__ == "__main__":
    ''' for actual cross-section '''
    #filename = 'limitForest_nominal.root'
    
    ''' for 1 pb cross-section '''
    filename = '/afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/combocards/bb_Zpb/limitForest_all.root'
    

## loop over all the files and save the gen and reco histograms in same rootfile
    if options.savehisto:
        #for ifile in open('rootfiles.txt'):
        #filename = ifile.rstrip()
        
        #for mzp in [200, 300, 500, 1000, 2000]:
        #    for ma0 in [ 1]:
        
                ## This function need the mass point for which you need the reweighted histogram 
                ## This will decide by itself the closest mass point which can be used as a base mass point and to be used for the reweighting. 
                ## The reweighted histograms is scaled with the cross-section of target and base cross-section. 
                
        mzp = int(sys.argv[2])#825
        ma0 = int(sys.argv[3])#300
        
        #for imass in open('zpbaryonicMass_private.txt'):
        #mzp = imass.split(" ")[0]
        #ma0 = imass.split(" ")[1]
        SaveHisto(filename,  int(mzp), int(ma0) )
        SaveHisto(filename,  int(mzp), int(ma0), "_btagUp" )
        SaveHisto(filename,  int(mzp), int(ma0), "_btagDown" )
        SaveHisto(filename,  int(mzp), int(ma0), "_mistagUp" )
        SaveHisto(filename,  int(mzp), int(ma0), "_mistagDown" )
        
        
