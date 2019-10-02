#!/usr/bin/env python

# *********************************************
# usage: 
#    python noJER_IDchecks_jets_issues
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
#period = "data2016"
period = "data2017"
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


# create output directory                                                                                                                                                   
DIR = "/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/noJER_" + period + "_IDchecks_jets_issues_ZTree/"
gSystem.Exec("mkdir -p " + DIR)
print "Output directory created!"

if (period == "data2016"):
        fDY = TFile.Open("/eos/home-h/hroskes/CJLST/190821/MC_2016/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")
        tDY = fDY.Get("ZTree/candTree")
        counterDY = fDY.Get("ZTree/Counters")
        SumWeight_DY = counterDY.GetBinContent(1)

        fTT = TFile.Open("/eos/home-h/hroskes/CJLST/190821/MC_2016/TTTo2L2Nu/ZZ4lAnalysis.root")
        tTT = fTT.Get("ZTree/candTree")
        counterTT = fTT.Get("ZTree/Counters")
        SumWeight_TT = counterTT.GetBinContent(1)

        fdata = TFile.Open("/eos/home-h/hroskes/CJLST/190821/Data_2016/AllData/ZZ4lAnalysis.root")
        tdata = fdata.Get("ZTree/candTree")
        lumi = 35.92 # /fb                                                                                                                                                             
        lumiText = "35.92 fb^{-1}"

elif (period == "data2017"):
        fDY = TFile.Open("/eos/home-h/hroskes/CJLST/190821/MC_2017/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")
        tDY = fDY.Get("ZTree/candTree")
        counterDY = fDY.Get("ZTree/Counters")
        SumWeight_DY = counterDY.GetBinContent(1)
        #tDY = fDY.Get("CRZLLTree/candTree")
        #counterDY = fDY.Get("CRZLLTree/Counters")
        #SumWeight_DY = counterDY.GetBinContent(40)

        fTT = TFile.Open("/eos/home-h/hroskes/CJLST/190821/MC_2017/TTTo2L2Nu/ZZ4lAnalysis.root")
        tTT = fTT.Get("ZTree/candTree")
        counterTT = fTT.Get("ZTree/Counters")
        SumWeight_TT = counterTT.GetBinContent(1)
        #tTT = fTT.Get("CRZLLTree/candTree")
        #counterTT = fTT.Get("CRZLLTree/Counters")
        #SumWeight_TT = counterTT.GetBinContent(40)

        fdata = TFile.Open("/eos/home-h/hroskes/CJLST/190821/Data_2017/AllData/ZZ4lAnalysis.root")
        tdata = fdata.Get("ZTree/candTree")
        #tdata = fdata.Get("CRZLLTree/candTree")
        lumi = 41.53 # /fb                                                                                                                                                             
        lumiText = "41.53 fb^{-1}"

elif (period == "data2018"):
        fDY = TFile.Open("/eos/home-h/hroskes/CJLST/190821/MC_2018/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")
        tDY = fDY.Get("ZTree/candTree")
        counterDY = fDY.Get("ZTree/Counters")
        SumWeight_DY = counterDY.GetBinContent(1)

        fTT = TFile.Open("/eos/home-h/hroskes/CJLST/190821/MC_2018/TTTo2L2Nu/ZZ4lAnalysis.root")
        tTT = fTT.Get("ZTree/candTree")
        counterTT = fTT.Get("ZTree/Counters")
        SumWeight_TT = counterTT.GetBinContent(1)

        fdata = TFile.Open("/eos/home-h/hroskes/CJLST/190821/Data_2018/AllData/ZZ4lAnalysis.root")
        tdata = fdata.Get("ZTree/candTree")
        lumi = 59.74 # /fb
        lumiText = "59.74 fb^{-1}"


#********************
# Define histo Z->ee
#********************
leadingJet_Eta_noID_data    = TH1F ("leadingJet_Eta_noID_data","leadingJet_Eta_noID_data",      47, -4.7, 4.7)
leadingJet_Eta_noID_MC      = TH1F ("leadingJet_Eta_noID_MC","leadingJet_Eta_noID_MC",          47, -4.7, 4.7)
leadingJet_Eta_noID_MCup    = TH1F ("leadingJet_Eta_noID_MCup","leadingJet_Eta_noID_MCup",      47, -4.7, 4.7)
leadingJet_Eta_noID_MCdn    = TH1F ("leadingJet_Eta_noID_MCdn","leadingJet_Eta_noID_MCdn",      47, -4.7, 4.7)

