''' 
This script extract the efficiency by doing the back calculation using the analysis tree. 
The trees doesn't have the N2 cut applied so appling the N2 < 0 and also applying the cross-section weights here. 
Since the cross-section is multiplied it requires to access the cross-section file also. 
'''

import os 
import sys 
import optparse 
from ROOT import *

sys.path.append('/afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/CommonUtilities/Helpers')
import fileutils

import scipy
rootfile  = 'data/limitForest_all.root'
crosssectionfile = 'data/CrossSections_20170619_ATLASCMS_Run1Parameters_HiggsMassesFixedToMA.txt'


ZpMass=[600., 800., 1000.,1200.,1400.,1700.,2000.,2500.]
A0Mass=[300., 400., 500.,600.,700.,800.]
lumi_ = 35.9 

fin = fileutils.OpenRootFile(rootfile)


usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)
parser.add_option("-e", "--efficiency",  action="store_true",  dest="efficiency")
parser.add_option("-p", "--histogram",   action="store_true",  dest="histogram")

(options, args) = parser.parse_args()

print options 
def getcrosssection(mzp_, ma0_):
    xs = 0.0 
    for iline in open(crosssectionfile):
        masses = iline.rstrip().split()
        
        mzp = masses[0]
        ma0 = masses[1]
        
        if (mzp_ == str(mzp)) & (ma0_ == str(ma0)):
            xs = masses[7]
            break 
    return xs


def WriteEff():
    froot = TFile("originalshapes.root","UPDATE")
    
    print 'inside write eff'
    fout = open('efficiency-2HDM.txt', 'w' )
    for mzp in ZpMass:
        for ma0 in A0Mass:
            print "inside loop"
            
            mzp_  = str(int(mzp))
            ma0_  = str(int(ma0))
            
            xs_  = float (getcrosssection(mzp_, ma0_) ) * 1000.0 * (0.577)
            
            treename = 'ZpA0_' + mzp_ + '_' + ma0_ +'_signal'
            
            print treename
            
            tree_ = TChain(treename)
            tree_.Add(rootfile)
            
            histname = 'signal_' + treename
            histname = histname.replace("ZpA0_","ZpA0-")
            histname = histname.replace("_","-")
            histname = histname.replace("-signal","_signal")
            histname = histname.replace("signal-","signal_")
            
            
            #nbins = 4
            #binning = [200.0, 270.0, 350.0, 475.0, 1000.0]

            histname_pt = histname+'_pt'
            histname_diff = histname+'_diff'
            histname_up   = histname + '_btagUp'
            histname_down = histname + '_btagDown'
            histname_mistagup   = histname + '_mistagUp'
            histname_mistagdown = histname + '_mistagDown'
            
            nbins = 4
            binning = [200.0, 270.0, 350.0, 475.0, 1000.0]

            
            h = TH1F(histname,histname, nbins, scipy.array(binning))
            h_up = TH1F(histname_up,histname_up, nbins, scipy.array(binning))
            h_down = TH1F(histname_down,histname_down, nbins, scipy.array(binning))
            h_mistagup = TH1F(histname_mistagup,histname_mistagup, nbins, scipy.array(binning))
            h_mistagdown = TH1F(histname_mistagdown,histname_mistagdown, nbins, scipy.array(binning))

            h_pt = TH1F(histname_pt, histname_pt, nbins, scipy.array(binning))
            #h = TH1F(histname,histname, nbins, scipy.array(binning) )
            #h_pt = TH1F(histname_pt, histname_pt, nbins, scipy.array(binning) )
            h_diff = TH1F(histname_diff, histname_diff, 100, -500, 500 )

            tree_.Draw("met>>"+histname,"weight*(N2DDT<0.0)","goff")
            tree_.Draw("met>>"+histname_up,"weight*(N2DDT<0.0)","goff")
            tree_.Draw("met>>"+histname_down,"weight*(N2DDT<0.0)","goff")
            tree_.Draw("met>>"+histname_mistagup,"weight*(N2DDT<0.0)","goff")
            tree_.Draw("met>>"+histname_mistagdown,"weight*(N2DDT<0.0)","goff")

            tree_.Draw("higgsPt>>"+histname_pt,"weight*(N2DDT<0.0)","goff")
            tree_.Draw("(met-higgsPt)>>"+histname_diff,"weight*(N2DDT<0.0)","goff")
            
            eff  = h.Integral()/(lumi_ * xs_ )
            
            print ("integral of ",treename,  h.Integral(), eff)
            
            effline = mzp_ + ' ' + ma0_ + ' ' + str(eff) + '\n'
            if mzp > (ma0 + 125.0):
                fout.write(effline)
                froot.cd()
                h.Write()
                h_up.Write()
                h_down.Write()
                h_mistagup.Write()
                h_mistagdown.Write()
                h_pt.Write()
                h_diff.Write()

    fout.close()
    return 0








def SaveHisto(model='2HDM'):
    print "inside savehisto"
    fhisto = fileutils.OpenRootFile('efficiency-2HDM.root','RECREATE')
    h_eff = TH2F('h_eff_'+model, 'h_eff_'+model, 20 , 600,2600, 7,300,900 )
    
    for iline in open('efficiency-2HDM.txt'):
        masses = iline.rstrip().split()
        h_eff.Fill(float(masses[0]), float(masses[1]),float( masses[2]))
        
    fhisto.cd()
    h_eff.Write()

    





def main():
    if options.efficiency:
        WriteEff()
    if options.histogram:
        SaveHisto()
        
#    if options.recoHisto:
 #       SaveRecoHistograms()
        

if __name__ == "__main__":
    print 'inside __main'
    main()
    
