
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
import Utils
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
sys.path.append('/afs/hep.wisc.edu/cms/khurana/MonoH2016MCProduction/MonoHEfficiency/CMSSW_8_0_11/src/MonoH/MonoHbb/Helpers')
import fileutils
from ReadXS import *

os.system('rm monoHReweightedSignalShapes.root')
usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

## data will be true if -d is passed and will be false if -m is passed
parser.add_option("-s", "--savehisto",  action="store_true",  dest="savehisto")
parser.add_option("-w", "--saveweight", action="store_true",  dest="saveweight")


(options, args) = parser.parse_args()



ZpMass=[600., 800., 1000.,1200.,1400.,1700.,2000.,2500.]
A0Mass=[300., 400., 500.,600.,700.,800.]


class FillTrueHistograms:
    def __init__(self, rootfilename, treename, histname, outfile, weightfilename, xs_ratio):
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
        self.weighthistname = self.histname.replace('signal_','weight_')
        self.weightfilename = weightfilename
        self.xs_ratio = xs_ratio
        self.hpT = []
    
#    def CheckTreeExistence():
        
    def DefineHisto(self):
        print "inside define histogram"
        #nbins = 4
        #binning = [200.0, 270.0, 350.0, 475.0, 1000.0]
        #print "inside Define Histo"
        
        ## define one higgs pT histogram for one set of cut values. 
        #for ihist in range(10):
         #   ihist_str = str(ihist)
        #self.hpT.append(TH1F(self.histname, self.histname, nbins, scipy.array(binning) ))
        

        binhi = 1000
        binlo = 200
        nbins = int ((binhi - binlo )/ 5.0)
        self.hpT.append(TH1F(self.histname, self.histname, nbins, binlo, binhi ))

        return 0
    

    def ExtractGenWeight(self, higgspT):
        weight = 1.0
        matchedBin = 1
        ''' open the weight file'''
        fin = fileutils.OpenRootFile(self.weightfilename)
        weighthist_ = fin.Get(self.weighthistname)
        print " weight histname = ", self.weighthistname
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
            higgspT_               =  self.monoHTree.__getattr__('higgsPt')
            N2DDT_                 =  self.monoHTree.__getattr__('N2DDT')
            genBosonPt_            =  self.monoHTree.__getattr__('genBosonPt')
            met_                   =  self.monoHTree.__getattr__('met')
            weight_                =  self.monoHTree.__getattr__('weight')
            #=  self.monoHTree.__getattr__('')
            
            print 'N2DDT_ = ', N2DDT_
            if N2DDT_ > 0: continue 
            genweight = 1.0 
            
            genweight = self.ExtractGenWeight(higgspT_)
            #genweight = self.ExtractGenWeight(met_)
            print ( 'higgs pT = ', higgspT_, ' genweight = ', genweight)
            #self.weighthistname
            
            totalweight = weight_ * genweight
            self.hpT[0].Fill(met_,totalweight)
            
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
    histname = 'gen_ZpA0-'+MZp + '-' + MA0 +'_signal'
    return histname



def Recohistname(MZp, MA0):
    histname = 'category_monohiggs/signal_ZpA0-'+MZp + '-' + MA0 +'_signal'
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

def SaveHisto(filename, mzp, ma0, postfix=""):

# weights are saved in this file
    weightfilename = 'monoHSignalShapes.root'

# reweighted histograms are saved in this file
    outputfilename = 'monoHReweightedSignalShapes.root'
    

## extract histname with weights 
    tmpname = Genhistname(str(int(mzp)), str(int(ma0)) )
    weighthistname = tmpname.replace('gen_', 'weight_')
    
    print ' weight histo is= ', weighthistname
    mzpTree = min(ZpMass, key=lambda x:abs(x-int( mzp)))
    if (int(mzp) - int(mzpTree)) ==0:
        mzpTree = ZpMass[ZpMass.index(mzpTree)-1]
    
    ma0Tree = min(A0Mass, key=lambda x:abs(x-int( ma0)))

    treename = 'ZpA0_'+ str(int(mzpTree)) +'_'+ str(int(ma0Tree)) +'_signal'+postfix
    print ' treename= ', treename
## extract histname to be saved in the output rootfiles. 
    recohistname = weighthistname.replace('weight_', 'signal_')
    recohistname = recohistname + postfix
    xsobj = crosssection('crosssectionZp2HDM.txt')
    xs_base_ = xsobj.xs(mzpTree, ma0Tree)
    xs_target_ = xsobj.xs(int(mzp), int(ma0))
    xs_ratio_ = float(xs_target_/xs_base_)
    
    
    fillhisto = FillTrueHistograms (filename, treename, recohistname, outputfilename, weightfilename, xs_ratio_)
    
## Deifne histograms 
    fillhisto.DefineHisto()

## Loop over events 
    fillhisto.Loop()
## Write histogram to rootfile
    fillhisto.WriteHisto()
    
    return (recohistname,recohistname)


if __name__ == "__main__":
    filename = '/afs/hep.wisc.edu/cms/khurana/MonoH2016MCProduction/MonoHEfficiency/CMSSW_7_4_7/src/MonoHCombination/BenediktSetup/MonoXFit_MonoH/limitForest_all.root'
    ## loop over all the files and save the gen and reco histograms in same rootfile
    if options.savehisto:
        #for ifile in open('rootfiles.txt'):
        #filename = ifile.rstrip()
        
        for mzp in range(825, 4000, 25):
            for ma0 in range (300,1000, 25):
                ## This function need the mass point for which you need the reweighted histogram 
                ## This will decide by itself the closest mass point which can be used as a base mass point and to be used for the reweighting. 
                ## The reweighted histograms is scaled with the cross-section of target and base cross-section. 
                
        #mzp = int(sys.argv[2])#825
        #ma0 = int(sys.argv[3])#300
                SaveHisto(filename,  int(mzp), int(ma0) )
                SaveHisto(filename,  int(mzp), int(ma0), "_btagUp" )
                SaveHisto(filename,  int(mzp), int(ma0), "_btagDown" )
                SaveHisto(filename,  int(mzp), int(ma0), "_mistagUp" )
                SaveHisto(filename,  int(mzp), int(ma0), "_mistagDown" )
                
        
