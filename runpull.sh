datacardname=$1
mlfit=$2
#combine -M MaxLikelihoodFit $datacardname -t -1 --expectSignal 0  
#combine -M MaxLikelihoodFit $datacardname   --rMax 30



## full command 

## freeze binby bin
#combine -M FitDiagnostics  $datacardname -n obs --saveShapes --saveWithUncertainties  --robustFit=1 --X-rtd FITTER_DYN_STEP  --rMin=-5 --rMax=30 --freezeNuisanceGroups binbybin

## run on data
combine -M FitDiagnostics  $datacardname -n obs --saveShapes --saveWithUncertainties  --robustFit=1 --X-rtd FITTER_DYN_STEP  --expectSignal=1 --rMin=-2 --rMax=2

## run on asimov
#combine -M FitDiagnostics  $datacardname -n exp --saveShapes --saveWithUncertainties  --robustFit=1 --X-rtd FITTER_DYN_STEP --expectSignal=1 -t -1 --rMin=-5 --rMax=30

## run in old combine for tautau
#combine -M MaxLikelihoodFit $datacardname  --robustFit=1  --preFitValue=0. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\"  --rMin -2 --rMax 2 --saveNormalizations --saveWithUncertainties   


mv fitDiagnosticsobs.root fitDiagnostics_$mlfit.root