leadingJet_Eta_jetID_data    = TH1F ("leadingJet_Eta_jetID_data","leadingJet_Eta_jetID_data",   47, -4.7, 4.7)
leadingJet_Eta_jetID_MC      = TH1F ("leadingJet_Eta_jetID_MC","leadingJet_Eta_jetID_MC",       47, -4.7, 4.7)
leadingJet_Eta_jetID_MCup    = TH1F ("leadingJet_Eta_jetID_MCup","leadingJet_Eta_jetID_MCup",   47, -4.7, 4.7)
leadingJet_Eta_jetID_MCdn    = TH1F ("leadingJet_Eta_jetID_MCdn","leadingJet_Eta_jetID_MCdn",   47, -4.7, 4.7)

leadingJet_Eta_PUID_data    = TH1F ("leadingJet_Eta_PUID_data","leadingJet_Eta_PUID_data",      47, -4.7, 4.7)
leadingJet_Eta_PUID_MC      = TH1F ("leadingJet_Eta_PUID_MC","leadingJet_Eta_PUID_MC",          47, -4.7, 4.7)
leadingJet_Eta_PUID_MCup    = TH1F ("leadingJet_Eta_PUID_MCup","leadingJet_Eta_PUID_MCup",      47, -4.7, 4.7)
leadingJet_Eta_PUID_MCdn    = TH1F ("leadingJet_Eta_PUID_MCdn","leadingJet_Eta_PUID_MCdn",      47, -4.7, 4.7)

print 'Reading file', fDY.GetName(),'...'
n_events = 0

for event in tDY:
        #if (n_events == 100): break
        n_events+=1
        nJetsUp = 0
        nJetsDn = 0
        highest_up = 0.
        highest_dn = 0.
        i_up = 0
        i_dn = 0

        if(n_events % int((tDY.GetEntries()/50)) == 0):
                print "{} %".format(str(100*n_events/tDY.GetEntries() + 1))
                
        for jet in range(event.JetEta.size()):
                if (event.JetPtJEC_noJER.at(jet)*(1+event.JetSigma.at(jet)) > highest_up):
                        highest_up = event.JetPtJEC_noJER.at(jet)*(1+event.JetSigma.at(jet))
                        i_up = jet
                if (event.JetPtJEC_noJER.at(jet)*(1-event.JetSigma.at(jet)) > highest_dn):
                        highest_dn = event.JetPtJEC_noJER.at(jet)*(1-event.JetSigma.at(jet))
                        i_dn = jet
                if ( event.JetPtJEC_noJER.at(jet)*(1+event.JetSigma.at(jet)) > 30.):
                        nJetsUp += 1
                if ( event.JetPtJEC_noJER.at(jet)*(1-event.JetSigma.at(jet)) > 30.):
                        nJetsDn += 1

        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(0) > 30. and event.JetID.at(0) != 0 and event.JetPUID.at(0) != 0):
                leadingJet_Eta_PUID_MC.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_DY)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_up)*(1+event.JetSigma.at(i_up)) > 30. and event.JetID.at(i_up) != 0 and event.JetPUID.at(i_up) != 0):
                leadingJet_Eta_PUID_MCup.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_DY)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30. and event.JetID.at(i_dn) != 0 and event.JetPUID.at(i_dn) != 0):
                leadingJet_Eta_PUID_MCdn.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_DY)

        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(0) > 30. and event.JetID.at(0) != 0):
                leadingJet_Eta_jetID_MC.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_DY)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_up)*(1+event.JetSigma.at(i_up)) > 30. and event.JetID.at(i_up) != 0):
                leadingJet_Eta_jetID_MCup.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_DY)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30. and event.JetID.at(i_dn) != 0):
                leadingJet_Eta_jetID_MCdn.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_DY)

        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(0) > 30.):
                leadingJet_Eta_noID_MC.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_DY)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_up)*(1+event.JetSigma.at(i_up)) > 30.):
                leadingJet_Eta_noID_MCup.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_DY)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30.):
                leadingJet_Eta_noID_MCdn.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_DY)


print 'Reading file', fTT.GetName(),'...'

