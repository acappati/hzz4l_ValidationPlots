#!/usr/bin/env python

# *********************************************
# usage: 
#    python ratioPlots_jetsDistrib_DATAvsMC.py
#
# *********************************************

import json
import ROOT
from ROOT import *
import math, helper, CMSGraphics, CMS_lumi
from CMSGraphics import makeCMSCanvas, makeLegend
from helper import ReadJSON
from helper import DoSimpleFit, Result
from ROOT import TFile, TH1, TH1F, TCanvas, gSystem, TAttFill, TLegend, TRatioPlot, TPad, TStyle, THStack, TPaveText, gStyle
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

# *****************************                                                                                                                       
# Data tree options                                                                                                                              
# *****************************                                                                                                                                       
CRZLTree  = True
ZTree     = False
# *****************************                                                                                                                                         
# Data periods options                                                                                                                                                    
# *****************************                                                                                                                                          
#period = "data2016"                                                                                                                                                        
#period = "data2017"                                                                                                                                              
period = "data2018"
# *****************************      

def DrawRatioPlot(name, xaxis_title, yaxis_title, c, data, MC, MCUp, MCDn, logscale):
        c.Divide(0,2,0,0)
        pad1 = c.cd(1)

        pad1.SetBottomMargin(0.02)
        pad1.SetTopMargin(0.18)
        pad1.SetLeftMargin(0.10)
    
        if logscale:
                pad1.SetLogy()

        max = 0.
        for bin in range (MC.GetSize() - 2):
                if ( MC.GetBinContent(bin + 1) > max):
                        max = MC.GetBinContent(bin + 1)

        MC.SetMaximum(1.4*max)
        
        MC.SetFillColor(kOrange + 1)
        MC.GetYaxis().SetTitle(yaxis_title)
        MC.Draw("HIST")
        MC.GetXaxis().SetLabelSize(0)
        MC.GetYaxis().SetTitleSize(0.07)
        MC.GetYaxis().SetLabelSize(0.07)
        MC.GetYaxis().SetTitleOffset(0.7)
        
        data.SetLineColor(ROOT.kBlack)
        data.SetMarkerStyle(20)
        data.SetMarkerSize(0.6)
        data.Draw("p E1 X0 SAME")

        pad2 = c.cd(2)

        pad2.SetBottomMargin(0.20)
        pad2.SetTopMargin(0.02)
        pad2.SetLeftMargin(0.10)
    
        Ratio    = TH1F("Ratio","Ratio",MC.GetSize() - 2, MC.GetXaxis().GetXmin(),MC.GetXaxis().GetXmax())
        sigma_up = TH1F("sigma_up","sigma_up",MC.GetSize() - 2, MC.GetXaxis().GetXmin(),MC.GetXaxis().GetXmax())
        sigma_dn = TH1F("sigma_dn","sigma_dn",MC.GetSize() - 2, MC.GetXaxis().GetXmin(),MC.GetXaxis().GetXmax())

        for bin in range (MC.GetSize() - 2):
                if (MC.GetBinContent(bin + 1) == 0):
                        Ratio   .SetBinContent(bin + 1, 0)
                        Ratio   .SetBinError(bin + 1, 0)
                        sigma_up.SetBinContent(bin + 1, 0)
                        sigma_dn.SetBinContent(bin + 1, 0)
                else:
                        Ratio   .SetBinContent(bin + 1, float(data.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        Ratio   .SetBinError  (bin + 1, 1./(data.GetBinContent(bin + 1))**0.5)
                        sigma_up.SetBinContent(bin + 1, float(MCUp.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        sigma_dn.SetBinContent(bin + 1, float(MCDn.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))

        for bin in range (Ratio.GetSize() - 2):
                temp = Ratio.GetBinContent(bin + 1)
                Ratio.SetBinContent( bin + 1, temp - 1)

        for bin in range (sigma_up.GetSize() - 2):
                temp = sigma_up.GetBinContent(bin + 1)
                sigma_up.SetBinContent( bin + 1, temp - 1)

        for bin in range (sigma_dn.GetSize() - 2):
                temp = sigma_dn.GetBinContent(bin + 1)
                sigma_dn.SetBinContent( bin + 1, temp - 1)

        sigma_up.SetFillColor(ROOT.kGray)
        sigma_up.SetLineColor(ROOT.kGray)
        sigma_up.SetMaximum(2.0)
        sigma_up.SetMinimum(-2.0)
        sigma_up.GetXaxis().SetTitle(xaxis_title)
        sigma_up.GetYaxis().SetTitle("(Data/MC)-1")
        sigma_up.GetYaxis().SetTitleOffset(0.6)
        sigma_up.Draw("HIST")
        sigma_up.GetXaxis().SetLabelSize(0.07)
        sigma_up.GetXaxis().SetTitleSize(0.07)
        sigma_up.GetYaxis().SetLabelSize(0.07)
        sigma_up.GetYaxis().SetTitleSize(0.07)
        
        sigma_dn.SetFillColor(ROOT.kGray)
        sigma_dn.SetLineColor(ROOT.kGray)
        sigma_dn.Draw("HIST SAME")
        
        gPad.RedrawAxis()
        
        Ratio.SetMarkerStyle(20)
        Ratio.SetMarkerSize(0.6)
        Ratio.Draw("p E1 X0 SAME")
        
        pad1.cd()
        leg = TLegend(.75,.45,.95,.75)
        leg.SetBorderSize(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.07)
        #leg.AddEntry(MC, "Z/t#bar{t} + jets", "f" )
        leg.AddEntry(MC, "DY + t#bar{t}  MC", "f" )
        leg.AddEntry(data, "Data", "p")
        leg.AddEntry(sigma_up, "JEC Uncertainty", "f")
        leg.Draw()

        #draw CMS and lumi text                                                                                                                                                          
        CMS_lumi.writeExtraText = True
        CMS_lumi.extraText      = "Preliminary"
        CMS_lumi.lumi_sqrtS     = lumiText + " (13 TeV)"
        CMS_lumi.cmsTextSize    = 0.6
        CMS_lumi.lumiTextSize   = 0.46
        CMS_lumi.extraOverCmsTextSize = 0.75
        CMS_lumi.relPosX = 0.12
        CMS_lumi.CMS_lumi(pad1, 0, 0)
        c.Update()

        c.SaveAs(name+".pdf")
        c.SaveAs(name+".png")
        
        c.Clear()


if (period == "data2016"):
        fDY = TFile.Open("/eos/user/a/amapane/CJLST-backup/190617/MC_2016/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")
        fTT = TFile.Open("/eos/user/a/amapane/CJLST-backup/190617/MC_2016/TTTo2L2Nu/ZZ4lAnalysis.root")
        fdata = TFile.Open("/eos/user/a/amapane/CJLST-backup/190617/Data_2016/AllData/ZZ4lAnalysis.root")
        lumi = 35.92 # /fb
        lumiText = "35.92 fb^{-1}"

        if (CRZLTree):
                tDY = fDY.Get("CRZLTree/candTree")
                counterDY = fDY.Get("CRZLTree/Counters")
                SumWeight_DY = counterDY.GetBinContent(40)
                tTT = fTT.Get("CRZLTree/candTree")
                counterTT = fTT.Get("CRZLTree/Counters")
                SumWeight_TT = counterTT.GetBinContent(40)
                tdata = fdata.Get("CRZLTree/candTree")
                treeText = "CRZLTree"

        elif (ZTree):
                tDY = fDY.Get("ZTree/candTree")
                counterDY = fDY.Get("ZTree/Counters")
                SumWeight_DY = counterDY.GetBinContent(1)
                tTT = fTT.Get("zTree/candTree")
                counterTT = fTT.Get("ZTree/Counters")
                SumWeight_TT = counterTT.GetBinContent(1)
                tdata = fdata.Get("ZTree/candTree")
                treeText = "ZTree"

elif (period == "data2017"):
        fDY = TFile.Open("/eos/user/a/amapane/CJLST-backup/190617/MC_2017/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")
        fTT = TFile.Open("/eos/user/a/amapane/CJLST-backup/190617/MC_2017/TTTo2L2Nu/ZZ4lAnalysis.root")
        fdata = TFile.Open("/eos/user/a/amapane/CJLST-backup/190617/Data_2017/AllData/ZZ4lAnalysis.root")
        lumi = 41.53 # /fb
        lumiText = "41.53 fb^{-1}"

        if (CRZLTree):
                tDY = fDY.Get("CRZLTree/candTree")
                counterDY = fDY.Get("CRZLTree/Counters")
                SumWeight_DY = counterDY.GetBinContent(40)
                tTT = fTT.Get("CRZLTree/candTree")
                counterTT = fTT.Get("CRZLTree/Counters")
                SumWeight_TT = counterTT.GetBinContent(40)
                tdata = fdata.Get("CRZLTree/candTree")
                treeText = "CRZLTree"

        elif (ZTree):
                tDY = fDY.Get("ZTree/candTree")
                counterDY = fDY.Get("ZTree/Counters")
                SumWeight_DY = counterDY.GetBinContent(1)
                tTT = fTT.Get("zTree/candTree")
                counterTT = fTT.Get("ZTree/Counters")
                SumWeight_TT = counterTT.GetBinContent(1)
                tdata = fdata.Get("ZTree/candTree")
                treeText = "ZTree"

elif (period == "data2018"):
        fDY = TFile.Open("/eos/user/a/amapane/CJLST-backup/190617/MC_2018/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")
        fTT = TFile.Open("/eos/user/a/amapane/CJLST-backup/190617/MC_2018/TTTo2L2Nu/ZZ4lAnalysis.root")
        fdata = TFile.Open("/eos/user/a/amapane/CJLST-backup/190617/Data_2018/AllData/ZZ4lAnalysis.root")
        lumi = 59.74 # /fb
        lumiText = "59.74 fb^{-1}"

        if (CRZLTree):
                tDY = fDY.Get("CRZLTree/candTree")
                counterDY = fDY.Get("CRZLTree/Counters")
                SumWeight_DY = counterDY.GetBinContent(40)
                tTT = fTT.Get("CRZLTree/candTree")
                counterTT = fTT.Get("CRZLTree/Counters")
                SumWeight_TT = counterTT.GetBinContent(40)
                tdata = fdata.Get("CRZLTree/candTree")
                treeText = "CRZLTree"

        elif (ZTree):
                tDY = fDY.Get("ZTree/candTree")
                counterDY = fDY.Get("ZTree/Counters")
                SumWeight_DY = counterDY.GetBinContent(1)
                tTT = fTT.Get("zTree/candTree")
                counterTT = fTT.Get("ZTree/Counters")
                SumWeight_TT = counterTT.GetBinContent(1)
                tdata = fdata.Get("ZTree/candTree")
                treeText = "ZTree"

# create output directory                                                                                                                                                   
DIR = "/afs/cern.ch/work/e/elfontan/private/HZZ/Run2Legacy/CMSSW_10_3_1/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/jet_MET_Z_" + str(period) + str(treeText) + '/'
gSystem.Exec("mkdir -p " + DIR)
print "Output directory created!"


#********************
# Define histo Z->ee
#********************
leadingJet_Pt_data     = TH1F("leadingJet_Pt_data","leadingJet_Pt_data",      27, 30, 300)
leadingJet_Pt_MC       = TH1F("leadingJet_Pt_MC","leadingJet_Pt_MC",          27, 30, 300)
leadingJet_Pt_MCup     = TH1F("leadingJet_Pt_MCup","leadingJet_Pt_MCup",      27, 30, 300)
leadingJet_Pt_MCdn     = TH1F("leadingJet_Pt_MCdn","leadingJet_Pt_MCdn",      27, 30, 300)

leadingJet_Eta_data    = TH1F("leadingJet_Eta_data","leadingJet_Eta_data",      47, -4.7, 4.7)
leadingJet_Eta_MC      = TH1F("leadingJet_Eta_MC","leadingJet_Eta_MC",          47, -4.7, 4.7)
leadingJet_Eta_MCup    = TH1F("leadingJet_Eta_MCup","leadingJet_Eta_MCup",      47, -4.7, 4.7)
leadingJet_Eta_MCdn    = TH1F("leadingJet_Eta_MCdn","leadingJet_Eta_MCdn",      47, -4.7, 4.7)

nJetsPt30_data     = TH1I("nJetsPt30_data","nJetsPt30_data",      6, 0, 6)
nJetsPt30_MC       = TH1I("nJetsPt30_MC","nJetsPt30_MC",          6, 0, 6)
nJetsPt30_MCup     = TH1I("nJetsPt30_MCup","nJetsPt30_MCup",      6, 0, 6)
nJetsPt30_MCdn     = TH1I("nJetsPt30_MCdn","nJetsPt30_MCdn",      6, 0, 6)

PFMET_data     = TH1F("PFMET_data","PFMET_data",      17, 0, 170)
PFMET_MC       = TH1F("PFMET_MC","PFMET_MC",          17, 0, 170)
PFMET_MCup     = TH1F("PFMET_MCup","PFMET_MCup",      17, 0, 170)
PFMET_MCdn     = TH1F("PFMET_MCdn","PFMET_MCdn",      17, 0, 170)


print 'Reading file', fDY.GetName(),'...'
n_events = 0

for event in tDY:
        n_events+=1
	nJetsUp = 0
	nJetsDn = 0
	highest_up = 0.
	highest_dn = 0.
	i_up = 0
	i_dn = 0
        if(n_events % int((tDY.GetEntries()/10)) == 0):
                print "{} %".format(str(100*n_events/tDY.GetEntries() + 1))

	#if (event.LepPt.at(0) < 30 or event.LepPt.at(1) < 30. or abs(event.LepLepId.at(0))!=11):
        #        continue
	if (event.LepPt.at(0) < 30. or event.LepPt.at(1) < 30.):
                continue
	if (event.ZMass < 70 or event.ZMass > 110):
		continue

	for jet in range(event.JetPt.size()):
		if (event.JetJERUp.at(jet)*(1+event.JetSigma.at(jet)) > highest_up):
			highest_up = event.JetJERUp.at(jet)*(1+event.JetSigma.at(jet))
			i_up = jet
		if (event.JetJERDown.at(jet)*(1-event.JetSigma.at(jet)) > highest_dn):
			highest_dn = event.JetJERDown.at(jet)*(1-event.JetSigma.at(jet))
			i_dn = jet
		if ( event.JetJERUp.at(jet)*(1+event.JetSigma.at(jet)) > 30.):
			nJetsUp += 1
		if ( event.JetJERDown.at(jet)*(1-event.JetSigma.at(jet)) > 30.):
			nJetsDn += 1

	if (event.JetPt.size() > 0 and event.JetPt.at(0) > 30.):
		leadingJet_Pt_MC.Fill(event.JetPt.at(0),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
		leadingJet_Eta_MC.Fill(event.JetEta.at(0),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	if (event.JetPt.size() > 0 and event.JetJERUp.at(i_up)*(1+event.JetSigma.at(i_up)) > 30.):
		leadingJet_Pt_MCup.Fill(event.JetPt.at(i_up),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
		leadingJet_Eta_MCup.Fill(event.JetEta.at(i_up),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	if (event.JetPt.size() > 0 and event.JetJERDown.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30.):
		leadingJet_Pt_MCdn.Fill(event.JetPt.at(i_dn),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
		leadingJet_Eta_MCdn.Fill(event.JetEta.at(i_dn),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)

	nJetsPt30_MC.Fill(event.nCleanedJetsPt30,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	nJetsPt30_MCup.Fill(nJetsUp,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	nJetsPt30_MCdn.Fill(nJetsDn,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)

	PFMET_MC.Fill(event.PFMET,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_MCup.Fill(event.PFMET_jesUp,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_MCdn.Fill(event.PFMET_jesDn,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)


print 'Reading file', fTT.GetName(),'...'
n_events=0

for event in tTT:
        n_events+=1
	nJetsUp = 0
	nJetsDn = 0
	highest_up = 0.
	highest_dn = 0.
	i_up = 0
	i_dn = 0
        if(n_events % int((tTT.GetEntries()/10)) == 0):
                print "{} %".format(str(100*n_events/tTT.GetEntries() + 1))

	#if (event.LepPt.at(0) < 30 or event.LepPt.at(1) < 30. or abs(event.LepLepId.at(0))!=11):
	if (event.LepPt.at(0) < 30 or event.LepPt.at(1) < 30.):
		continue
	if (event.ZMass < 70 or event.ZMass > 110):
		continue

	for jet in range(event.JetPt.size()):
		if (event.JetJERUp.at(jet)*(1+event.JetSigma.at(jet)) > highest_up):
			highest_up = event.JetJERUp.at(jet)*(1+event.JetSigma.at(jet))
			i_up = jet
		if (event.JetJERDown.at(jet)*(1-event.JetSigma.at(jet)) > highest_dn):
			highest_dn = event.JetJERDown.at(jet)*(1-event.JetSigma.at(jet))
			i_dn = jet
		if ( event.JetJERUp.at(jet)*(1+event.JetSigma.at(jet)) > 30.):
			nJetsUp += 1
		if ( event.JetJERDown.at(jet)*(1-event.JetSigma.at(jet)) > 30.):
			nJetsDn += 1

	if (event.JetPt.size() > 0 and event.JetPt.at(0) > 30.):
		leadingJet_Pt_MC.Fill(event.JetPt.at(0),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
		leadingJet_Eta_MC.Fill(event.JetEta.at(0),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	if (event.JetPt.size() > 0 and event.JetJERUp.at(i_up)*(1+event.JetSigma.at(i_up)) > 30.):
		leadingJet_Pt_MCup.Fill(event.JetPt.at(i_up),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
		leadingJet_Eta_MCup.Fill(event.JetEta.at(i_up),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	if (event.JetPt.size() > 0 and event.JetJERDown.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30.):
		leadingJet_Pt_MCdn.Fill(event.JetPt.at(i_dn),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
		leadingJet_Eta_MCdn.Fill(event.JetEta.at(i_dn),event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)

	nJetsPt30_MC.Fill(event.nCleanedJetsPt30,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	nJetsPt30_MCup.Fill(nJetsUp,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	nJetsPt30_MCdn.Fill(nJetsDn,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)

	PFMET_MC.Fill(event.PFMET,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_MCup.Fill(event.PFMET_jesUp,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_MCdn.Fill(event.PFMET_jesDn,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)


print 'Reading file', fdata.GetName(),'...'
#tdata.Draw("JetPt[0] >> leadingJet_Pt_data","nCleanedJetsPt30 > 0 && (ZMass > 70 && ZMass < 110) && (LepPt[0] > 30 && LepPt[1] > 30) && abs(LepLepId[0])==11")
#tdata.Draw("JetEta[0] >> leadingJet_Eta_data","nCleanedJetsPt30 > 0 && (ZMass > 70 && ZMass < 110) && (LepPt[0] > 30 && LepPt[1] > 30) && abs(LepLepId[0])==11")
#tdata.Draw("nCleanedJetsPt30 >> nJetsPt30_data","(ZMass > 70 && ZMass < 110) && (LepPt[0] > 30 && LepPt[1] > 30) && abs(LepLepId[0])==11")
#tdata.Draw("PFMET >> PFMET_data","(ZMass > 70 && ZMass < 110) && (LepPt[0] > 30 && LepPt[1] > 30) && abs(LepLepId[0])==11")
#tdata.Draw("ZMass >> ZMass_data","(ZMass > 70 && ZMass < 110) && (LepPt[0] > 30 && LepPt[1] > 30) && abs(LepLepId[0])==11")
tdata.Draw("JetPt[0] >> leadingJet_Pt_data",     "nCleanedJetsPt30 > 0 && JetPt[0] > 30. && (ZMass > 70 && ZMass < 110) && (LepPt[0] > 30 && LepPt[1] > 30)")
tdata.Draw("JetEta[0] >> leadingJet_Eta_data",   "nCleanedJetsPt30 > 0 && JetPt[0] > 30. && (ZMass > 70 && ZMass < 110) && (LepPt[0] > 30 && LepPt[1] > 30)")
tdata.Draw("nCleanedJetsPt30 >> nJetsPt30_data", "(ZMass > 70 && ZMass < 110) && (LepPt[0] > 30 && LepPt[1] > 30)")
tdata.Draw("PFMET >> PFMET_data",                "(ZMass > 70 && ZMass < 110) && (LepPt[0] > 30 && LepPt[1] > 30)")


c = ROOT.TCanvas()
DrawRatioPlot(DIR+"leadingJet_Pt", "Leading jet p_{T}", "Events/10 GeV", c, leadingJet_Pt_data, leadingJet_Pt_MC, leadingJet_Pt_MCup, leadingJet_Pt_MCdn, True)
DrawRatioPlot(DIR+"leadingJet_Eta", "Leading jet #eta", "Events/0.2", c, leadingJet_Eta_data, leadingJet_Eta_MC, leadingJet_Eta_MCup, leadingJet_Eta_MCdn, False)
DrawRatioPlot(DIR+"nCleanedJetsPt30", "# Jets Pt > 30 GeV", "Events", c, nJetsPt30_data, nJetsPt30_MC, nJetsPt30_MCup, nJetsPt30_MCdn, True)
DrawRatioPlot(DIR+"PFMET", "PFMET", "Events/10 GeV", c, PFMET_data, PFMET_MC, PFMET_MCup, PFMET_MCdn, False)



