#!/usr/bin/env python

# ***************************
# usage: 
#    python JetEta_PLOTTER.py
#
# ***************************

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
#period = "data2017"
period = "data2018"
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
DIR = "/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/Prefiring_check_" + period + "_ZZTree/"
gSystem.Exec("mkdir -p " + DIR)
print "Output directory created: " + str(DIR)

# Open file and get histos                                                                                                                                             
filename = "f_"+period
filename = TFile.Open(DIR+"OK_JetEta_" + period + "_ZZTree.root")
h_GGH    = filename.Get("leadingJet_Eta_ggH_MC")
h_GGH_w  = filename.Get("leadingJet_Eta_ggH_MC_w")
h_VBF    = filename.Get("leadingJet_Eta_VBF_MC")
h_VBF_w  = filename.Get("leadingJet_Eta_VBF_MC_w")
#h_data   = filename.Get("leadingJet_Eta_data")

c_GGH = ROOT.TCanvas("c_GGH", "c_GGH", 800, 800)
c_GGH.cd()
#upper plot pad                                                                                                                                                                                         
pad1_GGH = TPad("pad1_GGH","pad1_GGH", 0, 0.3, 1, 1.0)
pad1_GGH.Draw()
pad1_GGH.cd()

max = 0.
for bin in range (h_GGH.GetSize() - 2):
        if ( h_GGH.GetBinContent(bin + 1) > max):
                max = h_GGH.GetBinContent(bin + 1)

h_GGH.SetMaximum(1.5*max)
h_GGH.GetXaxis().SetTitle("#eta leading jet")
h_GGH.GetYaxis().SetTitleSize(0.05)
h_GGH.GetYaxis().SetTitleOffset(1.2)
h_GGH.GetYaxis().SetTitle("Events/0.2")
h_GGH.SetMarkerStyle(21)
h_GGH.SetMarkerColor(kRed)
h_GGH.SetMarkerSize(1.2)
#h_GGH.Scale(1./(h_GGH.Integral()))
h_GGH.Draw("hist p")

h_GGH_w.SetMarkerStyle(47)
h_GGH_w.SetMarkerColor(kBlue)
h_GGH_w.SetMarkerSize(1.2)
#h_GGH_w.Scale(1./(h_GGH_w.Integral()))
h_GGH_w.Draw("hist p SAME")

leg1 = TLegend(.65,.75,.87,.85)
leg1.SetBorderSize(0)
leg1.SetFillColor(0)
leg1.SetFillStyle(0)
leg1.SetTextFont(42)
leg1.SetTextSize(0.04)
leg1.AddEntry(h_GGH, "ggH125", "p" )
leg1.AddEntry(h_GGH_w, "ggH125_pref", "p" )
leg1.Draw()

c_GGH.Update()

#lower plot pad                                                                                                                                                                                         
c_GGH.cd()
pad2_GGH = TPad("pad2_GGH","pad2_GGH", 0, 0.05, 1, 0.3)
pad2_GGH.SetGridy()
pad2_GGH.Draw()
pad2_GGH.cd()    #pad2 becomes the current pad                                                                             

#define ratio plot                                                                                                                                                                                      
rp = TH1F(h_GGH_w.Clone("rp"))
rp.SetLineColor(kBlack)
rp.SetMinimum(0.5)
rp.SetMaximum(2.)
rp.SetStats(0)
rp.Divide(h_GGH)   # divide MC histos                                                                                                                                     
rp.SetMarkerColor(kBlack)
rp.SetMarkerStyle(24)
rp.SetTitle("")

rp.SetYTitle("MC_pref / MC")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(20)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(1.4)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(15)

rp.GetXaxis().SetTitleSize(20)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(4.)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(15)
rp.Draw("ep")

#draw CMS and lumi text                                                              
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = lumiText + " (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(pad1_GGH, 0, 0)

c_GGH.Update()

