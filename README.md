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

not applicable: done in the RunCombo_zpb.py

## for ZZ 

not applicable 

## for gg 

not applicable


# Create the combine cards for each final state 

# For 2HDM Model

## Create WW cards 
python RunCombo_zpb.py  --runww -c -t 

## Run WW cards
python RunCombo_zpb.py  -S -t -r --runww --oned

## Create gg cards 
python RunCombo_zpb.py  --rungg -c -t

## Run gg cards 
python RunCombo_zpb.py  -S -t -r --rungg --oned

## Create bb cards 
python RunCombo_zpb.py  --runbb -c -t

## Run bb cards 
python RunCombo_zpb.py  -S -t -r --runbb --oned


## Create tt cards 
python RunCombo_zpb.py  --runtt -c -t

## Run tt cards 
python RunCombo_zpb.py  -S -t -r --runtt --oned


## Create combo cards 
python RunCombo_zpb.py  -c -t

## Run combo cards 
python RunCombo_zpb.py  -S -t -r --oned




# For Z'-Baryonic Model 

## Create WW cards 
python RunCombo_zpb.py  --runww -c -b 

## Run WW cards
python RunCombo_zpb.py  -S -b -r --runww --oned

## Create gg cards 
python RunCombo_zpb.py  --rungg -c -b

## Run gg cards 
python RunCombo_zpb.py  -S -b -r --rungg --oned

## Create bb cards 
python RunCombo_zpb.py  --runbb -c -b

## Run bb cards 
python RunCombo_zpb.py  -S -b -r --runbb --oned


## Create tt cards 
python RunCombo_zpb.py  --runtt -c -b

## Run tt cards 
python RunCombo_zpb.py  -S -b -r --runtt --oned


## Create combo cards 
python RunCombo_zpb.py  -c -b

## Run combo cards 
python RunCombo_zpb.py  -S -b -r --oned

## Run combo cards for SI Limits
python RunCombo_zpb.py -S -b -r --SI 


# Once the limit is run for each of them, you can now sort the one d limits, this is needed to make the graphs directly from the text file. 
python SortLimit.py 

This will sort all the file in listed in the script. Add more if you wish. 


# Scale limits 1D

## For 2HDM 

### bb
python RunCombo_zpb.py -t --scalebblimits --oned

### gg

python RunCombo_zpb.py -t --scalegglimits --oned	

### tt

python RunCombo_zpb.py -t --scalettlimits --oned	

### ww

python RunCombo_zpb.py -t --scalewwlimits --oned

### zz

python RunCombo_zpb.py -t --scalezzlimits --oned

### combo 

python RunCombo_zpb.py -t --scalelimits  --oned


## For ZpB  

### bb

python RunCombo_zpb.py -b --scalebblimits --oned 

### gg

python RunCombo_zpb.py -b --scalegglimits --oned 

### tt

python RunCombo_zpb.py -b --scalettlimits --oned 

### ww

python RunCombo_zpb.py -b --scalewwlimits --oned 

### zz

python RunCombo_zpb.py -b --scalezzlimits --oned 

### python RunCombo_zpb.py -b --scalelimits  --oned


# Run the pulls 

## to run the pulls and obtain the .root file
source runpull.sh   combocards/combo_gg_ww_tt_bb_ZpB/Datacard_MZp10Ma01MonoHCombo2016FullData.txt bbtt

## to print the result from rootfile
python  diffNuisances.py  fitDiagnostics.root


# Various combinations 

## gg + tautau
python  RunCombo_zpb.py  --runggtt -b -c

python  RunCombo_zpb.py  --runggtt -b -r


## bb + WW
python  RunCombo_zpb.py  --runbbww -b -c 

python  RunCombo_zpb.py  --runbbww -b -r

## gg + tt + WW
python  RunCombo_zpb.py  --runggttww -b -c

python  RunCombo_zpb.py  --runggttww -b -r




## Run limits for one channel 
### For gg : this will create datacards with all paths fixed. 
python RunCombo_zpb.py -c -b --rungg

change if you want to change the dtacards on which limit will be run. 
### Following will run the limits on the points listed in the .txt file. 
python RunCombo_zpb.py -r -b 

### copy the limit.txt into anew file before running the next decay mode 


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


## get the SI limit plot 

python makeDMnucleonXsecPlot.py  --tt --gg --cmb --dd --bb --plotxsec





## Additional 

combine -M Asymptotic roostats-all.root  --freezeParameters zjetsScale

nuisance edit  rename * ww CMS_2016_eff_b CMS2016_eff_b
