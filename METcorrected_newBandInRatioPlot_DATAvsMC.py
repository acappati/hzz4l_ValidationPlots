#!/usr/bin/env python

# **+***************************************************
# usage: 
#    python METcorrected_newBandInRatioPlot_DATAvsMC.py
#
# ******************************************************

import json
import ROOT
import math
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

def DrawRatioPlot(name, xaxis_title, yaxis_title, c, data, MC, MC_NvtxWEIGHT, MC_jesUp, MC_jesDn, MC_jerUp, MC_jerDn, MC_puUp, MC_puDn, MC_metUp, MC_metDn):
        c.Divide(0,2,0,0)
        pad1 = c.cd(1)

        pad1.SetBottomMargin(0.02)
        pad1.SetTopMargin(0.18)
        pad1.SetLeftMargin(0.10)

        max = 0.
        for bin in range (MC.GetSize() - 2):
                if ( MC.GetBinContent(bin + 1) > max):
                        max = MC.GetBinContent(bin + 1)

        MC.SetMaximum(1.4*max)
        #norm = data.Integral()/MC.Integral()   # Normalize MC to data        
        #MC.Scale(norm)
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

        MC_NvtxWEIGHT.SetMarkerStyle(23)
        MC_NvtxWEIGHT.SetMarkerColor(kAzure)
        MC_NvtxWEIGHT.SetMarkerSize(0.9)
        MC_NvtxWEIGHT.Draw("p E1 X0 SAME")

        pad2 = c.cd(2)

        pad2.SetBottomMargin(0.20)
        pad2.SetTopMargin(0.02)
        pad2.SetLeftMargin(0.10)
        Ratio       = TH1F ("Ratio",       "Ratio",      MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        Ratio_W     = TH1F ("Ratio_W",     "Ratio_W",    MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_up    = TH1F ("sigma_up",    "sigma_up",   MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_dn    = TH1F ("sigma_dn",    "sigma_dn",   MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_jesUp = TH1F ("sigma_jesUp", "sigma_jesUp",MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_jesDn = TH1F ("sigma_jesDn", "sigma_jesDn",MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_jerUp = TH1F ("sigma_jerUp", "sigma_jerUp",MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_jerDn = TH1F ("sigma_jerDn", "sigma_jerDn",MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_puUp  = TH1F ("sigma_puUp",  "sigma_puUp", MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_puDn  = TH1F ("sigma_puDn",  "sigma_puDn", MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_metUp = TH1F ("sigma_metUp", "sigma_metUp",MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())
        sigma_metDn = TH1F ("sigma_metDn", "sigma_metDn",MC.GetSize() - 2, MC.GetXaxis().GetXmin(), MC.GetXaxis().GetXmax())

        up_list = []
        dn_list = []
        for bin in range (MC.GetSize() - 2):
                temp_list = []
                if (MC.GetBinContent(bin + 1) == 0):
                        Ratio      .SetBinContent(bin + 1, 0)
                        Ratio      .SetBinError  (bin + 1, 0)
                        Ratio_W    .SetBinContent(bin + 1, 0)
                        Ratio_W    .SetBinError  (bin + 1, 0)
                        sigma_jesUp.SetBinContent(bin + 1, 0)
                        sigma_jesDn.SetBinContent(bin + 1, 0)
                        sigma_jerUp.SetBinContent(bin + 1, 0)
                        sigma_jerDn.SetBinContent(bin + 1, 0)
                        sigma_puUp .SetBinContent(bin + 1, 0)
                        sigma_puDn .SetBinContent(bin + 1, 0)
                        sigma_metUp.SetBinContent(bin + 1, 0)
                        sigma_metDn.SetBinContent(bin + 1, 0)
                else:
                        Ratio      .SetBinContent(bin + 1, float(data.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        Ratio      .SetBinError  (bin + 1, 1./(data.GetBinContent(bin + 1))**0.5)
                        Ratio_W    .SetBinContent(bin + 1, float(data.GetBinContent(bin + 1))/MC_NvtxWEIGHT.GetBinContent(bin + 1))
                        Ratio_W    .SetBinError  (bin + 1, 1./(data.GetBinContent(bin + 1))**0.5)
                        sigma_jesUp.SetBinContent(bin + 1, float(MC_jesUp.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        sigma_jesDn.SetBinContent(bin + 1, float(MC_jesDn.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        sigma_jerUp.SetBinContent(bin + 1, float(MC_jerUp.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        sigma_jerDn.SetBinContent(bin + 1, float(MC_jerDn.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        sigma_puUp .SetBinContent(bin + 1, float(MC_puUp. GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        sigma_puDn .SetBinContent(bin + 1, float(MC_puDn. GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        sigma_metUp.SetBinContent(bin + 1, float(MC_metUp.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        sigma_metDn.SetBinContent(bin + 1, float(MC_metDn.GetBinContent(bin + 1))/MC.GetBinContent(bin + 1))
                        print '############### bin '+str(bin+1)+' ##############'
                        print str(sigma_jesUp.GetBinContent(bin+1))
                        print str(sigma_jerUp.GetBinContent(bin+1))
                        print str(sigma_puUp.GetBinContent(bin+1))
                        print str(sigma_metUp.GetBinContent(bin+1))
                        print str(sigma_jesDn.GetBinContent(bin+1))
                        print str(sigma_jerDn.GetBinContent(bin+1))
                        print str(sigma_puDn.GetBinContent(bin+1))
                        print str(sigma_metDn.GetBinContent(bin+1))
                        temp_jesUp = sigma_jesUp.GetBinContent(bin + 1)
                        temp_jerUp = sigma_jerUp.GetBinContent(bin + 1)
                        temp_puUp  = sigma_puUp.GetBinContent(bin + 1)
                        temp_metUp = sigma_metUp.GetBinContent(bin + 1)
                        temp_jesDn = sigma_jesDn.GetBinContent(bin + 1)                        
                        temp_jerDn = sigma_jerDn.GetBinContent(bin + 1)
                        temp_puDn  = sigma_puDn.GetBinContent(bin + 1)
                        temp_metDn = sigma_metDn.GetBinContent(bin + 1)
                        temp_list.append(temp_jesUp)
                        temp_list.append(temp_jerUp)
                        temp_list.append(temp_puUp)
                        temp_list.append(temp_metUp)
                        temp_list.append(temp_jesDn)
                        temp_list.append(temp_jerDn)
                        temp_list.append(temp_puDn)
                        temp_list.append(temp_metDn)
                        print 'temp_list size is: ' + str(len(temp_list))
                        tempUp_list = []
                        tempDn_list = []
                        for i in range(len(temp_list)) :
                                print 'Elemento', i, 'is ', temp_list[i]
                                if (temp_list[i] > 1.) : 
                                        tempUp_list.append(temp_list[i])
                                elif (temp_list[i] < 1.) :
                                        tempDn_list.append(temp_list[i])
                        print 'tempUp_list size is: ' + str(len(tempUp_list))
                        print 'tempDn_list size is: ' + str(len(tempDn_list))
                
                        temp_up = 0.
                        for i in tempUp_list :
                                temp_up += (i - 1)**2
                                #print 'Elemento up iesimo della lista: ', str(i), '; temp_up al giro i = ', temp_up
                        up = math.sqrt(temp_up)
                        up_list.append(up)

                        temp_dn = 0.        
                        for i in tempDn_list :
                                temp_dn += (i - 1)**2
                                #print 'Elemento dn iesimo della lista: ', str(i), '; temp_dn al giro i = ', temp_dn
                        dn = math.sqrt(temp_dn)
                        dn_list.append(dn)

        print 'UP LIST SIZE is: ' + str(len(up_list))
        print 'DN LIST SIZE is: ' + str(len(dn_list))

        for bin in range(len(up_list)) :
                sigma_up.SetBinContent( bin+1, up_list[bin])
                print 'bin = ', bin, '   up = ', str(sigma_up.GetBinContent(bin+1))
        for bin in range(len(dn_list)) :
                sigma_dn.SetBinContent( bin+1, -dn_list[bin])
                print 'bin = ', bin, '   down = ', str(sigma_dn.GetBinContent(bin+1))


        print "Saving ratios for each systematic contribution bin per bin into root file ..."
        outFile_DATA = TFile.Open("RatioHisto_PROVA_"+ period + ".root", "RECREATE")
        outFile_DATA.cd()
        sigma_jesUp.Write()
        sigma_jesDn.Write()
        sigma_jerUp.Write()
        sigma_jerDn.Write()
        sigma_puUp.Write()
        sigma_puDn.Write()
        sigma_metUp.Write()
        sigma_metDn.Write()
        outFile_DATA.Close()

        for bin in range (Ratio.GetSize() - 2):
                temp = Ratio.GetBinContent(bin + 1)
                Ratio.SetBinContent( bin + 1, temp - 1)
        for bin in range (Ratio_W.GetSize() - 2):
                temp = Ratio_W.GetBinContent(bin + 1)
                Ratio_W.SetBinContent( bin + 1, temp - 1)

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
        Ratio.SetMarkerColor(kOrange+1)
        Ratio.SetMarkerSize(0.6)
        Ratio.Draw("p E1 X0 SAME")

        Ratio_W.SetMarkerStyle(23)
        Ratio_W.SetMarkerSize(0.9)
        Ratio_W.SetMarkerColor(kAzure)
        Ratio_W.Draw("p E1 X0 SAME")
        
        pad1.cd()
        leg = TLegend(.75,.3,.85,.75)
        leg.SetBorderSize(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.07)
        #leg.AddEntry(MC, "Z/t#bar{t} + jets", "f" )
        leg.AddEntry(MC, "DY + t#bar{t}  MC", "f" )
        leg.AddEntry(data, "Data", "p")
        leg.AddEntry(MC_NvtxWEIGHT, "MC reweighted", "p")
        leg.AddEntry(sigma_up, "Tot uncertainty", "f")
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
DIR = "/afs/cern.ch/work/e/elfontan/private/HZZ/Run2Legacy/CMSSW_10_3_1/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/MET_withNvtxWEIGHT_" + str(period) + str(treeText) + '/'
gSystem.Exec("mkdir -p " + DIR)
print "Output directory created!"


      
#********************
# Define histo Z->ee
#********************
PFMET_corrected_data     = TH1F("PFMET_corrected_data","PFMET_corrected_data",         17, 0, 170)
PFMET_corrected_MC       = TH1F("PFMET_corrected_MC","PFMET_corrected_MC",             17, 0, 170)
PFMET_corrected_MC_jesUp = TH1F("PFMET_corrected_MC_jesUp","PFMET_corrected_MC_jesUp", 17, 0, 170)
PFMET_corrected_MC_jesDn = TH1F("PFMET_corrected_MC_jesDn","PFMET_corrected_MC_jesDn", 17, 0, 170)
PFMET_corrected_MC_jerUp = TH1F("PFMET_corrected_MC_jerUp","PFMET_corrected_MC_jerUp", 17, 0, 170)
PFMET_corrected_MC_jerDn = TH1F("PFMET_corrected_MC_jerDn","PFMET_corrected_MC_jerDn", 17, 0, 170)
PFMET_corrected_MC_puUp  = TH1F("PFMET_corrected_MC_puUp","PFMET_corrected_MC_puUp",   17, 0, 170)
PFMET_corrected_MC_puDn  = TH1F("PFMET_corrected_MC_puDn","PFMET_corrected_MC_puDn",   17, 0, 170)
PFMET_corrected_MC_metUp = TH1F("PFMET_corrected_MC_metUp","PFMET_corrected_MC_metUp", 17, 0, 170)
PFMET_corrected_MC_metDn = TH1F("PFMET_corrected_MC_metDn","PFMET_corrected_MC_metDn", 17, 0, 170)
PFMET_corrected_MC_OLDWEIGHT_puUp  = TH1F("PFMET_corrected_MC_OLDWEIGHT_puUp","PFMET_corrected_MC_OLDWEIGHT_puUp",   17, 0, 170)
PFMET_corrected_MC_OLDWEIGHT_puDn  = TH1F("PFMET_corrected_MC_OLDWEIGHT_puDn","PFMET_corrected_MC_OLDWEIGHT_puDn",   17, 0, 170)

PFMET_corrected_NvtxWEIGHT_MC      = TH1F("PFMET_corrected_NvtxWEIGHT_MC","PFMET_corrected_NvtxWEIGHT_MC",  17, 0, 170)
f_NvtxWEIGHT = TFile.Open("/afs/cern.ch/work/e/elfontan/private/HZZ/Run2Legacy/CMSSW_10_3_1/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/NvtxHisto_"+ period + ".root")
h_NvtxWEIGHT = f_NvtxWEIGHT.Get("Nvtx_ratio")


print 'Reading file', fDY.GetName(),'...'
n_events = 0
NvtxWEIGHT = 0
for event in tDY:
        #if n_events == 10000 :
        #        break
        n_events+=1

        if(n_events % int((tDY.GetEntries()/10)) == 0):
                print "{} %".format(str(100*n_events/tDY.GetEntries() + 1))

	#if (event.LepPt.at(0) < 30 or event.LepPt.at(1) < 30. or abs(event.LepLepId.at(0))!=11):
        #        continue
	if (event.LepPt.at(0) < 30. or event.LepPt.at(1) < 30.):
                continue
	if (event.Z1Mass < 70 or event.Z1Mass > 110):
		continue
                
	PFMET_corrected_MC.Fill(event.PFMET_corrected,             event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_jesUp.Fill(event.PFMET_corrected_jesUp, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_jesDn.Fill(event.PFMET_corrected_jesDn, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_jerUp.Fill(event.PFMET_corrected_jerUp, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_jerDn.Fill(event.PFMET_corrected_jerDn, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_OLDWEIGHT_puUp.Fill(event.PFMET_corrected_puUp,   event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_OLDWEIGHT_puDn.Fill(event.PFMET_corrected_puDn,   event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_puUp.Fill(event.PFMET_corrected_puUp,   event.genHEPMCweight*event.dataMCWeight*event.trigEffWeight*event.PUWeight_Up*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_puDn.Fill(event.PFMET_corrected_puDn,   event.genHEPMCweight*event.dataMCWeight*event.trigEffWeight*event.PUWeight_Dn*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_metUp.Fill(event.PFMET_corrected_metUp, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)
	PFMET_corrected_MC_metDn.Fill(event.PFMET_corrected_metDn, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_DY)

        #print "Nvtx is " + str(event.Nvtx)        
        #print "MET is " + str(event.PFMET_corrected)
        #print "NvtxWEIGHT bin is " + str(h_NvtxWEIGHT.FindBin(event.Nvtx))
        #print "NvtxWEIGHT is " + str(NvtxWEIGHT)
        NvtxWEIGHT = h_NvtxWEIGHT.GetBinContent(h_NvtxWEIGHT.FindBin(event.Nvtx))
        PFMET_corrected_NvtxWEIGHT_MC.Fill(event.PFMET_corrected, event.overallEventWeight*NvtxWEIGHT*event.xsec*1000*lumi/SumWeight_DY)

print 'Reading file', fTT.GetName(),'...'
n_events=0
for event in tTT:
        #if n_events == 10000 :
        #        break
        n_events+=1                                      
        NvtxWEIGHT = 0

        if(n_events % int((tTT.GetEntries()/10)) == 0):
                print "{} %".format(str(100*n_events/tTT.GetEntries() + 1))

	#if (event.LepPt.at(0) < 30 or event.LepPt.at(1) < 30. or abs(event.LepLepId.at(0))!=11):
	if (event.LepPt.at(0) < 30 or event.LepPt.at(1) < 30.):
		continue
	if (event.Z1Mass < 70 or event.Z1Mass > 110):
		continue

	PFMET_corrected_MC.Fill(event.PFMET_corrected,             event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_jesUp.Fill(event.PFMET_corrected_jesUp, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_jesDn.Fill(event.PFMET_corrected_jesDn, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_jerUp.Fill(event.PFMET_corrected_jerUp, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_jerDn.Fill(event.PFMET_corrected_jerDn, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_OLDWEIGHT_puUp.Fill(event.PFMET_corrected_puUp,   event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_OLDWEIGHT_puDn.Fill(event.PFMET_corrected_puDn,   event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_puUp.Fill(event.PFMET_corrected_puUp,   event.genHEPMCweight*event.dataMCWeight*event.trigEffWeight*event.PUWeight_Up*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_puDn.Fill(event.PFMET_corrected_puDn,   event.genHEPMCweight*event.dataMCWeight*event.trigEffWeight*event.PUWeight_Dn*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_metUp.Fill(event.PFMET_corrected_metUp, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)
	PFMET_corrected_MC_metDn.Fill(event.PFMET_corrected_metDn, event.overallEventWeight*event.xsec*1000*lumi/SumWeight_TT)

        NvtxWEIGHT = h_NvtxWEIGHT.GetBinContent(h_NvtxWEIGHT.FindBin(event.Nvtx))
	PFMET_corrected_NvtxWEIGHT_MC.Fill(event.PFMET_corrected, event.overallEventWeight*NvtxWEIGHT*event.xsec*1000*lumi/SumWeight_TT)



print 'Reading file', fdata.GetName(),'...'
for event in tdata:
        if (event.LepPt.at(0) < 30 or event.LepPt.at(1) < 30.):
                continue
        if (event.Z1Mass < 70 or event.Z1Mass > 110):
                continue
        PFMET_corrected_data.Fill(event.PFMET_corrected)

#tdata.Draw("PFMET_corrected >> PFMET_corrected_data",  "(Z1Mass > 70 && Z1Mass < 110) && (LepPt[0] > 30 && LepPt[1] > 30)")

#METhisto = TFile.Open("METhisto_NvtxWEIGHT_"+ period + ".root", "RECREATE")
#METhisto.cd()
#PFMET_corrected_MC.Write()
#PFMET_corrected_NvtxWEIGHT_MC.Write()
#PFMET_corrected_data.Write()
#PFMET_corrected_MC_jesUp.Write()
#PFMET_corrected_MC_jesDn.Write()
#PFMET_corrected_MC_jerUp.Write()
#PFMET_corrected_MC_jerDn.Write()
#PFMET_corrected_MC_puUp.Write()
#PFMET_corrected_MC_puDn.Write()
#PFMET_corrected_MC_OLDWEIGHT_puUp.Write()
#PFMET_corrected_MC_OLDWEIGHT_puDn.Write()
#PFMET_corrected_MC_metUp.Write()
#PFMET_corrected_MC_metDn.Write()
#h_NvtxWEIGHT.Write()
#METhisto.Close()

#f_NvtxWEIGHT.Close()


c = ROOT.TCanvas()
DrawRatioPlot(DIR+"PFMET_corrected", "PFMET_corrected", "Events/10 GeV", c, PFMET_corrected_data, PFMET_corrected_MC, PFMET_corrected_NvtxWEIGHT_MC, PFMET_corrected_MC_jesUp, PFMET_corrected_MC_jesDn, PFMET_corrected_MC_jerUp, PFMET_corrected_MC_jerDn, PFMET_corrected_MC_puUp, PFMET_corrected_MC_puDn, PFMET_corrected_MC_metUp, PFMET_corrected_MC_metDn)


