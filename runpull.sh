datacardname=$1
mlfit=$2
combine -M MaxLikelihoodFit $datacardname -t -1 --expectSignal 0
mv mlfit.root $mlfit