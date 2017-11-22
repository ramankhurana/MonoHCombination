class crosssection:
    def __init__(self, xsfilename):
        print 'inside initialisation of the cross-section class'
        
        self.filename  = xsfilename
        
    def xs(self, mzp, ma0 ):
        cross_section_ = 0.0
        
        info=[]
        for iline in open(self.filename):
            info = iline.rstrip().split(' ')
            if (int(info[0]) == int(mzp)) & (int(info[1]) == int(ma0)):
                cross_section_ = float(info[2])
                print info
        return cross_section_
    
    
        

xsObj = crosssection('crosssectionZp2HDM.txt')
sigma = xsObj.xs(600,300)
print sigma