c_GGH.SaveAs(DIR+"JetEta_GGH_"+period+"_ZZTree_ratio.pdf")
c_GGH.SaveAs(DIR+"JetEta_GGH_"+period+"_ZZTree_ratio.png")


c_VBF = ROOT.TCanvas("c_VBF", "c_VBF", 800, 800)
c_VBF.cd()
#upper plot pad                                                                                                                                                                                         
pad1_VBF = TPad("pad1_VBF","pad1_VBF", 0, 0.3, 1, 1.0)
pad1_VBF.Draw()
pad1_VBF.cd()
max = 0.
for bin in range (h_VBF.GetSize() - 2):
        if ( h_VBF.GetBinContent(bin + 1) > max):
                max = h_VBF.GetBinContent(bin + 1)

h_VBF.SetMaximum(1.5*max)
h_VBF.GetXaxis().SetTitle("#eta leading jet")
h_VBF.GetYaxis().SetTitleSize(0.04)
h_VBF.GetYaxis().SetTitleOffset(1.2)
h_VBF.GetYaxis().SetTitle("Events/0.2")
h_VBF.SetMarkerStyle(21)
h_VBF.SetMarkerColor(kRed)
h_VBF.SetMarkerSize(1.2)
h_VBF.Draw("hist p")

h_VBF_w.SetMarkerStyle(47)
h_VBF_w.SetMarkerColor(kBlue)
h_VBF_w.SetMarkerSize(1.2)
h_VBF_w.Draw("hist p SAME")

leg2 = TLegend(.65,.75,.87,.85)
leg2.SetBorderSize(0)
leg2.SetFillColor(0)
leg2.SetFillStyle(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.04)
leg2.AddEntry(h_VBF, "VBFH125", "p" )
leg2.AddEntry(h_VBF_w, "VBFH125_pref", "p" )
leg2.Draw()

c_VBF.Update()

#lower plot pad                                                                                                                                                                                         
c_VBF.cd()
pad2_VBF = TPad("pad2_VBF","pad2_VBF", 0, 0.05, 1, 0.3)
pad2_VBF.SetGridy()
pad2_VBF.Draw()
pad2_VBF.cd()    #pad2 becomes the current pad                                                                                                                              

#define ratio plot                                                                                                                                                                                      
rp = TH1F(h_VBF_w.Clone("rp"))
rp.SetLineColor(kBlack)
rp.SetMinimum(0.5)
rp.SetMaximum(2.)
rp.SetStats(0)
rp.Divide(h_VBF)   # divide MC histos                                                                                                                                     
rp.SetMarkerColor(kBlack)
rp.SetMarkerStyle(24)
rp.SetTitle("")

rp.SetYTitle("MC_pref / MC")
rp.GetYaxis().SetNdivisions(505)
rp.GetYaxis().SetTitleSize(20)
rp.GetYaxis().SetTitleFont(43)
rp.GetYaxis().SetTitleOffset(1.4)
rp.GetYaxis().SetLabelFont(43)
rp.GetYaxis().SetLabelSize(15)

rp.GetXaxis().SetTitleSize(20)
rp.GetXaxis().SetTitleFont(43)
rp.GetXaxis().SetTitleOffset(4.)
rp.GetXaxis().SetLabelFont(43)
rp.GetXaxis().SetLabelSize(15)
rp.Draw("ep")

#draw CMS and lumi text                                                              
CMS_lumi.writeExtraText = True
CMS_lumi.extraText      = "Preliminary"
CMS_lumi.lumi_sqrtS     = lumiText + " (13 TeV)"
CMS_lumi.cmsTextSize    = 0.6
CMS_lumi.lumiTextSize   = 0.46
CMS_lumi.extraOverCmsTextSize = 0.75
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(pad1_VBF, 0, 0)

c_VBF.Update()

c_VBF.SaveAs(DIR+"JetEta_VBF_"+period+"_ZZTree_ratio.pdf")
c_VBF.SaveAs(DIR+"JetEta_VBF_"+period+"_ZZTree_ratio.png")
#c.Clear()
