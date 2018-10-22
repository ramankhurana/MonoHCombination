import os 
for imzp in range(450,4000,50):
    for ima0 in range(300,325,25):
        mh = 125 
        if imzp > (ima0 + mh):
            masses   = str(imzp) + " " + str(ima0)
            print masses

