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
#include"TMultiGraph.h"


TH2D* small0706Base(string inputDir,string outputName,int option=0,int retrunexp=0){
	TCanvas* c1,*c2;
	TStyle* ts =setNCUStyle();
	//ts->SetPadRightMargin(0.17);
	ts->SetTitleOffset(0.65, "Z");
	ts->SetTitleOffset(0.8, "Y");
	c1 = new TCanvas("c1","",1000,768);
	
	int massZ[8]={600,800,1000,1200,1400,1700,2000,2500};
	int inputZ[8]={1,2,3,4,5,7,8,11};
	int massA[6]={300,400,500,600,700,800};
	
	TH2D* th2[4];
	th2[0]=new TH2D("expected","expected",8,0,8,6,0,6);
	th2[1]=new TH2D("observed","observed",8,0,8,6,0,6);
	
	th2[2]=new TH2D("expected","expected",8,0,8,6,0,6);
	th2[3]=new TH2D("observed","observed",8,0,8,6,0,6);
	
	TFile* tf1;
	
	tf1=TFile::Open("../ScanPlot_gz08.root");
	TH2F * th2f2=(TH2F *)tf1->FindObjectAny("xsec1");
	
	
	for(int i=0;i<4;i++){
		th2[i]->SetXTitle("m_{Z'}[GeV]");
		th2[i]->SetYTitle("m_{A0}[GeV]");
		th2[i]->SetMarkerSize(2);
	}
	
	for(int i=0;i<8;i++){
		for(int j=0;j<6;j++){
				
				TFile* tf1;
				TTree* tree;
				tf1=TFile::Open(Form("%s/higgsCombineTest_Asymptotic_%d_%dGeV_MonoHbb_13TeV.root",inputDir.data(),massZ[i],massA[j]));
				std::cout<<" filename = "<<tf1<<std::endl;
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
						
						if(quantileExpected==0.5)th2[2]->Fill(i,j,limit/th2f2->GetBinContent(inputZ[i],j+2));
						if(quantileExpected==-1)th2[3]->Fill(i,j,limit/th2f2->GetBinContent(inputZ[i],j+2));
				}
				
		}
	}
	
	for(int i=0;i<8;i++){
		
		th2[0]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
		th2[1]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
		th2[2]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
		th2[3]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));

	}
	for(int j=0;j<6;j++){
		
		th2[0]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
		th2[1]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
		th2[2]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
		th2[3]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
	}
	th2[3]->SetZTitle("#sigma_{95% CL} / #sigma_{th}");
	th2[2]->Draw("colz,text");
	c1->Print("expected.pdf");
	th2[3]->Draw("colz,text");
	c1->Print("observed.pdf");
	
	
	c1->Clear();
	
	TPad *p1 = new TPad("p1","",0,0.09,1,0.89);
   p1->Draw();
   p1->cd();
   //th2[3]->SetLogz(1);
   p1->SetLogz();
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
   gStyle->SetPaintTextFormat(" 4.2f ");
   
   p2->Range(x1,y1,x2,y2);
   th2[2]->Draw("TEXTSAME");
	
	TLatex * latex = new TLatex();
    latex->SetNDC();
    //latex->SetTextSize(0.05);
    latex->SetTextAlign(12); // align left
    latex->SetNDC(kTRUE);                                                                                                                        
	latex->SetTextSize(0.04);    
	//latex->SetTextFont(42);
   // latex->DrawLatex(0.15, 0.92, Form("                                                                  %.1f fb^{-1} ( 13 TeV )", 2.32));
     latex->DrawLatex(0.15, 0.84,"CMS");
       latex->SetTextFont(42);
	latex->DrawLatex(0.15, 0.81,"Z'#rightarrow DM+H");
      latex->DrawLatex(0.15, 0.77," (2HDM)");
      latex->DrawLatex(0.15, 0.73," Mono-H Combo");
		 latex->DrawLatex(0.15, 0.92, Form("                                                                                        %.1f fb^{-1} ( 13 TeV )", 12.9));
     
	c1->Print(Form("plot/%s.pdf",outputName.data()));
	c1->SaveAs(Form("plot/%s.png",outputName.data()));
	
	
	if (retrunexp==0)return th2[0];
	else if (retrunexp==1)return th2[1];
	else if (retrunexp==2)return th2[2];
	else if (retrunexp==3)return th2[3];
	//else if (retrunexp==4)return th2[4];
	else return th2[0];
}

