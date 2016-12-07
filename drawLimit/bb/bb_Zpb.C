#include <TLegend.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <TH1D.h>
#include <TRandom.h>
#include <TLorentzVector.h>
#include <TFile.h>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <TH1F.h>
#include <TH1.h>
#include <TCanvas.h>
#include <TROOT.h>
#include "TImage.h"
#include "TSystem.h"
#include "TStyle.h"
#include "../untuplizer.h"
#include <TClonesArray.h>
#include <fstream>
#include <cmath>
#include <TSystem.h>
#include <string>
#include <sstream>
#include "../setNCUStyle.C"
#include<TH2.h>
#include "TLine.h"
#include "TF1.h"
#include"TGraphAsymmErrors.h"
#include "TLatex.h"
#include "TPaletteAxis.h"


TH2D*  small0706InputXsec(TH2D* thxsec,string inputDir,string outputName,int option=0,int retrunexp=0){
	TCanvas* c1,*c2;
	setNCUStyle();
	c1 = new TCanvas("c1","",1000,768);
	
	
	int massZ[20]={10,20,50,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,2000,10000};
	int inputZ[9]={0,1,2,4,5,7,12,18,19};
	int massA[8]={1,10,20,50,100,150,500,1000};
	
	TH2D* th2[4];
	th2[0]=new TH2D("expected","expected",9,0,9,8,0,8);
	th2[1]=new TH2D("observed","observed",9,0,9,8,0,8);
	
	th2[2]=new TH2D("expected","expected",9,0,9,8,0,8);
	th2[3]=new TH2D("observed","observed",9,0,9,8,0,8);
	
	
	for(int i=0;i<4;i++){
		th2[i]->SetXTitle("m_{Z'}[GeV]");
		th2[i]->SetYTitle("m_{#chi}[GeV]");
		th2[i]->SetMarkerSize(2);
	}
	
	for(int i=0;i<9;i++){
		for(int j=0;j<8;j++){
				
				TFile* tf1;
				TTree* tree;
				if(massZ[i]==2*massA[j])tf1=TFile::Open(Form("%s/higgsCombineTest_Asymptotic_signalMZp_%d_Mdm_%dGeV_MonoHbb_13TeV.root",inputDir.data(),massZ[inputZ[i]]-5,massA[j]));
				else tf1=TFile::Open(Form("%s/higgsCombineTest_Asymptotic_signalMZp_%d_Mdm_%dGeV_MonoHbb_13TeV.root",inputDir.data(),massZ[inputZ[i]],massA[j]));
				if(!tf1)continue;
				//TDirectory * dir;
				//dir = (TDirectory*)tf1->Get(Form("higgsCombineTest_Asymptotic_%d_%dGeV_MonoHbb_13TeV.root",massZ[i],massA[j]));
				
				tf1->GetObject("limit",tree);
				TreeReader data(tree);
				//data.Print();
				for(Long64_t jEntry=0; jEntry<data.GetEntriesFast() ;jEntry++){
						data.GetEntry(jEntry);
						Float_t  quantileExpected = data.GetFloat("quantileExpected");
						Double_t  limit = data.GetDouble("limit");
						//if(option==1)limit*=8.3;
						if(quantileExpected==0.5)th2[0]->Fill(i,j,limit);
						if(quantileExpected==-1)th2[1]->Fill(i,j,limit);
						
						if(quantileExpected==0.5)th2[2]->Fill(i,j,limit/thxsec->GetBinContent(inputZ[i]+1,j+1));
						if(quantileExpected==-1)th2[3]->Fill(i,j,limit/thxsec->GetBinContent(inputZ[i]+1,j+1));
				}
				
		}
	}
	
	for(int i=0;i<9;i++){
		
		th2[0]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[inputZ[i]]));
		th2[1]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[inputZ[i]]));
		th2[2]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[inputZ[i]]));
		th2[3]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[inputZ[i]]));

	}
	for(int j=0;j<8;j++){
		
		th2[0]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
		th2[1]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
		th2[2]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
		th2[3]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
	}
	th2[2]->Draw("colz,text");
	c1->Print("expected.pdf");
	th2[3]->Draw("colz,text");
	c1->Print("observed.pdf");
	
	
	c1->Clear();
	
	TPad *p1 = new TPad("p1","",0,0.09,1,0.89);
   p1->Draw();
   p1->cd();
   
   th2[3]->Draw("colzTEXT");
   p1->Update();
   Double_t x1,y1,x2,y2;
   gPad->GetRange(x1,y1,x2,y2);

   c1->cd();
   TPad *p2 = new TPad("p2","",0,0.12,1,0.92);
   p2->SetFillStyle(0);
   p2->SetFillColor(0);
   p2->Draw();
   p2->cd();
   
   for(int i=0;i<2;i++){
		th2[i]->SetTitle("");
		th2[i+2]->SetTitle("");
	}
	th2[1]->SetXTitle("");
	th2[1]->SetYTitle("");
	//th2[3]->SetXTitle("");
	//th2[3]->SetYTitle("");
   gStyle->SetPaintTextFormat(" 2.2g ");
   
   p2->Range(x1,y1,x2,y2);
   th2[2]->Draw("TEXTSAME");
	
	TLatex * latex = new TLatex();
    latex->SetNDC();
    //latex->SetTextSize(0.05);
    latex->SetTextAlign(12); // align left
    latex->SetNDC(kTRUE);                                                                                                                        
	latex->SetTextSize(0.032);    
	//latex->SetTextFont(42);
    //latex->DrawLatex(0.15, 0.92, Form("                                                 %.1f fb^{-1} ( 13 TeV )", 2.32));
     //latex->DrawLatex(0.15, 0.68,"CMS");
	//latex->DrawLatex(0.18, 0.885, );
	
	c1->Print(Form("plot/%s.pdf",outputName.data()));
	c1->SaveAs(Form("plot/%s.png",outputName.data()));
	
	if (retrunexp==0)return th2[0];
	else if (retrunexp==1)return th2[1];
	else if (retrunexp==2)return th2[2];
	else if (retrunexp==3)return th2[3];
	//else if (retrunexp==4)return th2[4];
	else return th2[0];
}


