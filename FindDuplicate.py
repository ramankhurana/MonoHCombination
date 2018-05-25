import os 
import sys 

#initialFile = 'bin/limits_2hdm_combo_scaled_cleaned.txt'
#NewFile     = 'bin/limits_2hdm_combo_scaled_cleaned_NoDuplicate.txt'

initialFile = 'bin/limits_zpb_combo_cleaned.txt'
NewFile     = 'bin/limits_zpb_combo_cleaned_NoDuplicate.txt'

fout = open(NewFile, 'w')
fulllist=[]
for iline in open(initialFile):
    fulllist.append(iline)


def isduplicate(line, cleanit):
    counter = 0
    
    stripedline = line.rstrip().split()[0] +" "+ line.rstrip().split()[1] 
    for iline in open(initialFile):
        #print 'now checking ', iline
        thisstripedline = iline.rstrip().split()[0] +" "+ iline.rstrip().split()[1]
        if stripedline == thisstripedline: 
            counter = counter +1 
            if counter >1:
                print line
                fulllist.remove(line)
    #os.system('cp '+NewFile+' '+initialFile)
                
    return counter 



    
    
for iline in fulllist:
    counter = isduplicate(iline, True)
    print 'size of list is', len(fulllist)

    
for i in fulllist:
    fout.write(i)
    
    '''
    if counter > 1:
        print iline.rstrip(), "is duplicated ", counter, " times"
    '''
    
