#!/usr/bin/env python

# *************************************
# usage: 
#    python IDeffect_comparison.py
#
# *************************************

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
# Data periods options
# *****************************
#period = "data2016"
period = "data2017"
#period = "data2018"
# *****************************
if (period == "data2016"):
        lumiText = "35.92 fb^{-1}"

elif (period == "data2017"):
        lumiText = "41.53 fb^{-1}"

elif (period == "data2018"):
        lumiText = "59.74 fb^{-1}"
else:
        print ("Error: wrong option!")

# create output directory                                                                                                         
DIR = "/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/" + period + "_IDchecks_jets_issues_ZTree/"
gSystem.Exec("mkdir -p " + DIR)
print "Output directory created: " + str(DIR)

# Open file and get histos                                                                                                                                             
filename = "f_"+period
filename = TFile.Open(DIR+"leadingJet_etaDistributions_" + period + "_ZTree.root")
h_noID_data  = filename.Get("leadingJet_Eta_noID_data")
h_jetID_data = filename.Get("leadingJet_Eta_jetID_data")
h_PUID_data  = filename.Get("leadingJet_Eta_PUID_data")
h_noID_MC    = filename.Get("leadingJet_Eta_noID_MC")
h_jetID_MC   = filename.Get("leadingJet_Eta_jetID_MC")
h_PUID_MC    = filename.Get("leadingJet_Eta_PUID_MC")


c_data = ROOT.TCanvas()
c_data.cd()

#h_noID_data.SetMaximum(1.5*max)
h_noID_data.GetXaxis().SetTitle("#eta leading jet")
h_noID_data.GetYaxis().SetTitleSize(0.05)
h_noID_data.GetYaxis().SetTitleOffset(1.)
h_noID_data.GetYaxis().SetTitle("Events/0.2")
h_noID_data.SetLineWidth(3)
h_noID_data.SetLineColor(kAzure-3)
h_noID_data.DrawNormalized("hist")

h_jetID_data.SetLineWidth(3)
h_jetID_data.SetLineColor(kOrange-3)
h_jetID_data.DrawNormalized("hist same")

h_PUID_data.SetLineWidth(3)
h_PUID_data.SetLineColor(kRed)
h_PUID_data.DrawNormalized("hist same")

#leg = TLegend(.1,.7,.45,.88)
leg = TLegend(.35,.7,.65,.88)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.04)
leg.AddEntry(h_noID_data, "NO jet ID + NO PU ID", "f" )
leg.AddEntry(h_jetID_data, "jet ID + NO PU ID", "f" )
leg.AddEntry(h_PUID_data, "jet ID + PU ID", "f" )
leg.Draw()

#draw CMS and lumi text                                                              
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = lumiText + " (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_data, 0, 0)

c_data.SaveAs(DIR+"JetEta_data_IDcomparison_"+period+".pdf")
c_data.SaveAs(DIR+"JetEta_data_IDcomparison_"+period+".png")



c_MC = ROOT.TCanvas()
c_MC.cd()

#h_noID_MC.SetMaximum(1.5*max)
h_PUID_MC.GetXaxis().SetTitle("#eta leading jet")
h_PUID_MC.GetYaxis().SetTitleSize(0.05)
h_PUID_MC.GetYaxis().SetTitleOffset(1.)
h_PUID_MC.GetYaxis().SetTitle("Events/0.2")
h_PUID_MC.SetLineWidth(3)
h_PUID_MC.SetLineColor(kRed)
h_PUID_MC.DrawNormalized("hist")

h_jetID_MC.SetLineWidth(3)
h_jetID_MC.SetLineColor(kOrange-3)
h_jetID_MC.DrawNormalized("hist same")

h_noID_MC.SetLineWidth(3)
h_noID_MC.SetLineColor(kAzure-3)
h_noID_MC.DrawNormalized("hist same")

leg.Draw()

#draw CMS and lumi text                                                              
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = lumiText + " (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(c_MC, 0, 0)

c_MC.SaveAs(DIR+"JetEta_MC_IDcomparison_"+period+".pdf")
c_MC.SaveAs(DIR+"JetEta_MC_IDcomparison_"+period+".png")

