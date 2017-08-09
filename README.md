# MonoHCombination

This is the area to keep the datacards for each analysis. 

There is one directory for each analysis. Please keep your datacards in respective directory (latest one). 

Try to use the same naming convention of the datacards in order to avoid the failure of combiantion code (in next iteration). 

Try to run one card locally in your area before you push it to the github. It would be hard otherwise which decay mode cards are causing problems and lead to delays. 

## 
Make the tau tau combine cards  ready for combination
python TauTauCards.py


## incase willing to try: 
git clone git@github.com:ramankhurana/MonoHCombination.git 

or if you already have the code just update the cards in case they have changed. 

git pull --rebase


## Full grid for the 2HDM Model

## For Z' Baryonic model we can try to have following points for the combo: 
Mchi=1, 150, 500 GeV for MZp=500 GeV
Mchi=1, 150, 1000 GeV for MZp=1000 GeV



## Prepare tt cards
python TauTauCards.py

## prepare  bb datacards  
   * Remove ../ in the rootfile path. 
   * use bb/scan_2hdm.sh for preparing the datacards 
   * For Pull
     * combine -M MaxLikelihoodFit  bb/datacards_2HDM/ZpA0-1000-300/combined.txt  -t -1 --saveNormalizations --saveShapes --saveWithUncertainties
cards 
   

python bbCards.py

## Prepare combined cards 
python CombineDataCards.py Combination tt bb WW gg ZZ

## Run the combine cards 
## 