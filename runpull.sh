datacardname=$1
mlfit=$2
#combine -M MaxLikelihoodFit $datacardname -t -1 --expectSignal 0  
#combine -M MaxLikelihoodFit $datacardname   --rMax 30



## full command 
#combine -M FitDiagnostics  $datacardname -n obs --saveShapes --saveWithUncertainties  --robustFit=1 --X-rtd FITTER_DYN_STEP  --rMin=-5 --rMax=30 --freezeNuisanceGroups binbybin
combine -M FitDiagnostics  $datacardname -n obs --saveShapes --saveWithUncertainties  --robustFit=1 --X-rtd FITTER_DYN_STEP  --expectSignal=1 --rMin=-2 --rMax=2
#combine -M FitDiagnostics  $datacardname -n exp --saveShapes --saveWithUncertainties  --robustFit=1 --X-rtd FITTER_DYN_STEP --expectSignal=1 -t -1 --rMin=-5 --rMax=30

mv fitDiagnosticsobs.root fitDiagnostics_$mlfit.root
