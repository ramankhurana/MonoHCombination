''' 

-- to do list 
  - make following variables global in the class scope. 
  - this can be done by sending all of them to the __init__ and setting them there. 
  - reco name 
  - gen name
  - weight name 
  - rootfile name 
'''

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
- Fill the true histograms for each mass point, 
- data histogram is taken from: 
- For each process one histogram is defined in which each bin will correspond
  to a given region. Last bin correspond to the signal region. 

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
sys.path.append('/afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/ReweightingSetup//CommonUtilities/Helpers')
import fileutils



usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

## data will be true if -d is passed and will be false if -m is passed
parser.add_option("-s", "--savehisto",  action="store_true",  dest="savehisto")
parser.add_option("-w", "--saveweight", action="store_true",  dest="saveweight")
parser.add_option("-t", "--test", action="store_true",  dest="test")

(options, args) = parser.parse_args()


## create lists with offical mass values using the text file, and remove the duplicate values
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
ZpMass=[10, 20, 50, 100, 200, 300, 500, 1000, 2000]
A0Mass=[1]


class FillTrueHistograms:
    def __init__(self, rootfilename, histname, outfile):
        print "inside initialize function"
        
        self.rootfilename = rootfilename
        self.monoHTree = TChain("demo/tree_")
        self.monoHTree.Add(filename)
        self.NEntries = self.monoHTree.GetEntries()
        self.histname = histname
        self.outfile = outfile
        self.hpT = []
        self.MET = []
        self.Diff = []
    def DefineHisto(self):
        #nbins = 8
        #binning = [200.0, 230.0, 270.0, 310.0, 350.0, 400.0, 475.0, 700.0, 1000.0]
        
        #3nbins = 4
        #binning = [200.0, 270.0, 350.0, 475.0, 1000.0]
        #print "inside Define Histo"
        
        ## define one higgs pT histogram for one set of cut values. 
        #for ihist in range(10):
         #   ihist_str = str(ihist)
        #self.hpT.append(TH1F(self.histname, self.histname, nbins, scipy.array(binning) ))
        
        binhi = 1000
        binlo = 50
        #nbins = int ((binhi - binlo )/ 15.0)
        nbins = 20
        self.hpT.append(TH1F(self.histname, self.histname, nbins, binlo, binhi ))
        self.MET.append(TH1F(self.histname+'_pt', self.histname, nbins, binlo, binhi ))
        self.Diff.append(TH1F(self.histname+'_diff', self.histname, 100, -500,500 ))
        return 0
    
    ''' Loop over events and fill the required histograms, right now only hPT is filled  '''
    def Loop(self):
        print "inside Loop"
        for ievent in range(self.NEntries):
            self.monoHTree.GetEntry(ievent)
            higgspT_              =  self.monoHTree.__getattr__('HiggsPt')
            truemet_              =  self.monoHTree.__getattr__('trueMET')
            #if (ievent % 10000) == 0:     print ' event number = ', ievent
            #self.hpT[0].Fill(truemet_)
            self.hpT[0].Fill(higgspT_)
            self.MET[0].Fill(higgspT_)
            self.Diff[0].Fill(truemet_-higgspT_)
        return 0
    
    '''Write histograms to file, only those which are created and filled in this class.'''
    def WriteHisto(self,  mode='update'):
        print "writing histo"
        fout = TFile(self.outfile,mode)
        fout.cd()
        self.hpT[0].Write()
        self.MET[0].Write()
        self.Diff[0].Write()
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
    histname = histname.replace('_tarball_Fixed','')
    return histname



def Recohistname(MZp, MA0):
    histname = 'category_monohiggs/signal_ZpA0-'+MZp + '-' + MA0 +'_signal'
    return histname


def CreateWeights(outfile, targethistname, basehistname, weightHistname, mode='update'):
    print 'creating weight histo'
    fout = TFile(outfile, mode)
    fout.cd()
    #recohistname = recohistname.replace('category_monohiggs/','')
    ## normalise numerator and denominator with same number i.e. unity in this case. 
    target_ = fout.Get(targethistname)
    base_   = fout.Get(basehistname)
    print targethistname, basehistname
    print 'type target = ' , type(target_)
    print 'type base = ' , type(base_)
    
    
    weighthist_ = target_
    if (type(target_) is TH1F )  & (type(base_) is TH1F ):
        print "inside CreateWeights"
        target_.SetDirectory(0)
        base_.SetDirectory(0)
        
        target_.Scale(1.0/target_.Integral())
        base_.Scale(1.0/base_.Integral())
        weighthist_ = target_
        weighthist_.Divide(base_)
        weighthist_.SetName(weightHistname)
    print "type of weight hist in Createweight",type(weighthist_)
    
    return weighthist_