TH2D* getSigmaLimit(string inputDir,int option=0){
	TCanvas* c1,*c2;
	TStyle* ts =setNCUStyle();
	ts->SetPadRightMargin(0.14);
	c1 = new TCanvas("c1","",889,768);
	
	int massZ[8]={600,800,1000,1200,1400,1700,2000,2500};
	int inputZ[8]={1,2,3,4,5,7,8,11};
	int massA[6]={300,400,500,600,700,800};
	
	TH2D* th2[4];
	th2[0]=new TH2D("expected","expected",8,0,8,6,0,6);
	th2[1]=new TH2D("observed","observed",8,0,8,6,0,6);
	
	th2[2]=new TH2D("expected","expected",8,0,8,6,0,6);
	th2[3]=new TH2D("observed","observed",8,0,8,6,0,6);
	
	TFile* tf1;
	
	tf1=TFile::Open("../ScanPlot_gz08.root");
	TH2F * th2f2=(TH2F *)tf1->FindObjectAny("xsec1");
	
	
	for(int i=0;i<4;i++){
		th2[i]->SetXTitle("m_{Z'}[GeV]");
		th2[i]->SetYTitle("m_{A0}[GeV]");
		th2[i]->SetMarkerSize(2);
	}
	
	for(int i=0;i<8;i++){
		for(int j=0;j<6;j++){
				
				TFile* tf1;
				TTree* tree;
				tf1=TFile::Open(Form("%s/higgsCombineTest_Asymptotic_%d_%dGeV_MonoHbb_13TeV.root",inputDir.data(),massZ[i],massA[j]));
				if(!tf1)continue;
				//TDirectory * dir;
				//dir = (TDirectory*)tf1->Get(Form("higgsCombineTest_Asymptotic_%d_%dGeV_MonoHbb_13TeV.root",massZ[i],massA[j]));
				
				tf1->GetObject("limit",tree);
				TreeReader data(tree);
				//data.Print();
				data.GetEntry(option);
				Double_t  limit = data.GetDouble("limit");
				th2[0]->Fill(i,j,limit/th2f2->GetBinContent(inputZ[i],j+2));
				/*
				for(Long64_t jEntry=0; jEntry<data.GetEntriesFast() ;jEntry++){
						data.GetEntry(jEntry);
						Float_t  quantileExpected = data.GetFloat("quantileExpected");
						Double_t  limit = data.GetDouble("limit");
						//if(option==1)limit*=8.3;
						if(quantileExpected==0.5)th2[0]->Fill(i,j,limit);
						if(quantileExpected==-1)th2[1]->Fill(i,j,limit);
						
						if(quantileExpected==0.5)th2[2]->Fill(i,j,limit/th2f2->GetBinContent(inputZ[i],j+2));
						if(quantileExpected==-1)th2[3]->Fill(i,j,limit/th2f2->GetBinContent(inputZ[i],j+2));
				}
				*/
		}
	}
	th2[0]->Draw("text");
	c1->Print(Form("%d.pdf",option));
	
	 return th2[0];
}