void smallDrawTGragh(string outputName,TH2D* th1[],int option=0){
	
	TCanvas* c1;
	c1 = new TCanvas("c1","", 600, 600);
	//gStyle->SetTitleFontSize(0.01);
	TStyle* ts=setNCUStyle();
	//TStyle* ts=new TStyle();
	
	ts->SetTitleSize(0.045,"XYZ");
	ts->SetLabelSize(0.05, "XYZ");
	ts->SetLabelOffset(0.007, "XYZ");
	ts->SetTitleOffset(1.3, "Y");
	ts->SetTitleFontSize(0.005);
	ts->SetPadLeftMargin(0.2);
	ts->SetPadRightMargin(0.11);
	//ts->cd();
	
	//setFPStyle();
	const int nMass=9;
	
	double massZ[nMass]={10,20,50,200,300,500,1000,2000,10000};
	
	
	double db1[6][nMass];
	double db2[6][nMass];
	for(int i=0;i<6;i++){
		for(int j=0;j<nMass;j++){
			db1[i][j]=th1[0]->GetBinContent(j+1,i+1);
			//cout<<i+1<<","<<j+1<<","<<th1[0]->GetBinContent(j+1,i+1)<<endl;
			db2[i][j]=th1[0]->GetBinContent(j+1,i+1);
			if(option ==2)db2[i][j]=th1[1]->GetBinContent(j+1,i+1);
		}
	}
	
	
	TGraph* tg1[6],* tg2[6];
	
	for(int i=0; i<6;i++){
		tg1[i]=new TGraph(nMass,massZ,db1[i]);
		tg2[i]=new TGraph(nMass,massZ,db2[i]);
		/*
		for(int j=0;j<nMass;j++){
			double x,temp=10;
			tg1[i]->GetPoint(j,x,temp);
			if(temp<0.01){
				tg1[i]->RemovePoint(j);
			}
			if(option==2){
				temp=10;
				tg2[i]->GetPoint(j,x,temp);
				if(temp<0.01)tg2[i]->RemovePoint(j);
			}
		}
		for(int j=0;j<nMass;j++){
			double x,temp=10;
			tg1[i]->GetPoint(j,x,temp);
			if(temp<0.01){
				tg1[i]->RemovePoint(j);
			}
			if(option==2){
				temp=10;
				tg2[i]->GetPoint(j,x,temp);
				if(temp<0.01)tg2[i]->RemovePoint(j);
			}
		}
		for(int j=0;j<nMass;j++){
			double x,temp=10;
			tg1[i]->GetPoint(j,x,temp);
			if(temp<0.01){
				tg1[i]->RemovePoint(j);
			}
			if(option==2){
				temp=10;
				tg2[i]->GetPoint(j,x,temp);
				if(temp<0.01)tg2[i]->RemovePoint(j);
			}
		}
		*/
	}
	
	
	/*
	tg1[0]=new TGraph(8,massZ,db1);
	tg1[1]=new TGraph(8,massZ,db2);
	tg1[2]=new TGraph(7,massZ2,db3);
	tg1[3]=new TGraph(7,massZ2,db4);
	tg1[4]=new TGraph(6,massZ3,db5);
	tg1[5]=new TGraph(6,massZ3,db6);
	
	tg2[0]=new TGraph(8,massZ,db21);
	tg2[1]=new TGraph(8,massZ,db22);
	tg2[2]=new TGraph(7,massZ2,db23);
	tg2[3]=new TGraph(7,massZ2,db24);
	tg2[4]=new TGraph(6,massZ3,db25);
	tg2[5]=new TGraph(6,massZ3,db26);
	*/
	tg1[0]->Draw("APL");
	c1->Print("dump.pdf");
	
	for(int i=0;i<1;i++){
		//tg1[i]=new TGraph(8,massZ,db[i]);
		if(option==2)tg1[i]->SetLineStyle(7);
		if(i==1){
			tg1[i]->SetLineColor(kOrange-3);
			tg2[i]->SetLineColor(kOrange-3);
		}
		else if(i==2){
			tg1[i]->SetLineColor(kCyan+2);
			tg2[i]->SetLineColor(kCyan+2);
		}
		else if(i==4){
			tg1[i]->SetLineColor(kGreen+3);
			tg2[i]->SetLineColor(kGreen+3);
		}
		else{
			tg1[i]->SetLineColor(i+1);
			tg2[i]->SetLineColor(i+1);
		} 
		tg1[i]->SetTitle("");
		tg2[i]->SetTitle("");
		if(i==1){
			tg1[i]->SetMarkerColor(kOrange-3);
			tg2[i]->SetMarkerColor(kOrange-3);
		}
		else if(i==2){
			tg1[i]->SetMarkerColor(kCyan+2);
			tg2[i]->SetMarkerColor(kCyan+2);
		}
		else if(i==4){
			tg1[i]->SetMarkerColor(kGreen+3);
			tg2[i]->SetMarkerColor(kGreen+3);
		}
		else{
			tg1[i]->SetMarkerColor(i+1);
			tg2[i]->SetMarkerColor(i+1);
		} 
		tg1[i]->SetFillColor(0);
		tg1[i]->SetLineWidth(3);
		tg2[i]->SetFillColor(0);
		tg2[i]->SetLineWidth(3);
		if(option ==2)  tg1[i]->GetYaxis()->SetTitle("#sigma_{95% CL} / #sigma_{th} ");
		
		//tg1[i]->GetYaxis()->SetFontSize(0.03);
		
		if(i==0){
			tg1[i]->GetXaxis()->SetNdivisions(508);
			tg1[i]->GetXaxis()->SetRangeUser(10,2000);
			tg1[i]->Draw("APL");
			if(option==2)tg2[i]->Draw("PL.same");
			tg1[i]->GetXaxis()->SetTitle("m_{Z'}[GeV]");
			//tg1[i]->SetMaximum(1.3);
			tg1[i]->SetMaximum(101);
			if(option==1)tg1[i]->SetMaximum(0.31);
			tg1[i]->SetMinimum(0);
		}
		else {
			tg1[i]->Draw("PL.same");
			if(option==2)tg2[i]->Draw("PL.same");
		}
	}
	
	TLegend* leg ;
	if(option==1)leg=new TLegend(0.711452,0.152447,0.980645,0.53966);
	else leg=new TLegend(0.711452,0.652447,0.940645,0.913966);
	
	leg->AddEntry(tg1[0],"m_{#chi}=300GeV");
	/*
	leg->AddEntry(tg1[1],"m_{A0}=400GeV");
	leg->AddEntry(tg1[2],"m_{A0}=500GeV");
	leg->AddEntry(tg1[3],"m_{A0}=600GeV");
	leg->AddEntry(tg1[4],"m_{A0}=700GeV");
	leg->AddEntry(tg1[5],"m_{A0}=800GeV");
	*/
	if(option==2){
		leg->Clear();
		leg->AddEntry(tg2[0],"m_{A0}=1 GeV");
		/*
		leg->AddEntry(tg2[1],"m_{A0}=400GeV");
		leg->AddEntry(tg2[2],"m_{A0}=500GeV");
		leg->AddEntry(tg2[3],"m_{A0}=600GeV");
		leg->AddEntry(tg2[4],"m_{A0}=700GeV");
		leg->AddEntry(tg2[5],"m_{A0}=800GeV");
		*/
	}
	 leg->SetFillColor(0);
	leg->SetFillStyle(0);
	 leg->SetTextSize(0.035);
	leg->Draw("same");
	
	TLegend* leg2 ;
	leg2=new TLegend(0.551452,0.802447,0.711452,0.913966);
	TH1D* thL1=new TH1D("","",1,0,1);
	TH1D* thL2=new TH1D("","",1,0,1);
	
	thL2->SetMarkerSize(0);
	thL2->SetLineStyle(7);
	leg2->AddEntry(thL1,"observed");
	leg2->AddEntry(thL2,"expected");
	
	if(option!=1)leg2->Draw("same");
	
	TLatex * latex = new TLatex();
    latex->SetNDC();
    
    latex->SetTextAlign(10); // align left
    latex->SetNDC(kTRUE);                 
	latex->SetTextSize(0.06);    
	//latex->SetTextFont(42);
    if(option==2) {
	    latex->SetTextSize(0.032);    
	//latex->SetTextFont(42);
    //latex->DrawLatex(0.15, 0.92, Form("                                                                  %.1f fb^{-1} ( 13 TeV )", 2.32));
     
     latex->DrawLatex(0.15, 0.87,"CMS");
      latex->SetTextFont(42);
     latex->DrawLatex(0.15, 0.84,"Z'#rightarrow DM+H(2HDM)");
     latex->DrawLatex(0.15, 0.81,"Mono-H Combo");
     latex->DrawLatex(0.15, 0.77," g_{Z'}=0.8");
     latex->DrawLatex(0.15, 0.92, Form("                                                                             %.1f fb^{-1} ( 13 TeV )", 12.9));
     
    } 
	
	else  latex->DrawLatex(0.15, 0.92, Form("CMS                    %.1f fb^{-1} ( 13 TeV )", 12.9));
	
	
	//
	c1->Print(Form("plot/%s.pdf",outputName.data()));
	c1->SaveAs(Form("plot/%s.png",outputName.data()));
	tg1[0]->SetMaximum(250);
	tg1[0]->SetMinimum(0.1);
	c1->SetLogy(1);
	

	 Float_t x0 = 10;
  Float_t x1 = 2000;
  Float_t y0 = 1.;
  Float_t y1 = 1.;
	TLine* one = new TLine(x0,y0,x1,y1);
  one->SetLineColor(2);
  one->SetLineStyle(1);
  one->SetLineWidth(2);
  one->Draw("same");
	
	c1->Print(Form("plot/%sLog.pdf",outputName.data()));
	c1->SaveAs(Form("plot/%sLog.png",outputName.data()));
}