def WriteHistoCopied(outfile, histname,  mode='update'):
    print ('type of hist in WriteHistoCopied = ' , type(histname))
    #print 'writing coped histo ',histname.GetName()
    if type(histname) is TH1F: 
        fout = TFile(outfile,mode)
        fout.cd()
        histname.Write()
        fout.Close()
    return 0

def SaveHisto(filename):
## Input file name 
    fin = fileutils.OpenRootFile(filename)
    
## extrct mass values and hist name 
    tmphistname = filename.split('/')[8]
    ''' For Zp-2HDM Model
    massValue =  tmphistname.split('MZp')[1].split('_MA0')
    '''
    
    ''' For Zp-Baryonic Model'''
    massValue =  tmphistname.split('MZp')[1].split('_MChi')
    #histname = 'gen_ZpA0-'+massValue[0] + '-' + massValue[1] +'_signal'
    histname = Genhistname(massValue[0], massValue[1]) #'gen_ZpA0-'+massValue[0] + '-' + massValue[1] +'_signal' 
    
## make instance of the class
    outputfilename = 'monoHSignalShapes.root'
    fillhisto = FillTrueHistograms (filename, histname, outputfilename)
    
## Deifne histograms 
    fillhisto.DefineHisto()
    
## Loop over events 
    fillhisto.Loop()
    
## Write histogram to rootfile
    fillhisto.WriteHisto()
    
    

## Save Reco Histograms in the rootfile
    #recohistname = 'category_monohiggs/'+ histname.replace('gen_', 'signal_')
    recohistname = Recohistname(massValue[0], massValue[1])#'category_monohiggs/'+ histname.replace('gen_', 'signal_')
    
    hpTReco  = fillhisto.GetRecoHisto('../../mono-x.root', recohistname)
    if type (hpTReco) is TH1F:         fillhisto.WriteHistoCopied(hpTReco)
    
    
    
    
    '''
    ## cerate the weight histogram and save in the same output rootfile
    weightHistname = histname.replace('gen_','weight_')
    hpTWeight = fillhisto.CreateWeights(recohistname, histname, weightHistname)
    fillhisto.WriteHistoCopied(hpTWeight)
    '''
    
    return (histname,recohistname)




def CreateReweightedRecoHisto(weight, target, rootfile, mode='update'):
    fout = TFile(rootfile, mode)
    fout.cd()
    weight_ = fout.Get(weight)
    target_ = fout.Get(target)
    weight_.SetDirectory(0)
    target_.SetDirectory(0)
    
    target_.Scale(1.0/target_.Integral())
    
    target_.Multiply(weight_)
    target_.SetName(target.replace('gen_', 'reweighted_'))
    target_.Write()
    fout.Close()
    


''' filename is the input file, which has all the gen and reco level histograms. 
massvalue is a list with two elements, Zp mass and A0 mass. '''


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


def FindNearestPoint(mzp, ma0):
    
    
    baseZp =  min(ZpMass, key=lambda x:abs(x-int(mzp)))
    baseA0 =  min(A0Mass, key=lambda x:abs(x-int(ma0)))
    '''
    baseZp = ZpMass[ZpMass.index(baseZp)-1]
    '''
    
    ''' for higher base point
    if ZpMass.index(baseZp)+1 < len(ZpMass):
    baseZp = ZpMass[ZpMass.index(baseZp)+1]
    if ZpMass.index(baseZp)+1 >= len(ZpMass):
        baseZp = ZpMass[ZpMass.index(baseZp)-1]
    baseA0 = baseA0
    '''
    
    
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
        


    basePoint = [baseZp, baseA0]
 
    return basePoint