TH2D* small0706Compare(string inputDir[],string outputName,int option=0,int retrunexp=0){
	TCanvas* c1,*c2;
	setNCUStyle();
	c1 = new TCanvas("c1","",889,768);
	
	int massZ[8]={600,800,1000,1200,1400,1700,2000,2500};
	//int inputZ[8]={2,4,6,8,10,13,16,21};
	int inputZ[8]={1,2,3,4,5,7,8,11};
	int massA[6]={300,400,500,600,700,800};
	
	TH2D* th2[5];
	th2[0]=new TH2D("expected","expected",8,0,8,6,0,6);
	th2[1]=new TH2D("observed","observed",8,0,8,6,0,6);
	
	th2[2]=new TH2D("expected","expected",8,0,8,6,0,6);
	th2[3]=new TH2D("observed","observed",8,0,8,6,0,6);
	
	th2[4]=new TH2D("saveInf","",8,0,8,6,0,6);
	
	TFile* tf1;
	
	tf1=TFile::Open("../ScanPlot_gz08.root");
	TH2F * th2f2=(TH2F *)tf1->FindObjectAny("xsec1");
	
	
	for(int i=0;i<5;i++){
		th2[i]->SetXTitle("m_{Z'}[GeV]");
		th2[i]->SetYTitle("m_{A0}[GeV]");
		th2[i]->SetMarkerSize(2);
	}
	
	for(int i=0;i<8;i++){
		for(int j=0;j<6;j++){
				
				TFile* tf1,* tf2;
				TTree* tree,*tree2;
				tf1=TFile::Open(Form("%s/higgsCombineTest_Asymptotic_%d_%dGeV_MonoHbb_13TeV.root",inputDir[0].data(),massZ[i],massA[j]));
				tf2=TFile::Open(Form("%s/higgsCombineTest_Asymptotic_%d_%dGeV_MonoHbb_13TeV.root",inputDir[1].data(),massZ[i],massA[j]));
				//if(!tf2 || !tf2->IsOpen())continue;
				if(!tf1 || !tf1->IsOpen()){
					
				}
				if (!tf2 || !tf2->IsOpen()){
					tf2=TFile::Open(Form("%s/higgsCombineTest_Asymptotic_%d_%dGeV_MonoHbb_13TeV.root",inputDir[0].data(),massZ[i],massA[j]));
				}
				//if(!tf1)continue;
				//TDirectory * dir;
				//dir = (TDirectory*)tf1->Get(Form("higgsCombineTest_Asymptotic_%d_%dGeV_MonoHbb_13TeV.root",massZ[i],massA[j]));
				
				tf1->GetObject("limit",tree);
				tf2->GetObject("limit",tree2);
				TreeReader data(tree);
				TreeReader data2(tree2);
				//data.Print();
				bool isData1=0;
				Double_t  limit[2]={0,0};
				int jEntryMax=data.GetEntriesFast();
				if(data.GetEntriesFast()==0){
					limit[0]=1000;
					jEntryMax=data2.GetEntriesFast();
				}
				if(i==3 &&j==1)cout<<"jMax="<<jEntryMax<<endl;
				for(Long64_t jEntry=0; jEntry< jEntryMax;jEntry++){
						data.GetEntry(jEntry);
						data2.GetEntry(jEntry);
						Float_t  quantileExpected = data.GetFloat("quantileExpected");
						
						
						if(data.GetEntriesFast()==0) quantileExpected = data2.GetFloat("quantileExpected");
						if(data.GetEntriesFast()!=0)limit[0]= data.GetDouble("limit");
						limit[1]= data2.GetDouble("limit");
						//if(option==1)limit[1]*=8.3;
						if(i==3 &&j==1){
							cout<<limit[0]<<","<<limit[1]<<","<<quantileExpected<<endl;
							}
						
						if(quantileExpected==0.5){
							
							
							th2[0]->Fill(i,j,limit[0]<limit[1]?limit[0]:limit[1]);
							isData1=limit[0]<limit[1]?1:0;
							
							th2[2]->Fill(i,j,(limit[0]<limit[1]?limit[0]:limit[1])/th2f2->GetBinContent(inputZ[i],j+2));
							if (isData1)th2[4]->Fill(i,j,1);
							else th2[4]->Fill(i,j,2);
						}
						if(quantileExpected==-1){
							if(isData1)th2[1]->Fill(i,j,limit[0]);
							else th2[1]->Fill(i,j,limit[1]);
							
							if(isData1)th2[3]->Fill(i,j,limit[0]/th2f2->GetBinContent(inputZ[i],j+2));
							else th2[3]->Fill(i,j,limit[1]/th2f2->GetBinContent(inputZ[i],j+2));
						}
						
				}
				
		}
	}
	
	for(int i=0;i<8;i++){
		
		th2[4]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
		th2[1]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
		th2[2]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
		th2[3]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
	}
	for(int j=0;j<6;j++){
		
		th2[4]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
		th2[1]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
		th2[2]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
		th2[3]->GetYaxis()->SetBinLabel(j+1,Form("%d",massA[j]));
	}
	th2[4]->Draw("colz");
	th2[0]->Draw("text,same");
	c1->Print("expected.pdf");
	th2[1]->Draw("colz,text");
	c1->Print("observed.pdf");
	
	
	c1->Clear();
	
	TPad *p1 = new TPad("p1","",0,0.09,1,0.89);
   p1->Draw();
   p1->cd();
   th2[4]->Draw("colz");
   th2[3]->Draw("TEXT,same ");
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
   gStyle->SetPaintTextFormat(" 4.2f ");
   
   p2->Range(x1,y1,x2,y2);
   th2[2]->Draw("TEXTSAME");
	
	TLatex * latex = new TLatex();
    latex->SetNDC();
    //latex->SetTextSize(0.05);
    latex->SetTextAlign(12); // align left
    latex->SetNDC(kTRUE);                                                                                                                        
	latex->SetTextSize(0.06);    
	//latex->SetTextFont(42);
    latex->DrawLatex(0.15, 0.92, Form("CMS                         %.1f fb^{-1} ( 13 TeV )", 12.9));//latex->DrawLatex(0.18, 0.885, );
	
	c1->Print(Form("plot/%s.pdf",outputName.data()));
	c1->SaveAs(Form("plot/%s.png",outputName.data()));
	if (retrunexp==0)return th2[0];
	else if (retrunexp==1)return th2[1];
	else if (retrunexp==2)return th2[2];
	else if (retrunexp==3)return th2[3];
	else if (retrunexp==4)return th2[4];
	else return th2[0];
}

