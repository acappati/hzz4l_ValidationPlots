#!/usr/bin/env python

# ***********************
# usage: 
#    python prefiring.py
#
# ***********************

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
ZZTree  = True
ZTree     = False
# *****************************                                                                                                                                         
# Data periods options                                                                                                                                                    
# *****************************                                                                                                                                          
period = "data2016"                                                                                                                                                        
#period = "data2017"                                                                                                                                              
#period = "data2018"
# *****************************      

def DrawRatioPlot(name, sample, xaxis_title, yaxis_title, c, data, MC, MCUp, MCDn, logscale):
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
    
        Ratio    = TH1F ("Ratio", "Ratio", MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_up = TH1F ("sigma_up", "sigma_up", MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_dn = TH1F ("sigma_dn", "sigma_dn", MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())

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
        leg.AddEntry(MC, sample, "f" )
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
        fdata   = TFile.Open  ("/eos/home-h/hroskes/CJLST/190821/Data_2016/AllData/ZZ4lAnalysis.root")
        fGGH    = TFile.Open  ("/eos/home-h/hroskes/CJLST/190821/MC_2016/ggH125/ZZ4lAnalysis.root")
        fVBF    = TFile.Open  ("/eos/home-h/hroskes/CJLST/190821/MC_2016/VBFH125/ZZ4lAnalysis.root")
        lumi = 35.92 # /fb
        lumiText = "35.92 fb^{-1}"

        if (ZZTree):
                tGGH = fGGH.Get("ZZTree/candTree")
                counterGGH = fGGH.Get("ZZTree/Counters")
                SumWeight_GGH = counterGGH.GetBinContent(40)
                tVBF = fVBF.Get("ZZTree/candTree")
                counterVBF = fVBF.Get("ZZTree/Counters")
                SumWeight_VBF = counterVBF.GetBinContent(40)
                tdata = fdata.Get("ZZTree/candTree")
                treeText = "ZZTree"

        elif (ZTree):
                tGGH = fGGH.Get("ZTree/candTree")
                counterGGH = fGGH.Get("ZTree/Counters")
                SumWeight_GGH = counterGGH.GetBinContent(1)
                tVBF = fVBF.Get("ZTree/candTree")
                counterVBF = fVBF.Get("ZTree/Counters")
                SumWeight_VBF = counterVBF.GetBinContent(1)
                tdata = fdata.Get("ZTree/candTree")
                treeText = "ZTree"

elif (period == "data2017"):
        fdata   = TFile.Open  ("/eos/home-h/hroskes/CJLST/190821/Data_2017/AllData/ZZ4lAnalysis.root")
        fGGH    = TFile.Open  ("/eos/home-h/hroskes/CJLST/190821/MC_2017/ggH125/ZZ4lAnalysis.root")
        fVBF    = TFile.Open  ("/eos/home-h/hroskes/CJLST/190821/MC_2017/VBFH125/ZZ4lAnalysis.root")
        lumi = 41.53 # /fb
        lumiText = "41.53 fb^{-1}"

        if (ZZTree):
                tGGH = fGGH.Get("ZZTree/candTree")
                counterGGH = fGGH.Get("ZZTree/Counters")
                SumWeight_GGH = counterGGH.GetBinContent(40)
                tVBF = fVBF.Get("ZZTree/candTree")
                counterVBF = fVBF.Get("ZZTree/Counters")
                SumWeight_VBF = counterVBF.GetBinContent(40)
                tdata = fdata.Get("ZZTree/candTree")
                treeText = "ZZTree"

        elif (ZTree):
                tGGH = fGGH.Get("ZTree/candTree")
                counterGGH = fGGH.Get("ZTree/Counters")
                SumWeight_GGH = counterGGH.GetBinContent(1)
                tVBF = fVBF.Get("ZTree/candTree")
                counterVBF = fVBF.Get("ZTree/Counters")
                SumWeight_VBF = counterVBF.GetBinContent(1)
                tdata = fdata.Get("ZTree/candTree")
                treeText = "ZTree"

elif (period == "data2018"):
        fdata   = TFile.Open  ("/eos/home-h/hroskes/CJLST/190821/Data_2018/AllData/ZZ4lAnalysis.root")
        fGGH    = TFile.Open  ("/eos/home-h/hroskes/CJLST/190821/MC_2018/ggH125/ZZ4lAnalysis.root")
        fVBF    = TFile.Open  ("/eos/home-h/hroskes/CJLST/190821/MC_2018/VBFH125/ZZ4lAnalysis.root")
        lumi = 59.74 # /fb
        lumiText = "59.74 fb^{-1}"

        if (ZZTree):
                tGGH = fGGH.Get("ZZTree/candTree")
                counterGGH = fGGH.Get("ZZTree/Counters")
                SumWeight_GGH = counterGGH.GetBinContent(40)
                tVBF = fVBF.Get("ZZTree/candTree")
                counterVBF = fVBF.Get("ZZTree/Counters")
                SumWeight_VBF = counterVBF.GetBinContent(40)
                tdata = fdata.Get("ZZTree/candTree")
                treeText = "ZZTree"

        elif (ZTree):
                tGGH = fGGH.Get("ZTree/candTree")
                counterGGH = fGGH.Get("ZTree/Counters")
                SumWeight_GGH = counterGGH.GetBinContent(1)
                tVBF = fVBF.Get("ZTree/candTree")
                counterVBF = fVBF.Get("ZTree/Counters")
                SumWeight_VBF = counterVBF.GetBinContent(1)
                tdata = fdata.Get("ZTree/candTree")
                treeText = "ZTree"

# create output directory                                                                                                                     
DIR = "/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/PROVAPROVAPROVA_Prefiring_check_" + period + "_" + str(treeText) + "/"
gSystem.Exec("mkdir -p " + DIR)
print "Output directory created: " + str(DIR)


#********************
# Define histo Z->ee
#********************
leadingJet_Eta_data     = TH1F("leadingJet_Eta_data","leadingJet_Eta_data",         45, -4.5, 4.5)

leadingJet_Eta_ggH_MC   = TH1F("leadingJet_Eta_ggH_MC","leadingJet_Eta_ggH_MC",     45, -4.5, 4.5)
leadingJet_Eta_ggH_MCup = TH1F("leadingJet_Eta_ggH_MCup","leadingJet_Eta_ggH_MCup", 45, -4.5, 4.5)
leadingJet_Eta_ggH_MCdn = TH1F("leadingJet_Eta_ggH_MCdn","leadingJet_Eta_ggH_MCdn", 45, -4.5, 4.5)
leadingJet_Eta_ggH_MC_w   = TH1F("leadingJet_Eta_ggH_MC_w","leadingJet_Eta_ggH_MC_w",     45, -4.5, 4.5)
leadingJet_Eta_ggH_MCup_w = TH1F("leadingJet_Eta_ggH_MCup_w","leadingJet_Eta_ggH_MCup_w", 45, -4.5, 4.5)
leadingJet_Eta_ggH_MCdn_w = TH1F("leadingJet_Eta_ggH_MCdn_w","leadingJet_Eta_ggH_MCdn_w", 45, -4.5, 4.5)

leadingJet_Eta_VBF_MC   = TH1F("leadingJet_Eta_VBF_MC","leadingJet_Eta_VBF_MC",     45, -4.5, 4.5)
leadingJet_Eta_VBF_MCup = TH1F("leadingJet_Eta_VBF_MCup","leadingJet_Eta_VBF_MCup", 45, -4.5, 4.5)
leadingJet_Eta_VBF_MCdn = TH1F("leadingJet_Eta_VBF_MCdn","leadingJet_Eta_VBF_MCdn", 45, -4.5, 4.5)
leadingJet_Eta_VBF_MC_w   = TH1F("leadingJet_Eta_VBF_MC_w","leadingJet_Eta_VBF_MC",     45, -4.5, 4.5)
leadingJet_Eta_VBF_MCup_w = TH1F("leadingJet_Eta_VBF_MCup_w","leadingJet_Eta_VBF_MCup_w", 45, -4.5, 4.5)
leadingJet_Eta_VBF_MCdn_w = TH1F("leadingJet_Eta_VBF_MCdn_w","leadingJet_Eta_VBF_MCdn_w", 45, -4.5, 4.5)


print 'Reading file', fGGH.GetName(),'...'
n_events = 0

for event in tGGH:
        n_events+=1
	nJetsUp = 0
	nJetsDn = 0
	highest_up = 0.
	highest_dn = 0.
	i_up = 0
	i_dn = 0
        if(n_events % int((tGGH.GetEntries()/10)) == 0):
                print "{} %".format(str(100*n_events/tGGH.GetEntries() + 1))

	#if (event.LepPt.at(0) < 30. or event.LepPt.at(1) < 30.):
        #        continue
	#if (event.Z1Mass < 70 or event.Z1Mass > 110):
	#	continue

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
		leadingJet_Eta_ggH_MC.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi/SumWeight_GGH)
		leadingJet_Eta_ggH_MC_w.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_GGH)
	if (event.JetPt.size() > 0 and event.JetJERUp.at(i_up)*(1+event.JetSigma.at(i_up)) > 30.):
		leadingJet_Eta_ggH_MCup.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi/SumWeight_GGH)
		leadingJet_Eta_ggH_MCup_w.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeightUp/SumWeight_GGH)
	if (event.JetPt.size() > 0 and event.JetJERDown.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30.):
		leadingJet_Eta_ggH_MCdn.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi/SumWeight_GGH)
		leadingJet_Eta_ggH_MCdn_w.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeightDn/SumWeight_GGH)