## following code is for the validation purpose. validating interpolation along mDM 
    '''
    if ((int(mzp) - int(baseZp)) ==0) & ((int(ma0) - int(baseA0)) ==0) :
        baseZp = baseZp
        baseA0 = A0Mass[A0Mass.index(baseA0)-1]

    '''
    
    '''
    ## following code is for the validation purpose. validating interpolation along mZp
    if ((int(mzp) - int(baseZp)) ==0) & ((int(ma0) - int(baseA0)) ==0) :
    baseZp = ZpMass[ZpMass.index(baseZp)-1]
        baseA0 = baseA0
    '''


    

def SaveWeightHisto(filename, massvalue):
    highToLow = False
## Input file name 
    fin = fileutils.OpenRootFile(filename)
    
    ## extrct mass values and hist name 
    #tmphistname = filename.split('/')[6]
    #massValue =  tmphistname.split('MZp')[1].split('_MA0')
    
    
    ## check if this is available in the official samples. 
    isinOfficalSample = IsOfficialSample(massvalue)
    print " This is an official sample ", isinOfficalSample
    
    
    massvalueStr = [ str(massvalue[0]), str(massvalue[1]) ]
        
    histname = Genhistname(massvalueStr[0], massvalueStr[1])
    

    ## Following code is useful for the actual running, but not for the validation of the official points. 
    
    ## if this is an official sample then choose the base sample and the target sample so that weights are unity. 
    if isinOfficalSample==True:
        massValueBase = massvalue
    
    if isinOfficalSample==False: 
        massValueBase = FindNearestPoint(int(massvalue[0]), int(massvalue[1]))
        


##    massValueBase = FindNearestPoint(int(massvalue[0]), int(massvalue[1]))
    
    print 'base mass value', massValueBase
    
    

    massBalueBaseStr = [str(massValueBase[0]), str(massValueBase[1])]
    basehistname = Genhistname(massBalueBaseStr[0], massBalueBaseStr[1]) 
    
    ## create the weight histogram and save in the same output rootfile
    weightHistname = histname.replace('gen_','weight_')
    print (filename, histname, basehistname, weightHistname)
    hpTWeight = CreateWeights(filename, histname, basehistname, weightHistname)
    print "type of hpTWeight = ",type(hpTWeight)
    WriteHistoCopied(filename, hpTWeight)
    return 0


def IsOfficialSample(massvec):
    ispresent = False
    for imass in open('zpbaryonicMass_official.txt'):
        #print imass
        massstr  = str(massvec[0]) + ' ' + str(massvec[1])
        if massstr == imass.rstrip():
            ispresent = True
            break
    return ispresent 




if __name__ == "__main__":
    
    ## loop over all the files and save the gen and reco histograms in same rootfile
    if options.savehisto:
        #for ifile in open('rootfiles.txt'):
        for ifile in open('rootfiles.txt'):
            print 'saving the Higgs pT histograms for ', ifile
            filename = ifile.rstrip()
            SaveHisto(filename)
            
    if options.saveweight:
        #for mzp in ZpMass:
        #    for ma0 in  A0Mass:
        
    #    for mzp in [1500]:#, 20, 50, 100, 200, 300, 500, 1000, 2000]: 
    #        for ma0 in [100]:
                #mzp=2500
                #ma0=300
#        for imassval in open('zpbaryonicMass_private.txt'):
        for imassval in open('test.txt'):
        #for imassval in open('zpbaryonicMass_official.txt'):
            #massvec = [int(mzp), int(ma0)]
            massvec = [int(imassval.split(' ')[0]), int(imassval.split(' ')[1])]
            print '----------------------------saving weights for ',massvec
            SaveWeightHisto('monoHSignalShapes.root', massvec)
        #print 'name'
    if options.test:
        for ifile in open('rootfiles.txt'):
            print 'saving the Higgs pT histograms for ', ifile
            filename = ifile.rstrip()
            tmphistname = filename.split('/')[8]
            massValue =  tmphistname.split('MZp')[1].split('_MA0')
            baseMass = FindNearestPoint(massValue[0], massValue[1])
            print massValue, baseMass
## Create the reweighted RECO Histogram for a given mass point 
#CreateReweightedRecoHisto('weight_ZpA0-1400-300_signal', 'gen_ZpA0-1700-300_signal', 'monoHSignalShapes.root')
