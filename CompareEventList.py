a=[]
for line in open("/afs/cern.ch/user/k/khurana/public/crosssectionZpBaryonic.txt"):
    #aa = line.split() 
    a.append(line)

b=[]
for line2 in open("bin/crosssectionZpBaryonic.txt"):
    #bb = line.split()
    b.append(line2)


aminusb=set(a)-set(b)
bminusa=set(b)-set(a)
sameevent=set(a)&set(b)

ab=list(aminusb)
ba=list(bminusa)
same=list(sameevent)

print "not present in /afs/cern.ch/work/k/khurana/monoHSignalProduction/genproductions/bin/MadGraph5_aMCatNLO/testgridpack/CMSSW_7_4_5/src/MonoHCombination/ReweightingSetup/crosssectio\
nZpBaryonicCleaned.txt" 
for jevent in range(len(ab)):
    print ab[jevent].rstrip()


print "not present in bin/crosssectionZpBaryonic.txt" 
for ievent in range(len(ba)):
    print ba[ievent].rstrip()


print "same of pixel seed and conv veto"




print "lenght of ab =", len(ab)
print "lenght of ba =", len(ba)
print "length of sameevent =", len(same)