print 'Reading file', fVBF.GetName(),'...'
n_events=0

for event in tVBF:
        n_events+=1
	nJetsUp = 0
	nJetsDn = 0
	highest_up = 0.
	highest_dn = 0.
	i_up = 0
	i_dn = 0
        if(n_events % int((tVBF.GetEntries()/10)) == 0):
                print "{} %".format(str(100*n_events/tVBF.GetEntries() + 1))

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
		leadingJet_Eta_VBF_MC.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi/SumWeight_VBF)
		leadingJet_Eta_VBF_MC_w.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_VBF)
	if (event.JetPt.size() > 0 and event.JetJERUp.at(i_up)*(1+event.JetSigma.at(i_up)) > 30.):
		leadingJet_Eta_VBF_MCup.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi/SumWeight_VBF)
		leadingJet_Eta_VBF_MCup_w.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeightUp/SumWeight_VBF)
	if (event.JetPt.size() > 0 and event.JetJERDown.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30.):
		leadingJet_Eta_VBF_MCdn.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi/SumWeight_VBF)
		leadingJet_Eta_VBF_MCdn_w.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeightDn/SumWeight_VBF)


print 'Reading file', fdata.GetName(),'...'

for event in tdata:
        if (event.JetPt.size() > 0 and event.JetPt.at(0) > 30.):
                leadingJet_Eta_data.Fill (event.JetEta.at(0))


