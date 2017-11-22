
import os 

def isExisting(mzp, ma0):
    exists = False 
    for iline in open('data/crosssectionZp2HDM.txt','r'):
        line = iline.rstrip().split()
        mzp_ = line[0]
        ma0_ = line[1]
        if ( ( mzp_ == str(mzp) ) & ( ma0_ == str(ma0)) ):
            exists  =True 
            break
    return exists

    
    


fout = open('data/missingcrosssection.txt','w')
for mzp in range(600, 4000, 25):
    for ma0 in range (300,350, 25):
        isthere = isExisting(mzp, ma0)
        line = str(mzp) + ' '+ str(ma0) + '\n'
        if not isthere:
            fout.write(line)
            
    
