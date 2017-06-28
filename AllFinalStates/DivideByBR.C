void DivideByBR(){
  TString filename = "combination.root";
  float br = 1.;
  bool prodxs = true;
  float xs[]={0.45217, 0.27765, 0.14383, 0.075451, 0.041208, 0.017786, 0.0082317, 0.0025458};
  
  TFile* f = new TFile (filename, "update");
  f->cd();
  TGraph* limitgr = (TGraph*) f->Get("LimitExpectedCLs");
  std::cout<<" # of points = "<<limitgr->GetN()<<std::endl;
  const int npoint = 8;
  Double_t* x;
  Double_t* y;
  x = limitgr->GetX();
  y = limitgr->GetY();


  for (int i=0; i<npoint ;i++){
    y[i]  = y[i] / br ;
    if (prodxs) y[i] = y[i] / xs[i];
    std::cout<<" y = "<<y[i]<<std::endl;
  }
  
  TGraph* limit_  = new TGraph(npoint, x, y);
  limit_ = limitgr;
  limit_->SetName("limit_");
  limit_->Draw();
  limit_->Write();
  
  
}