void smallDrawTGragh(string outputName,TH2D* th1[],int option=0){
	/*TCanvas* c1,*c2;
	setNCUStyle();
	c1 = new TCanvas("c1","",889,768);
	double db1[8]={0};
	double db2[8]={0};
	double db3[7]={0};
	double db4[7]={0};
	double db5[5]={0};
	double db6[6]={0};
	double db21[8]={0};
	double db22[8]={0};
	double db23[7]={0};
	double db24[7]={0};
	double db25[5]={0};
	double db26[6]={0};
	double massZ[8]={600,800,1000,1200,1400,1700,2000,2500};
	double massZ2[7]={800,1000,1200,1400,1700,2000,2500};
	double massZ3[6]={1000,1200,1400,1700,2000,2500};
	double massZ4[5]={1200,1400,1700,2000,2500};
	double massZ5[7]={600,800,1000,1200,1400,1700,2000};
	double massZ6[5]={1000,1400,1700,2000,2500};
	
	for(int j=0;j<8;j++)db1[j]=th1[0]->GetBinContent(j+1,1);
	for(int j=0;j<8;j++)db2[j]=th1[0]->GetBinContent(j+1,2);
	for(int j=0;j<7;j++)db3[j]=th1[0]->GetBinContent(j+2,3);
	for(int j=0;j<6;j++)db4[j]=th1[0]->GetBinContent(j+3,4);
	
	
	for(int j=0;j<6;j++)db5[j]=th1[0]->GetBinContent(j+3,5);
	for(int j=0;j<6;j++)db6[j]=th1[0]->GetBinContent(j+3,6);
	
	for(int j=0;j<8;j++)db21[j]=th1[1]->GetBinContent(j+1,1);
	for(int j=0;j<8;j++)db22[j]=th1[1]->GetBinContent(j+1,2);
	for(int j=0;j<7;j++)db23[j]=th1[1]->GetBinContent(j+2,3);
	for(int j=0;j<6;j++)db24[j]=th1[1]->GetBinContent(j+3,4);
	
	
	for(int j=0;j<6;j++)db25[j]=th1[1]->GetBinContent(j+3,5);
	for(int j=0;j<6;j++)db26[j]=th1[1]->GetBinContent(j+3,6);
	
	TGraph* tg1[6];
	
	tg1[0]=new TGraph(8,massZ,db1);
	tg1[1]=new TGraph(8,massZ,db2);
	tg1[2]=new TGraph(7,massZ2,db3);
	tg1[3]=new TGraph(6,massZ3,db4);
	tg1[4]=new TGraph(6,massZ3,db5);
	tg1[5]=new TGraph(6,massZ3,db6);
	
	
	TGraph* tg2[6];
	
	tg2[0]=new TGraph(8,massZ,db21);
	tg2[1]=new TGraph(8,massZ,db22);
	tg2[2]=new TGraph(7,massZ2,db23);
	tg2[3]=new TGraph(6,massZ3,db24);
	tg2[4]=new TGraph(6,massZ3,db25);
	tg2[5]=new TGraph(6,massZ3,db26);
	
	
	for(int i=0;i<6;i++){
		//tg1[i]=new TGraph(8,massZ,db[i]);
		if(option==2)tg1[i]->SetLineStyle(7);
		if(i==1){
			tg1[i]->SetLineColor(7);
			tg2[i]->SetLineColor(7);
		}
		else{
			tg1[i]->SetLineColor(i+1);
			tg2[i]->SetLineColor(i+1);
		} 
		tg1[i]->SetTitle("");
		tg2[i]->SetTitle("");
		if (i==1){
			tg1[i]->SetMarkerColor(7);
			tg2[i]->SetMarkerColor(7);
		}
		else{
			tg1[i]->SetMarkerColor(i+1);
			tg2[i]->SetMarkerColor(i+1);
		} 
		tg1[i]->SetFillColor(0);
		tg1[i]->SetLineWidth(3);
		tg2[i]->SetFillColor(0);
		tg2[i]->SetLineWidth(3);
		
		if(i==0){
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
	else leg=new TLegend(0.711452,0.652447,0.960645,0.913966);
	leg->SetFillColor(0);
	leg->SetFillStyle(0);
	leg->AddEntry(tg1[0],"m_{A0}=300GeV");
	leg->AddEntry(tg1[1],"m_{A0}=400GeV");
	leg->AddEntry(tg1[2],"m_{A0}=500GeV");
	leg->AddEntry(tg1[3],"m_{A0}=600GeV");
	leg->AddEntry(tg1[4],"m_{A0}=700GeV");
	leg->AddEntry(tg1[5],"m_{A0}=800GeV");
	if(option==2){
		leg->Clear();
		leg->AddEntry(tg2[0],"m_{A0}=300GeV");
		leg->AddEntry(tg2[1],"m_{A0}=400GeV");
		leg->AddEntry(tg2[2],"m_{A0}=500GeV");
		leg->AddEntry(tg2[3],"m_{A0}=600GeV");
		leg->AddEntry(tg2[4],"m_{A0}=700GeV");
		leg->AddEntry(tg2[5],"m_{A0}=800GeV");
	}
	 leg->SetTextSize(0.035);
	leg->Draw("same");
	TLegend* leg2 ;
	leg2=new TLegend(0.451452,0.752447,0.711452,0.913966);
	TH1D* thL1=new TH1D("","",1,0,1);
	TH1D* thL2=new TH1D("","",1,0,1);
	
	thL2->SetLineStyle(7);
	leg2->AddEntry(thL1,"observed");
	leg2->AddEntry(thL2,"expected");
	
	if(option!=1)leg2->Draw("same");
	TLatex * latex = new TLatex();
    latex->SetNDC();
    //latex->SetTextSize(0.03);
    latex->SetTextAlign(10); // align left
    latex->SetNDC(kTRUE);                                                                                                                        
	latex->SetTextSize(0.06);    
	latex->SetTextFont(42);
    if(option==2)latex->DrawLatex(0.15, 0.92, Form("CMS                                                       %.1f fb^{-1} ( 13 TeV )", 2.32));
	else latex->DrawLatex(0.15, 0.92, Form("CMS                                              %.1f fb^{-1} ( 13 TeV )", 2.32));
	//
	c1->Print(Form("plot/%s.pdf",outputName.data()));
	c1->SaveAs(Form("plot/%s.png",outputName.data()));
	tg1[0]->SetMaximum(250);
	tg1[0]->SetMinimum(0.1);
	c1->SetLogy(1);
	

	 Float_t x0 = 600;
  Float_t x1 = 2500;
  Float_t y0 = 1.;
  Float_t y1 = 1.;
	TLine* one = new TLine(x0,y0,x1,y1);
  one->SetLineColor(2);
  one->SetLineStyle(1);
  one->SetLineWidth(2);
  one->Draw("same");
	
	c1->Print(Form("plot/%sLog.pdf",outputName.data()));
	c1->SaveAs(Form("plot/%sLog.png",outputName.data()));
	*/
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
	double massZ[8]={600,800,1000,1200,1400,1700,2000,2500};
	/*
	double db1[8]={0};
	double db2[8]={0};
	double db3[7]={0};
	double db4[7]={0};
	double db5[5]={0};
	double db6[6]={0};
	
	double massZ2[7]={800,1000,1200,1400,1700,2000,2500};
	double massZ3[6]={1000,1200,1400,1700,2000,2500};
	double massZ4[5]={1200,1400,1700,2000,2500};
	
	for(int j=0;j<8;j++)db1[j]=th1[0]->GetBinContent(j+1,1);
	for(int j=0;j<8;j++)db2[j]=th1[0]->GetBinContent(j+1,2);
	for(int j=0;j<7;j++)db3[j]=th1[0]->GetBinContent(j+2,3);
	for(int j=0;j<7;j++)db4[j]=th1[0]->GetBinContent(j+2,4);
	for(int j=0;j<6;j++)db5[j]=th1[0]->GetBinContent(j+3,5);
	for(int j=0;j<6;j++)db6[j]=th1[0]->GetBinContent(j+3,6);
	
	double db21[8]={0};
	double db22[8]={0};
	double db23[7]={0};
	double db24[7]={0};
	double db25[5]={0};
	double db26[6]={0};
	if(option ==2){
		for(int j=0;j<8;j++)db21[j]=th1[1]->GetBinContent(j+1,1);
		for(int j=0;j<8;j++)db22[j]=th1[1]->GetBinContent(j+1,2);
		for(int j=0;j<7;j++)db23[j]=th1[1]->GetBinContent(j+2,3);
		for(int j=0;j<7;j++)db24[j]=th1[1]->GetBinContent(j+2,4);
		for(int j=0;j<6;j++)db25[j]=th1[1]->GetBinContent(j+3,5);
		for(int j=0;j<6;j++)db26[j]=th1[1]->GetBinContent(j+3,6);
	}
	else {
		for(int j=0;j<8;j++)db21[j]=th1[0]->GetBinContent(j+1,1);
		for(int j=0;j<8;j++)db22[j]=th1[0]->GetBinContent(j+1,2);
		for(int j=0;j<7;j++)db23[j]=th1[0]->GetBinContent(j+2,3);
		for(int j=0;j<7;j++)db24[j]=th1[0]->GetBinContent(j+2,4);
		for(int j=0;j<6;j++)db25[j]=th1[0]->GetBinContent(j+3,5);
		for(int j=0;j<6;j++)db26[j]=th1[0]->GetBinContent(j+3,6);
	}
	*/
	
	double db1[6][8];
	double db2[6][8];
	for(int i=0;i<6;i++){
		for(int j=0;j<8;j++){
			db1[i][j]=th1[0]->GetBinContent(j+1,i+1);
			//cout<<i+1<<","<<j+1<<","<<th1[0]->GetBinContent(j+1,i+1)<<endl;
			db2[i][j]=th1[0]->GetBinContent(j+1,i+1);
			if(option ==2)db2[i][j]=th1[1]->GetBinContent(j+1,i+1);
		}
	}
	
	
	TGraph* tg1[6],* tg2[6];
	
	for(int i=0; i<6;i++){
		tg1[i]=new TGraph(8,massZ,db1[i]);
		tg2[i]=new TGraph(8,massZ,db2[i]);
		
		for(int j=0;j<8;j++){
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
		for(int j=0;j<8;j++){
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
		for(int j=0;j<8;j++){
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
	
	for(int i=0;i<6;i++){
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
	
	leg->AddEntry(tg1[0],"m_{A0}=300GeV");
	leg->AddEntry(tg1[1],"m_{A0}=400GeV");
	leg->AddEntry(tg1[2],"m_{A0}=500GeV");
	leg->AddEntry(tg1[3],"m_{A0}=600GeV");
	leg->AddEntry(tg1[4],"m_{A0}=700GeV");
	leg->AddEntry(tg1[5],"m_{A0}=800GeV");
	if(option==2){
		leg->Clear();
		leg->AddEntry(tg2[0],"m_{A0}=300GeV");
		leg->AddEntry(tg2[1],"m_{A0}=400GeV");
		leg->AddEntry(tg2[2],"m_{A0}=500GeV");
		leg->AddEntry(tg2[3],"m_{A0}=600GeV");
		leg->AddEntry(tg2[4],"m_{A0}=700GeV");
		leg->AddEntry(tg2[5],"m_{A0}=800GeV");
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
	

	 Float_t x0 = 600;
  Float_t x1 = 2500;
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
	c1 = new TCanvas("c1","",889,768);
	int massZ[8]={600,800,1000,1200,1400,1700,2000,2500};
	int inputZ[8]={2,4,6,8,10,13,16,21};
	int massA[6]={300,400,500,600,700,800};
	
	TH2D* th2[5];
	th2[0]=new TH2D("eff","eff",8,0,8,6,0,6);
	for(int i=0;i<8;i++){
		for(int j=0;j<6;j++){
			fstream file1(Form("%s/ratelineMZp%d_MA0%d.txt",inputDir.data(),massZ[i],massA[j]));
			double db1=0;
			file1>>db1;
			db1/=23000;
			db1/=0.577;
			if(option==1)db1*=8.3;
			th2[0]->Fill(i,j,db1);
		}
	}
	
	for(int i=0;i<8;i++)th2[0]->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
	for(int i=0;i<6;i++)th2[0]->GetYaxis()->SetBinLabel(i+1,Form("%d",massA[i]));
	th2[0]->SetXTitle("m_{Z'}[GeV]");
		th2[0]->SetYTitle("m_{A0}[GeV]");
	th2[0]->SetMarkerSize(2);
	th2[0]->SetTitle(Form("%s",outputName.data()));
	gStyle->SetPaintTextFormat(" 4.4f ");
	th2[0]->Draw("colztext");
	c1->Print(Form("plot/%s.pdf",outputName.data()));
	c1->SaveAs(Form("plot/%s.png",outputName.data()));
	return th2[0];
}

TH2D* TH2DComparer(TH2D* th1,TH2D* th2){
		int massZ[8]={600,800,1000,1200,1400,1700,2000,2500};
	
	int massA[6]={300,400,500,600,700,800};
	
	TCanvas* c1,*c2;
	setNCUStyle();
	c1 = new TCanvas("c1","",889,768);
	TH2D* th3;
	th3=new TH2D("eff","eff",8,0,8,6,0,6);
	for(int i=0;i<8;i++){
		for(int j=0;j<6;j++){
			double a=th1->GetBinContent(i+1,j+1),b=th2->GetBinContent(i+1,j+1);
			th3->SetBinContent(i+1,j+1,a>b?a:b);
		}
	}
	for(int i=0;i<8;i++)th3->GetXaxis()->SetBinLabel(i+1,Form("%d",massZ[i]));
	for(int i=0;i<6;i++)th3->GetYaxis()->SetBinLabel(i+1,Form("%d",massA[i]));
	th3->SetXTitle("m_{Z'}[GeV]");
	th3->SetYTitle("m_{A0}[GeV]");
	th3->SetMarkerSize(2);
	gStyle->SetPaintTextFormat(" 4.4f ");
	th3->Draw("colztext");
	c1->Print("plot/effMax.pdf");
	c1->SaveAs("plot/effMax.png");
	return th3;
}

TGraph* excludeLimit(TH2D* th2,int option=0){
		double massZ[8]={600,800,1000,1200,1400,1700,2000,2500};
		double y[8]={0};
		double yy[8]={0};
		
		for(int i=0;i<8;i++){
			for(int j=0;j<6;j++){
				//cout<<th2->GetBinContent(i+1,j+1)<<"c"<<endl;
				if(th2->GetBinContent(i+1,j+1)<1)continue;
				else {
					//cout<<th2->GetBinContent(i+1,j+1)<<endl;
					if(j==0)y[i]=0;
					else {
						double x=(1-th2->GetBinContent(i+1,j))/(th2->GetBinContent(i+1,j+1)-th2->GetBinContent(i+1,j));
						yy[i]=x+j-1;
						cout<<yy[i]<<",";
						y[i]=300+(j+x-1)*100;
					}
					break;
				}
			}	
			cout<<endl;
		}
		
		for(int i=0;i<8;i++)cout<<"y["<<i<<"]="<<y[i]<<endl;
		TGraph* tg1=new TGraph(8,massZ,y);
		
		double massZZ[8]={0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5};
		TGraph* tg2=new TGraph(8,massZZ,yy);
		if(option==1)return tg2;
		else return tg1;
}

void drawExcludeLimit(TGraph* tg1,TGraph* tg2,int rangeUp=2500){
	TCanvas* c1;
	setNCUStyle(1);
	c1 = new TCanvas("c1","",889,768);
	
	tg2->SetFillColor(0);
	tg1->SetFillColor(0);
	tg2->SetLineColor(2);
	tg1->Draw("APL");
	c1->Print("exclude.pdf");
	tg1->SetLineWidth(3);
	tg2->SetLineWidth(3);
	tg1->SetTitle("");
	tg1->Draw("APL");
	tg2->Draw("PL,same");
	tg1->SetMaximum(800);
	tg1->SetMinimum(300);
	tg1->GetXaxis()->SetTitle("m_{Z'}[GeV]");
	tg1->GetXaxis()->SetNdivisions(508);
	tg1->GetXaxis()->SetRangeUser(600,rangeUp);
	tg1->GetYaxis()->SetTitle("m_{A0}[GeV]");
	
	TLegend* leg ;
	leg=new TLegend(0.711452,0.652447,0.940645,0.863966);
	leg->SetFillColor(0);
	leg->SetFillStyle(0);
	leg->AddEntry(tg1,"expected");
	leg->AddEntry(tg2,"observed");
	leg->Draw("same");
	
	TLatex * latex = new TLatex();
    latex->SetNDC();
    //latex->SetTextSize(0.03);
    latex->SetTextAlign(10); // align left
    latex->SetNDC(kTRUE);                                                                                                                        
	latex->SetTextSize(0.06);    
	latex->SetTextFont(42);
    latex->DrawLatex(0.15, 0.92, Form("CMS                         %.1f fb^{-1} ( 13 TeV )", 2.32));
	
	c1->Print(Form("plot/exclude_%d.pdf",rangeUp));
	c1->SaveAs(Form("plot/exclude_%d.png",rangeUp));
}

void drawExcludeLimitSigma(TGraph* tg1[],TGraph* tg2,int rangeUp=2500){
	TCanvas* c1;
	setNCUStyle(1);
	c1 = new TCanvas("c1","",889,768);
	
	tg2->SetFillColor(0);
	
	
	tg2->SetLineColor(2);
	//tg1->Draw("APL");
	//c1->Print("exclude.pdf");
	tg1[2]->SetLineWidth(3);
	tg2->SetLineWidth(3);
	tg1[0]->SetTitle("");
	//tg1[0]->Draw("APL");
	
	//tg1[1]->Draw("PL,same");
	//tg1[2]->Draw("PL,same");
	//tg1[3]->Draw("PL,same");
	//tg1[4]->Draw("PL,same");
	
	double limitSigma[5][8];
	for(int i=0;i<5;i++){
		double* temp=tg1[i]->GetY(); 
		for(int j=0;j<8;j++){
			limitSigma[i][j]=temp[j];
			cout<<temp[j]<<",";
		}
		cout<<endl;
	}
	for(int i=0;i<8;i++){
		limitSigma[0][i]-=limitSigma[2][i];
		limitSigma[1][i]-=limitSigma[2][i];
		limitSigma[3][i]=limitSigma[2][i]-limitSigma[3][i];
		limitSigma[4][i]=limitSigma[2][i]-limitSigma[4][i];
		
	}
	
	double massZ[8]={600,800,1000,1200,1400,1700,2000,2500};
	TGraphAsymmErrors* limit_68=new TGraphAsymmErrors(8,massZ,limitSigma[2],0,0,limitSigma[4],limitSigma[0]);
	TGraphAsymmErrors* limit_95=new TGraphAsymmErrors(8,massZ,limitSigma[2],0,0,limitSigma[3],limitSigma[1]);
	
	limit_68->SetMaximum(800);
	limit_68->SetMinimum(300);
	limit_68->GetXaxis()->SetTitle("m_{Z'}[GeV]");
	limit_68->GetXaxis()->SetNdivisions(508);
	limit_68->GetXaxis()->SetRangeUser(600,rangeUp+10);
	limit_68->GetYaxis()->SetTitle("m_{A0}[GeV]");
	
	limit_68->SetFillColor(kYellow);
	limit_68->Draw("3A");
	
	limit_95->SetFillColor(kGreen);
	limit_95->Draw("3 same");
	
	tg1[2]->SetFillColor(0);
	tg1[2]->Draw("PLsame");
	
	tg2->Draw("PL,same");
	
	
	TLegend* leg ;
	leg=new TLegend(0.711452,0.652447,0.940645,0.863966);
	leg->SetFillColor(0);
	leg->SetFillStyle(0);
	leg->AddEntry(tg1[2],"expected");
	leg->AddEntry(limit_95,"1 #sigma");
	leg->AddEntry(limit_68,"2 #sigma");
	
	leg->AddEntry(tg2,"observed");
	leg->Draw("same");
	
	TLatex * latex = new TLatex();
    latex->SetNDC();
    //latex->SetTextSize(0.03);
    latex->SetTextAlign(10); // align left
    latex->SetNDC(kTRUE);                                                                                                                        
	latex->SetTextSize(0.06);    
	latex->SetTextFont(42);
    latex->DrawLatex(0.15, 0.92, Form("CMS                         %.1f fb^{-1} ( 13 TeV )", 2.32));
	
	c1->Print(Form("plot/exclude_%d.pdf",rangeUp));
	c1->SaveAs(Form("plot/exclude_%d.png",rangeUp));
}

void drawExcludeLimitWith2D(TGraph* tg1,TGraph* tg2,TH2D* th2[]){
	TCanvas* c1;
	TStyle* ts =setNCUStyle();
	ts->SetPadRightMargin(0.14);
	c1 = new TCanvas("c1","",889,768);
	/*
	double yy1[8],yy2[8];
	for(int i=0;i<8;i++){
		yy1[i]=0;
	}
	*/
	c1->Clear();
	
	TPad *p1 = new TPad("p1","",0,0.09,1,0.89);
   p1->Draw();
   p1->cd();
   
    th2[1]->Draw("colz text");

  tg1->Draw("pl same");
	tg2->Draw("PL,same");
	
	//th2[2]->Draw("colz,same");
   //th2[1]->Draw("TEXT,same ");
   p1->Update();
   Double_t x1,y1,x2,y2;
   gPad->GetRange(x1,y1,x2,y2);

   c1->cd();
   TPad *p2 = new TPad("p2","",0,0.12,1,0.92);
   p2->SetFillStyle(0);
   p2->SetFillColor(0);
   p2->Draw();
   p2->cd();
   
   gStyle->SetPaintTextFormat(" .4g");
   
   p2->Range(x1,y1,x2,y2);
   th2[0]->Draw("TEXTSAME");
	
	TLatex * latex = new TLatex();
    latex->SetNDC();
    //latex->SetTextSize(0.05);
    latex->SetTextAlign(12); // align left
    latex->SetNDC(kTRUE);                                                                                                                        
	latex->SetTextSize(0.06);    
	latex->SetTextFont(42);
    latex->DrawLatex(0.15, 0.92, Form("CMS                         %.1f fb^{-1} ( 13 TeV )", 2.32));//latex->DrawLatex(0.18, 0.885, );
	
	
	tg2->SetFillColor(0);
	tg1->SetFillColor(0);
	tg2->SetLineColor(2);
	//tg1->Draw("APL");
	//c1->Print("exclude.pdf");
	tg1->SetLineWidth(tg1->GetLineWidth()*2);
	tg2->SetLineWidth(tg2->GetLineWidth()*2);
	
	
	tg1->SetMaximum(800);
	tg1->SetMinimum(300);
	tg1->GetXaxis()->SetTitle("m_{Z'}[GeV]");
	tg1->GetXaxis()->SetNdivisions(508);
	tg1->GetXaxis()->SetRangeUser(600,2500);
	tg1->GetYaxis()->SetTitle("m_{A0}[GeV]");
	
	TLegend* leg ;
	leg=new TLegend(0.711452,0.652447,0.940645,0.863966);
	leg->SetFillColor(0);
	leg->SetFillStyle(0);
	leg->AddEntry(tg1,"exp");
	leg->AddEntry(tg2,"obs");
	//leg->Draw("same");
	c1->Print("plot/exclude2D.pdf");
	
	
	//c1->Print("plot/exclude.pdf");
	//c1->SaveAs("plot/exclude.png");
}

void small0803(){
	
	
	TH2D* th2,*th3,*th4;
	th2=small0706Base("../../Combination","limit_combination",0,2);
	std::cout<<" after th2, th3"<<std::endl;
	th3=small0706Base("../../Combination","limit_combination",0,3);
	//th2=small0706Compare(in,"limit_compare",1,2);
	std::cout<<" after th2, th3"<<std::endl;
	TGraph* tg1,*tg2;
	tg1=excludeLimit(th2);
	
	TH2D* thh[2];
	thh[0]=th2;
	thh[1]=th3;
	
	th2->SetName("exp");
	th3->SetName("obs");
	TFile* outFile = new TFile("output.root","recreate");
	th2->Write();
	th3->Write();
	outFile->Close();

	
	
	smallDrawTGragh("limit_compare1D",thh,2);
	//smallDrawTGragh("limit_compare1D_obs",th3);
	//th3=small0706Compare(in,"limit_compare",1,3);
	//th4=small0706Compare(in,"limit_compare",1,4);
	
	
	tg2=excludeLimit(th3);
	
	drawExcludeLimit(tg1,tg2);
	drawExcludeLimit(tg1,tg2,1400);
	
	//draw limit 2 sigma
	TH2D* th_sigma[5];
	th_sigma[0]=getSigmaLimit("../../Combination",0);
	th_sigma[1]=getSigmaLimit("../../Combination",1);
	th_sigma[2]=getSigmaLimit("../../Combination",2);
	th_sigma[3]=getSigmaLimit("../../Combination",3);
	th_sigma[4]=getSigmaLimit("../../Combination",4);
	
	TGraph* tg_sigma[5];
	tg_sigma[0]=excludeLimit(th_sigma[0]);
	tg_sigma[1]=excludeLimit(th_sigma[1]);
	tg_sigma[2]=excludeLimit(th_sigma[2]);
	tg_sigma[3]=excludeLimit(th_sigma[3]);
	tg_sigma[4]=excludeLimit(th_sigma[4]);
	
	
	drawExcludeLimitSigma(tg_sigma,tg2,1400);
	drawExcludeLimitSigma(tg_sigma,tg2);
	
	tg1=excludeLimit(th2,1);
	tg2=excludeLimit(th3,1);
	
	drawExcludeLimitWith2D(tg1,tg2,thh);
}




