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


# Data periods options
# *****************************
period = "data2016"
#period = "data2017"
#period = "data2018"
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
        #for bin in range (MC.GetSize() - 2):
        #        if ( MC.GetBinContent(bin + 1) > max):
        #                max = MC.GetBinContent(bin + 1)
        for bin in range (data.GetSize() - 2):
                if ( data.GetBinContent(bin + 1) > max):
                        max = data.GetBinContent(bin + 1)

        MC.SetMaximum(1.4*max)
        norm = data.Integral()/MC.Integral()   # Normalize MC to data        
        MC.Scale(norm)
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
        c.SaveAs(name+".root")
        
        c.Clear()


# create output directory                                                                                                                                                   
#DIR = "/afs/cern.ch/work/e/elfontan/private/HZZ/Run2Legacy/CMSSW_10_3_1/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/jet_MET_Z_" + str(period) + "_ZTree/"
DIR = "/afs/cern.ch/work/e/elfontan/private/HZZ/Run2Legacy/CMSSW_10_3_1/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/jet_MET_Z_" + str(period) + "_CRZLTree/"
gSystem.Exec("mkdir -p " + DIR)
print "Output directory created!"

if (period == "data2016"):
        fDY = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2016/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")
        #tDY = fDY.Get("ZTree/candTree")
        #counterDY = fDY.Get("ZTree/Counters")
        #SumWeight_DY = counterDY.GetBinContent(1)
        tDY = fDY.Get("CRZLTree/candTree")
        counterDY = fDY.Get("CRZLTree/Counters")
        SumWeight_DY = counterDY.GetBinContent(40)

        fTT = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2016/TTTo2L2Nu/ZZ4lAnalysis.root")
        #tTT = fTT.Get("ZTree/candTree")
        #counterTT = fTT.Get("ZTree/Counters")
        #SumWeight_TT = counterTT.GetBinContent(1)
        tTT = fTT.Get("CRZLTree/candTree")
        counterTT = fTT.Get("CRZLTree/Counters")
        SumWeight_TT = counterTT.GetBinContent(40)

        fdata = TFile.Open("root://lxcms03//data3/Higgs/190617/Data_2016/AllData/ZZ4lAnalysis.root")
        tdata = fdata.Get("ZTree/candTree")
        #tdata = fdata.Get("CRZLL/candTree")
        lumi = 35.92 # /fb
        lumiText = "35.92 fb^{-1}"

elif (period == "data2017"):
        fDY = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2017/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")
        #tDY = fDY.Get("ZTree/candTree")
        #counterDY = fDY.Get("ZTree/Counters")
        #SumWeight_DY = counterDY.GetBinContent(1)
        tDY = fDY.Get("CRZLTree/candTree")
        counterDY = fDY.Get("CRZLTree/Counters")
        SumWeight_DY = counterDY.GetBinContent(1)

        fTT = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2017/TTTo2L2Nu/ZZ4lAnalysis.root")
        #tTT = fTT.Get("ZTree/candTree")
        #counterTT = fTT.Get("ZTree/Counters")
        #SumWeight_TT = counterTT.GetBinContent(1)
        tTT = fTT.Get("CRZLTree/candTree")
        counterTT = fTT.Get("CRZLTree/Counters")
        SumWeight_TT = counterTT.GetBinContent(1)

        fdata = TFile.Open("root://lxcms03//data3/Higgs/190617/Data_2017/AllData/ZZ4lAnalysis.root")
        #tdata = fdata.Get("ZTree/candTree")
        tdata = fdata.Get("CRZLTree/candTree")
        lumi = 41.53 # /fb
        lumiText = "41.53 fb^{-1}"

elif (period == "data2018"):
        fDY = TFile.Open("/eos/user/t/tsculac/BigStuff/LegacyProduction_1/MC_2016/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")
        tDY = fDY.Get("ZTree/candTree")
        counterDY = fDY.Get("ZTree/Counters")
        SumWeight_DY = counterDY.GetBinContent(1)
        #SumWeight = (f1.Get("ZTree/Counters")).GetBinContent(1)

        fTT = TFile.Open("/eos/user/t/tsculac/BigStuff/LegacyProduction_1/MC_2016/TTTo2L2Nu/ZZ4lAnalysis.root")
        tTT = fTT.Get("ZTree/candTree")
        counterTT = fTT.Get("ZTree/Counters")
        SumWeight_TT = counterTT.GetBinContent(1)

        fdata = TFile.Open("/eos/user/t/tsculac/BigStuff/LegacyProduction_1/Data_2016/AllData/ZZ4lAnalysis.root")
        tdata = fdata.Get("ZTree/candTree")
        lumi = 59.74 # /fb
        lumiText = "59.74 fb^{-1}"


