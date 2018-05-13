# cards path: 

bb 2hdm: https://github.com/zucchett/Combination

bb zpb: /afs/cern.ch/work/b/bmaier/public/xRaman/180426

gg: see email 

WW: /eos/user/n/ntrevisa/datacards_2HDM_Zbar_combination

tautau: /afs/cern.ch/work/g/gfunk/public/datacards_monoh_combo_all/MB_tt_COMBO_UPDATE/

ZZ: 

# Prepration of cards 

## for bb 2HDM 

python BBCards.py

## for bb ZpB 
### create datacards using

###

## for TauTau 
python TauTauCards.py -t
python TauTauCards_zpb.py -b

## for WW 

## for ZZ 

## for gg 




# You can run various steps needed for the mono-H combination using the single macro: 

python RunCombo.py 

## But in this form it doesn't do much. Explore the options it has to do meaningful things. 

python RunCombo.py -c  ## -c is for combining the datacards 

## for WW setup: 

rename the directory datacards_2HDM_Zbar_combination  by datacards_combination

## for gg setup 

## for tautau setup: 
python TauTauCards.py -t 
python TauTauCards.py -b

## for bb 2hdm setup 

## for bbzpb setup 

## for ZZ setup 


## Once the limit text file is there, you need to scale the limits and plot them. 
### Limit can be rescaled using: 
python RunLimits.py --rescale

### Clean limits, this will remove those mass points for which limit has failed. 
python CleanLimits.py

### RemoveDuplicate, Just in case one point was ran twice, you can remove it using following: 
python FindDuplicate.py





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
## # ModelBiulder
