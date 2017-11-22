#!/bin/sh
export SCRAM_ARCH=slc6_amd64_gcc491
currentpath=$PWD
cd /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/ReweightingSetup/
eval `scram runtime -sh`

/afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/ReweightingSetup/FillReweightedHistograms.py -s XXX YYY 

cp /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/ReweightingSetup/data/monoHReweightedSignalShapes_XXX_YYY.root /eos/cms/store/user/khurana/monohgridpacks/2hdm/shapes/monoHReweightedSignalShapes_XXX_YYY.root
#cp /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/batchsubmission/ttemp_XXX_YYY/cmsgrid_final.lhe /eos/cms/store/user/khurana/monohgridpacks/2hdm/LHE/cmsgrid_final_XXX_YYY.lhe

#rm -rf /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/batchsubmission/ttemp_XXX_YYY