n_events = 0
for event in tTT:
        #if (n_events == 100): break
        n_events+=1
	nJetsUp = 0
	nJetsDn = 0
	highest_up = 0.
	highest_dn = 0.
	i_up = 0
	i_dn = 0

        if(n_events % int((tTT.GetEntries()/50)) == 0):
                print "{} %".format(str(100*n_events/tTT.GetEntries() + 1))

        for jet in range(event.JetEta.size()):
                if (event.JetPtJEC_noJER.at(jet)*(1+event.JetSigma.at(jet)) > highest_up):
                        highest_up = event.JetPtJEC_noJER.at(jet)*(1+event.JetSigma.at(jet))
                        i_up = jet
                if (event.JetPtJEC_noJER.at(jet)*(1-event.JetSigma.at(jet)) > highest_dn):
                        highest_dn = event.JetPtJEC_noJER.at(jet)*(1-event.JetSigma.at(jet))
                        i_dn = jet
                if ( event.JetPtJEC_noJER.at(jet)*(1+event.JetSigma.at(jet)) > 30.):
                        nJetsUp += 1
                if ( event.JetPtJEC_noJER.at(jet)*(1-event.JetSigma.at(jet)) > 30.):
                        nJetsDn += 1

        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(0) > 30. and event.JetID.at(0) != 0 and event.JetPUID.at(0) != 0):
                leadingJet_Eta_PUID_MC.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_TT)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_up)*(1+event.JetSigma.at(i_up)) > 30. and event.JetID.at(i_up) != 0 and event.JetPUID.at(i_up) != 0):
                leadingJet_Eta_PUID_MCup.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_TT)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30. and event.JetID.at(i_dn) != 0 and event.JetPUID.at(i_dn) != 0):
                leadingJet_Eta_PUID_MCdn.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_TT)

        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(0) > 30. and event.JetID.at(0) != 0):
                leadingJet_Eta_jetID_MC.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_TT)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_up)*(1+event.JetSigma.at(i_up)) > 30. and event.JetID.at(i_up) != 0):
                leadingJet_Eta_jetID_MCup.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_TT)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30. and event.JetID.at(i_dn) != 0):
                leadingJet_Eta_jetID_MCdn.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_TT)

        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(0) > 30.):
                leadingJet_Eta_noID_MC.Fill (event.JetEta.at(0), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_TT)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_up)*(1+event.JetSigma.at(i_up)) > 30.):
                leadingJet_Eta_noID_MCup.Fill (event.JetEta.at(i_up), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_TT)
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(i_dn)*(1-event.JetSigma.at(i_up)) > 30.):
                leadingJet_Eta_noID_MCdn.Fill (event.JetEta.at(i_dn), event.overallEventWeight*event.xsec*1000*lumi*event.L1prefiringWeight/SumWeight_TT)



print 'Reading file', fdata.GetName(),'...'

n_events = 0
for event in tdata:
        #if (n_events == 100): break
        n_events+=1
        if(n_events % int((tdata.GetEntries()/50)) == 0):
                print "{} %".format(str(100*n_events/tdata.GetEntries() + 1))

        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(0) > 30. and event.JetID.at(0) != 0 and event.JetPUID.at(0) != 0):
                leadingJet_Eta_PUID_data.Fill (event.JetEta.at(0))                        
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(0) > 30. and event.JetID.at(0) != 0):
                leadingJet_Eta_jetID_data.Fill (event.JetEta.at(0))                        
        if (event.JetEta.size() > 0 and event.JetPtJEC_noJER.at(0) > 30.):
                leadingJet_Eta_noID_data.Fill(event.JetEta.at(0))
                                                


print "Saving distributions into root file ..."
outFile = TFile.Open(DIR+"leadingJet_etaDistributions_" + period + "_ZTree.root", "RECREATE")
outFile.cd()
leadingJet_Eta_noID_data.Write()
leadingJet_Eta_jetID_data.Write()
leadingJet_Eta_PUID_data.Write()
leadingJet_Eta_noID_MC.Write()
leadingJet_Eta_noID_MCup.Write()
leadingJet_Eta_noID_MCdn.Write()
leadingJet_Eta_jetID_MC.Write()
leadingJet_Eta_jetID_MCup.Write()
leadingJet_Eta_jetID_MCdn.Write()
leadingJet_Eta_PUID_MC.Write()
leadingJet_Eta_PUID_MCup.Write()
leadingJet_Eta_PUID_MCdn.Write()

c = ROOT.TCanvas()
DrawRatioPlot(DIR+"noJER_leadingJetEta_NOjetID_NOpuID", "Leading jet #eta", "Events/0.2", c, leadingJet_Eta_noID_data, leadingJet_Eta_noID_MC, leadingJet_Eta_noID_MCup, leadingJet_Eta_noID_MCdn, False)
DrawRatioPlot(DIR+"noJER_leadingJetEta_jetID_NOpuID", "Leading jet #eta", "Events/0.2", c, leadingJet_Eta_jetID_data, leadingJet_Eta_jetID_MC, leadingJet_Eta_jetID_MCup, leadingJet_Eta_jetID_MCdn, False)
DrawRatioPlot(DIR+"noJER_leadingJetEta_jetID_PUID", "Leading jet #eta", "Events/0.2", c, leadingJet_Eta_PUID_data, leadingJet_Eta_PUID_MC, leadingJet_Eta_PUID_MCup, leadingJet_Eta_PUID_MCdn, False)