TH2D* readTxt(string inputDir,string outputName,int option=0){
	TCanvas* c1,*c2;
	setNCUStyle();
	c1 = new TCanvas("c1","",1600,800);
	int massZ[20]={10,20,50,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,2000,10000};
	//int inputZ[8]={2,4,6,8,10,13,16,21};
	int massA[8]={1,10,20,50,100,150,500,1000};
	
	TH2D* th2[5];
	th2[0]=new TH2D("eff","eff",20,0,20,8,0,8);
	fstream file1(Form("%s/Zpb_xsec.txt",inputDir.data()));
	for(int i=0;i<20;i++){
		for(int j=0;j<8;j++){
			
			double db1=0,db2=0,db3=0;
			file1>>db1;
			file1>>db2;
			file1>>db3;
			//cout<<db1<<","<<db2<<","<<db3<<endl;
			if(db1==massZ[i] && db2==massA[j])cout<<"i="<<i<<",j="<<j<<",xsec="<<db3<<endl;
			//if(option==1)db1*=8.3;
			th2[0]->Fill(i,j,db3);
		}
	}
	
	for(int i=0;i<20;i++)th2[0]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
	for(int i=0;i<8;i++)th2[0]->GetYaxis()->SetBinLabel(i+1,Form("%d",massA[i]));
	th2[0]->SetXTitle("m_{Z'}[GeV]");
		th2[0]->SetYTitle("m_{#chi}[GeV]");
	th2[0]->SetMarkerSize(2);
	th2[0]->SetTitle(Form("%s",outputName.data()));
	gStyle->SetPaintTextFormat(" 2.2g");
	th2[0]->Draw("colztext");
	c1->Print(Form("plot/%s.pdf",outputName.data()));
	c1->SaveAs(Form("plot/%s.png",outputName.data()));
	return th2[0];
}

void bb_Zpb(){
	TH2D* th2;
	th2=readTxt(".","xsec");
	TH2D* thh[2];
	thh[0]=small0706InputXsec(th2,"../../bb/bb_zpb","limit_2D",0,2);
	thh[1]=small0706InputXsec(th2,"../../bb/bb_zpb","limit_2D",0,3);
	
	smallDrawTGragh("limit_compare1D",thh,2);
}