#********************
# Define histo Z->ee
#********************
PFMET_data     = TH1F("PFMET_data","PFMET_data",      20, 0, 200)
PFMET_MC       = TH1F("PFMET_MC","PFMET_MC",          20, 0, 200)
PFMET_MCup     = TH1F("PFMET_MCup","PFMET_MCup",      20, 0, 200)
PFMET_MCdn     = TH1F("PFMET_MCdn","PFMET_MCdn",      20, 0, 200)

PFMET_corrected_data     = TH1F("PFMET_corrected_data","PFMET_corrected_data",      20, 0, 200)
PFMET_corrected_MC       = TH1F("PFMET_corrected_MC","PFMET_corrected_MC",          20, 0, 200)
PFMET_corrected_MCup     = TH1F("PFMET_corrected_MCup","PFMET_corrected_MCup",      20, 0, 200)
PFMET_corrected_MCdn     = TH1F("PFMET_corrected_MCdn","PFMET_corrected_MCdn",      20, 0, 200)



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
	if (event.Z1Mass < 70 or event.Z1Mass > 110):
		continue

	PFMET_MC.Fill(event.PFMET,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_MCup.Fill(event.PFMET_jesUp,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_MCdn.Fill(event.PFMET_jesDn,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)

	PFMET_corrected_MC.Fill(event.PFMET_corrected,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MCup.Fill(event.PFMET_corrected_jesUp,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MCdn.Fill(event.PFMET_corrected_jesDn,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)

	#PFMET_MC.Fill(event.PFMET)
	#PFMET_MCup.Fill(event.PFMET_jesUp)
	#PFMET_MCdn.Fill(event.PFMET_jesDn)

	#PFMET_corrected_MC.Fill(event.PFMET_corrected)
	#PFMET_corrected_MCup.Fill(event.PFMET_corrected_jesUp)
	#PFMET_corrected_MCdn.Fill(event.PFMET_corrected_jesDn)

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
	if (event.Z1Mass < 70 or event.Z1Mass > 110):
		continue

	PFMET_MC.Fill(event.PFMET,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_MCup.Fill(event.PFMET_jesUp,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_MCdn.Fill(event.PFMET_jesDn,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)

	PFMET_corrected_MC.Fill(event.PFMET_corrected,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MCup.Fill(event.PFMET_corrected_jesUp,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MCdn.Fill(event.PFMET_corrected_jesDn,event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)

	#PFMET_MC.Fill(event.PFMET)
	#PFMET_MCup.Fill(event.PFMET_jesUp)
	#PFMET _MCdn.Fill(event.PFMET_jesDn)

        #PFMET_corrected_MC.Fill(event.PFMET_corrected)
	#PFMET_corrected_MCup.Fill(event.PFMET_corrected_jesUp)
	#PFMET_corrected_MCdn.Fill(event.PFMET_corrected_jesDn)


print 'Reading file', fdata.GetName(),'...'
tdata.Draw("PFMET >> PFMET_data",                      "(Z1Mass > 70 && Z1Mass < 110) && (LepPt[0] > 30 && LepPt[1] > 30)")
tdata.Draw("PFMET_corrected >> PFMET_corrected_data",  "(Z1Mass > 70 && Z1Mass < 110) && (LepPt[0] > 30 && LepPt[1] > 30)")


c = ROOT.TCanvas()
DrawRatioPlot(DIR+"PFMET", "PFMET", "Events/10 GeV", c, PFMET_data, PFMET_MC, PFMET_MCup, PFMET_MCdn, False)
DrawRatioPlot(DIR+"PFMET_corrected", "PFMET_corrected", "Events/10 GeV", c, PFMET_corrected_data, PFMET_corrected_MC, PFMET_corrected_MCup, PFMET_corrected_MCdn, False)



