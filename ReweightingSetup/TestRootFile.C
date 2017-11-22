void TestRootFile(TString filename){
  filename = "data/"+filename;
  TFile* f   = new TFile(filename, "READ");
  std::cout<<" file = "<<filename<<std::endl;
  TString histname = filename.ReplaceAll("data/monoHReweightedSignalShapes_","signal_ZpA0-");
  histname = histname.ReplaceAll("_","-");
  histname = histname.ReplaceAll(".root", "_signal");
  histname = histname.ReplaceAll("signal-", "signal_");
  //signal_ZpA0-800_300.root
  //signal_ZpA0-800-300_signal
  TH1F* h = (TH1F*) f->Get(histname);
  TH1F* h_up = (TH1F*) f->Get(histname+"_btagUp");
  TH1F* h_down = (TH1F*) f->Get(histname+"_btagDown");
  
  std::cout<<" file = "<<filename
	   <<" histo = "<<histname
	   <<" integral = "<<h->Integral(1,-1)
	   <<" mean = "<<h->GetMean()
	   <<" rms = "<<h->GetRMS()
    	   <<" integral_up = "<<h_up->Integral()
	   <<" integral_down = "<<h_down->Integral()
	   <<std::endl;

    
}