#c = ROOT.TCanvas()
#DrawRatioPlot(DIR+"leadingJet_Eta_GGH", "ggH125", "Leading jet #eta", "Events/0.2", c, leadingJet_Eta_data, leadingJet_Eta_ggH_MC, leadingJet_Eta_ggH_MCup, leadingJet_Eta_ggH_MCdn, False)
#DrawRatioPlot(DIR+"leadingJet_Eta_VBF", "VBFH125", "Leading jet #eta", "Events/0.2", c, leadingJet_Eta_data, leadingJet_Eta_VBF_MC, leadingJet_Eta_VBF_MCup, leadingJet_Eta_VBF_MCdn, False)
#DrawRatioPlot(DIR+"leadingJet_Eta_GGH_w", "ggH125_pref", "Leading jet #eta", "Events/0.2", c, leadingJet_Eta_data, leadingJet_Eta_ggH_MC_w, leadingJet_Eta_ggH_MCup_w, leadingJet_Eta_ggH_MCdn_w, False)
#DrawRatioPlot(DIR+"leadingJet_Eta_VBF_w", "VBFH125_pref", "Leading jet #eta", "Events/0.2", c, leadingJet_Eta_data, leadingJet_Eta_VBF_MC_w, leadingJet_Eta_VBF_MCup_w, leadingJet_Eta_VBF_MCdn_w, False)


outFile = TFile.Open(DIR+"OK_JetEta_" + period + "_" + treeText + ".root", "RECREATE")
print "Saving histos into root file " + outFile.GetName() + "..."
outFile.cd()
leadingJet_Eta_data.Write()
leadingJet_Eta_ggH_MC.Write()
leadingJet_Eta_ggH_MCup.Write()
leadingJet_Eta_ggH_MCdn.Write()
leadingJet_Eta_ggH_MC_w.Write()
leadingJet_Eta_ggH_MCup_w.Write()
leadingJet_Eta_ggH_MCdn_w.Write()
leadingJet_Eta_VBF_MC.Write()
leadingJet_Eta_VBF_MCup.Write()
leadingJet_Eta_VBF_MCdn.Write()
leadingJet_Eta_VBF_MC_w.Write()
leadingJet_Eta_VBF_MCup_w.Write()
leadingJet_Eta_VBF_MCdn_w.Write()
outFile.Close()
