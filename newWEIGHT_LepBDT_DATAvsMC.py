#!/usr/bin/env python

# ****************************************
# usage: 
#    python newWEIGHT_LepBDT_DATAvsMC.py
#
# ****************************************


import json
import ROOT, math, helper, CMSGraphics, CMS_lumi
from ROOT import TFile, TH1, TH1F, TCanvas, gSystem, TAttFill, TLegend, TRatioPlot, TPad, TStyle, THStack, TPaveText, gStyle
from CMSGraphics import makeCMSCanvas, makeLegend
from helper import ReadJSON
from helper import DoSimpleFit, Result
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kMagenta


# *****************************
# Declare all the variables 
# options
# *****************************                                                                                                                         
redoDATAHistos    = True
redoMCDYHistos    = True
redoMCTTbarHistos = True

# Data tree options 
# *****************************                                                                                                                         
ZZTree    = False
CRZLLTree = False
CRZLTree  = False
ZTree     = True

# Data periods options                                                                                                                                        
# *****************************                                                                                                                         
#period = "data2016"
period = "data2017"                                                                                                                                               
#period = "data2018"                                                                                                                                                 
# *****************************  


# *****************************                                                                                        
# Input file
# *****************************                                                                                                                         
if(period == "data2016"):
    inputDATAtree    = TFile.Open("root://lxcms03//data3/Higgs/190617/Data_2016/AllData/ZZ4lAnalysis.root")          # 2016 Data                                                   
    inputMCDYtree    = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2016/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")  # DYJets 2016 MC (LO)                             
    inputMCTTbartree = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2016/TTTo2L2Nu/ZZ4lAnalysis.root")          # TTTo2L2Nu 2016 MC         
    lumi     = 35.92  # fb-1
    lumiText = '35.92 fb^{-1}'
    if(ZZTree):
        treeDATA    = inputDATAtree.Get("ZZTree/candTree")
        treeMCDY    = inputMCDYtree.Get("ZZTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("ZZTree/candTree")
        treeText  = "ZZTree"
    elif(CRZLLTree):
        treeDATA    = inputDATAtree.Get("CRZLLTree/candTree")
        treeMCDY    = inputMCDYTtee.Get("CRZLLTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("CRZLLTree/candTree")
        treeText  = "CRZLLTree"
    elif(CRZLTree):
        treeDATA    = inputDATAtree.Get("CRZLTree/candTree")
        treeMCDY    = inputMCDYtree.Get("CRZLTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("CRZLTree/candTree")
        treeText  = "CRZLTree"
    elif(ZTree):
        treeDATA    = inputDATAtree.Get("ZTree/candTree")
        treeMCDY    = inputMCDYtree.Get("ZTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("ZTree/candTree")
        treeText  = "ZTree"
    else:
        print ("Error: wrong option!")

elif(period == "data2017"):
    inputDATAtree    = TFile.Open("root://lxcms03//data3/Higgs/190617/Data_2017/AllData/ZZ4lAnalysis.root")          # 2017 Data                                                   
    inputMCDYtree    = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2017/DYJetsToLL_M50_LO/ZZ4lAnalysis.root")  # DYJets 2017 MC (LO)                  
    inputMCTTbartree = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2017/TTTo2L2Nu/ZZ4lAnalysis.root")          # TTTo2L2Nu 2017 MC         
    lumi     = 41.53   # fb-1
    lumiText = '41.53 fb^{-1}'
    if(ZZTree):
        treeDATA    = inputDATAtree.Get("ZZTree/candTree")
        treeMCDY    = inputMCDYtree.Get("ZZTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("ZZTree/candTree")
        treeText  = "ZZTree"
    elif(CRZLLTree):
        treeDATA    = inputDATAtree.Get("CRZLLTree/candTree")
        treeMCDY    = inputMCDYtree.Get("CRZLLTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("CRZLLTree/candTree")
        treeText  = "CRZLLTree"
    elif(CRZLTree):
        treeDATA    = inputDATAtree.Get("CRZLTree/candTree")
        treeMCDY    = inputMCDYtree.Get("CRZLTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("CRZLTree/candTree")
        treeText  = "CRZLTree"
    elif(ZTree):
        treeDATA    = inputDATAtree.Get("ZTree/candTree")
        treeMCDY    = inputMCDYtree.Get("ZTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("ZTree/candTree")
        treeText  = "ZTree"
    else:
        print ("Error: wrong option!")

elif(period == "data2018"):
    inputDATAtree    = TFile.Open("../ZZ4lAnalysis.root")                                 #2018 data    
    inputMCDYtree    = TFile.Open("/data3/Higgs/190128/DYJetsToLL_M50/ZZ4lAnalysis.root") #DYJets 2018 MC 
    inputMCTTbartree = TFile.Open("/data3/Higgs/190128/TTTo2L2Nu/ZZ4lAnalysis.root")      #TTbarJets 2017 MC (rereco json)
    lumi     = 58.83   # fb-1
    lumiText = '58.83 fb^{-1}'
    if(ZZTree):
        treeDATA    = inputDATAtree.Get("ZZTree/candTree")
        treeMCDY    = inputMCDYtree.Get("ZZTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("ZZTree/candTree")
        treeText  = "ZZTree"
    elif(CRZLLTree):
        treeDATA    = inputDATAtree.Get("CRZLLTree/candTree")
        treeMCDY    = inputMCDYtree.Get("CRZLLTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("CRZLLTree/candTree")
        treeText  = "CRZLLTree"
    elif(CRZLTree):
        treeDATA    = inputDATAtree.Get("CRZLTree/candTree")
        treeMCDY    = inputMCDYtree.Get("CRZLTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("CRZLTree/candTree")
        treeText  = "CRZLTree"
    elif(ZTree):
        treeDATA    = inputDATAtree.Get("ZTree/candTree")
        treeMCDY    = inputMCDYtree.Get("ZTree/candTree")
        treeMCTTbar = inputMCTTbartree.Get("ZTree/candTree")
        treeText  = "ZTree"
    else:
        print ("Error: wrong option!")
else: 
    print ("Error: choose a period!")



# ********************
#  do DATA histos 
# ********************
if(redoDATAHistos) :

    TH1.SetDefaultSumw2() # set sumw2 = true fro all the histograms created from now on

    # ******************************
    # Define data histograms Z->ee
    # ******************************
    Z_ele_1st_LepBDT_hist    = TH1F('Z_ele_1st_LepBDT_hist'               , 'LepBDT leading ele'               , 100, -1.1, 1.1) 
    Z_ele_1st_LepBDT_hist_EB = TH1F('Z_ele_1st_LepBDT_hist_EB', 'LepBDT leading ele in ECAL Barrel', 100, -1.1, 1.1) 
    Z_ele_1st_LepBDT_hist_EE = TH1F('Z_ele_1st_LepBDT_hist_EE', 'LepBDT leading ele in ECAL Endcap', 100, -1.1, 1.1) 

    # ******************************
    # Define data histograms Z->mumu
    # ******************************
    Z_mu_1st_LepBDT_hist    = TH1F('Z_mu_1st_LepBDT_hist'   , 'LepBDT leading mu'               , 40, 0., 10.) 
    Z_mu_1st_LepBDT_hist_MB = TH1F('Z_mu_1st_LepBDT_hist_MB', 'LepBDT leading mu in Muon Barrel', 40, 0., 10.) 
    Z_mu_1st_LepBDT_hist_ME = TH1F('Z_mu_1st_LepBDT_hist_ME', 'LepBDT leading mu in Muon Endcap', 40, 0., 10.) 

    if CRZLTree :
        Z_ExtraEl_LepBDT_hist    = TH1F('Z_ExtraEl_LepBDT_hist'               , 'LepBDT extraEl'               , 100, -1.1, 1.1)
        Z_ExtraEl_LepBDT_hist_EB = TH1F('Z_ExtraEl_LepBDT_hist_EB', 'LepBDT extraEl in ECAL Barrel', 100, -1.1, 1.1)
        Z_ExtraEl_LepBDT_hist_EE = TH1F('Z_ExtraEl_LepBDT_hist_EE', 'LepBDT extraEl in ECAL Endcap', 100, -1.1, 1.1)

        Z_ExtraMu_LepBDT_hist    = TH1F('Z_ExtraMu_LepBDT_hist'               , 'LepBDT extraMu'               , 100, -1.1, 1.1)
        Z_ExtraMu_LepBDT_hist_MB = TH1F('Z_ExtraMu_LepBDT_hist_MB', 'LepBDT extraMu in Muon Barrel', 100, -1.1, 1.1)
        Z_ExtraMu_LepBDT_hist_ME = TH1F('Z_ExtraMu_LepBDT_hist_ME', 'LepBDT extraMu in Muon Endcap', 100, -1.1, 1.1)

    

    ##############
    # read TTree #
    ##############
    print "reading tree", inputDATAtree.GetName(),treeText,treeDATA.GetName()  ,"..."

    treeDATA.SetBranchStatus("*",0)  # disable all branches
    if ZTree :
        treeDATA.SetBranchStatus("Zsel",1)
        treeDATA.SetBranchStatus("ZMass",1)
    else : 
        treeDATA.SetBranchStatus("ZZsel",1)
    treeDATA.SetBranchStatus("LepLepId",1)
    treeDATA.SetBranchStatus("LepPt",1)
    treeDATA.SetBranchStatus("LepEta",1)
    treeDATA.SetBranchStatus("LepBDT",1)

    for event in treeDATA:
        if ZTree :
            if ( event.Zsel < 0 ) : continue # skip events that do not pass the trigger 
        else : 
            if ( event.ZZsel < 0 ) : continue # skip events that do not pass the trigger 

        if (event.ZMass < 80. or event.ZMass > 100.): continue
        if (event.LepPt[0] < 30.) : continue
        #if (max(event.LepPt[0], event.LepPt[1]) < 30.) : continue  

        ###########
        # Z -> ee #
        ###########
        if((int(math.fabs(event.LepLepId[0])) == 11)) :
            
            if event.LepPt[0] >= event.LepPt[1] :
                Z_ele_1st_LepBDT_hist.Fill(event.LepBDT[0])

                if math.fabs(event.LepEta[0]) <= 1.479 :
                    Z_ele_1st_LepBDT_hist_EB.Fill(event.LepBDT[0])
                else :
                    Z_ele_1st_LepBDT_hist_EE.Fill(event.LepBDT[0])

            else :
                Z_ele_1st_LepBDT_hist.Fill(event.LepBDT[1])

                if math.fabs(event.LepEta[1]) <= 1.479 :
                    Z_ele_1st_LepBDT_hist_EB.Fill(event.LepBDT[1])
                else :
                    Z_ele_1st_LepBDT_hist_EE.Fill(event.LepBDT[1])

        ###########
        # Z->mumu #
        ###########
        if((int(math.fabs(event.LepLepId[0])) == 13)) :
            
            if event.LepPt[0] >= event.LepPt[1] :
                Z_mu_1st_LepBDT_hist.Fill(event.LepBDT[0])

                if math.fabs(event.LepEta[0]) <= 1. :
                    Z_mu_1st_LepBDT_hist_MB.Fill(event.LepBDT[0])
                else :
                    Z_mu_1st_LepBDT_hist_ME.Fill(event.LepBDT[0])

            else :
                Z_mu_1st_LepBDT_hist.Fill(event.LepBDT[1])

                if math.fabs(event.LepEta[1]) <= 1. :
                    Z_mu_1st_LepBDT_hist_MB.Fill(event.LepBDT[1])
                else :
                    Z_mu_1st_LepBDT_hist_ME.Fill(event.LepBDT[1])

            
        # extra lepton
        if CRZLTree :
                
                if(int(math.fabs(event.LepLepId[2])) == 11 ) :

                    Z_ExtraEl_LepBDT_hist.Fill(event.LepBDT[2])
                    
                    if math.fabs(event.LepEta[2]) <= 1.479 :  
                        Z_ExtraEl_LepBDT_hist_EB.Fill(event.LepBDT[2])
                    else :
                        Z_ExtraEl_LepBDT_hist_EE.Fill(event.LepBDT[2])

                elif(int(math.fabs(event.LepLepId[2])) == 13 ) :
                    
                     Z_ExtraMu_LepBDT_hist.Fill(event.LepBDT[2])

                     if math.fabs(event.LepEta[2]) <= 1. :
                         Z_ExtraMu_LepBDT_hist_MB.Fill(event.LepBDT[2])
                     else :
                         Z_ExtraMu_LepBDT_hist_ME.Fill(event.LepBDT[2])

                else :
                    print "Error: wrong particle ID!"


    #save histograms in a root file 
    print "saving histograms into root file ..."
    LepBDT_DATA_outFile = TFile.Open("LepBDTdistrib_DATA_"+ period + "_" + treeText +".root", "RECREATE")
    LepBDT_DATA_outFile.cd()

    Z_ele_1st_LepBDT_hist.Write()
    Z_ele_1st_LepBDT_hist_EB.Write()
    Z_ele_1st_LepBDT_hist_EE.Write()
                                          
    Z_mu_1st_LepBDT_hist.Write()
    Z_mu_1st_LepBDT_hist_MB.Write()
    Z_mu_1st_LepBDT_hist_ME.Write()
                                                                
    if CRZLTree :               
        Z_ExtraEl_LepBDT_hist.Write()
        Z_ExtraEl_LepBDT_hist_EB.Write()
        Z_ExtraEl_LepBDT_hist_EE.Write()
                                
        Z_ExtraMu_LepBDT_hist.Write()
        Z_ExtraMu_LepBDT_hist_MB.Write()
        Z_ExtraMu_LepBDT_hist_ME.Write()


    LepBDT_DATA_outFile.Close()



# ********************
#  do MC DY histos
# ********************
if(redoMCDYHistos) :

    TH1.SetDefaultSumw2() # set sumw2 = true fro all the histograms created from now on

    # ******************************
    # Define data histograms Z->ee
    # ******************************
    Z_ele_1st_LepBDT_MC_DY_hist    = TH1F('Z_ele_1st_LepBDT_MC_DY_hist'   , 'LepBDT leading ele'               , 100, -1.1, 1.1) 
    Z_ele_1st_LepBDT_MC_DY_hist_EB = TH1F('Z_ele_1st_LepBDT_MC_DY_hist_EB', 'LepBDT leading ele in ECAL Barrel', 100, -1.1, 1.1) 
    Z_ele_1st_LepBDT_MC_DY_hist_EE = TH1F('Z_ele_1st_LepBDT_MC_DY_hist_EE', 'LepBDT leading ele in ECAL Endcap', 100, -1.1, 1.1) 

    # ******************************
    # Define data histograms Z->mumu
    # ******************************
    Z_mu_1st_LepBDT_MC_DY_hist    = TH1F('Z_mu_1st_LepBDT_MC_DY_hist'   , 'LepBDT leading mu'               , 40, 0., 10.) 
    Z_mu_1st_LepBDT_MC_DY_hist_MB = TH1F('Z_mu_1st_LepBDT_MC_DY_hist_MB', 'LepBDT leading mu in Muon Barrel', 40, 0., 10.) 
    Z_mu_1st_LepBDT_MC_DY_hist_ME = TH1F('Z_mu_1st_LepBDT_MC_DY_hist_ME', 'LepBDT leading mu in Muon Endcap', 40, 0., 10.) 

    if CRZLTree :
        Z_ExtraEl_LepBDT_MC_DY_hist    = TH1F('Z_ExtraEl_LepBDT_MC_DY_hist'               , 'LepBDT extraEl'               , 100, -1.1, 1.1)
        Z_ExtraEl_LepBDT_MC_DY_hist_EB = TH1F('Z_ExtraEl_LepBDT_MC_DY_hist_EB', 'LepBDT extraEl in ECAL Barrel', 100, -1.1, 1.1)
        Z_ExtraEl_LepBDT_MC_DY_hist_EE = TH1F('Z_ExtraEl_LepBDT_MC_DY_hist_EE', 'LepBDT extraEl in ECAL Endcap', 100, -1.1, 1.1)

        Z_ExtraMu_LepBDT_MC_DY_hist    = TH1F('Z_ExtraMu_LepBDT_MC_DY_hist'               , 'LepBDT extraMu'               , 100, -1.1, 1.1)
        Z_ExtraMu_LepBDT_MC_DY_hist_MB = TH1F('Z_ExtraMu_LepBDT_MC_DY_hist_MB', 'LepBDT extraMu in Muon Barrel', 100, -1.1, 1.1)
        Z_ExtraMu_LepBDT_MC_DY_hist_ME = TH1F('Z_ExtraMu_LepBDT_MC_DY_hist_ME', 'LepBDT extraMu in Muon Endcap', 100, -1.1, 1.1)

    
    # get partial event weight
    hcounters           = inputMCDYtree.Get("ZTree/Counters")
    gen_sumWeights      = hcounters.GetBinContent(1)
    partialSampleWeight = lumi * 1000 / gen_sumWeights


    # read tree 
    print "reading tree", inputMCDYtree.GetName(),treeText,treeMCDY.GetName()  ,"..."
    for event in treeMCDY:
        if ZTree :
            if ( event.Zsel < 0 ) : continue # skip events that do not pass the trigger
        else :
            if ( event.ZZsel < 0 ) : continue # skip events that do not pass the trigger

        weight = partialSampleWeight*event.xsec*event.overallEventWeight/event.genHEPMCweight

        if (event.ZMass < 80. or event.ZMass > 100.): continue
        if (event.LepPt[0] < 30.) : continue
        #if (max(event.LepPt[0], event.LepPt[1]) < 30.) : continue  


        ###########  
        # Z -> ee #
        ###########
        if(int(math.fabs(event.LepLepId[0])) == 11) :
            
            if event.LepPt[0] >= event.LepPt[1] :
                Z_ele_1st_LepBDT_MC_DY_hist.Fill(event.LepBDT[0], weight)

                if math.fabs(event.LepEta[0]) <= 1.479 :
                    Z_ele_1st_LepBDT_MC_DY_hist_EB.Fill(event.LepBDT[0], weight)
                else :
                    Z_ele_1st_LepBDT_MC_DY_hist_EE.Fill(event.LepBDT[0], weight)

            else :
                Z_ele_1st_LepBDT_MC_DY_hist.Fill(event.LepBDT[1], weight)

                if math.fabs(event.LepEta[1]) <= 1.479 :
                    Z_ele_1st_LepBDT_MC_DY_hist_EB.Fill(event.LepBDT[1], weight)
                else :
                    Z_ele_1st_LepBDT_MC_DY_hist_EE.Fill(event.LepBDT[1], weight)
          
        ###########  
        # Z->mumu #
        ###########
        if(int(math.fabs(event.LepLepId[0])) == 13) :
            
            if event.LepPt[0] >= event.LepPt[1] :
                Z_mu_1st_LepBDT_MC_DY_hist.Fill(event.LepBDT[0], weight)

                if math.fabs(event.LepEta[0]) <= 1. :
                    Z_mu_1st_LepBDT_MC_DY_hist_MB.Fill(event.LepBDT[0], weight)
                else :
                    Z_mu_1st_LepBDT_MC_DY_hist_ME.Fill(event.LepBDT[0], weight)

            else :
                Z_mu_1st_LepBDT_MC_DY_hist.Fill(event.LepBDT[1], weight)

                if math.fabs(event.LepEta[1]) <= 1. :
                    Z_mu_1st_LepBDT_MC_DY_hist_MB.Fill(event.LepBDT[1], weight)
                else :
                    Z_mu_1st_LepBDT_MC_DY_hist_ME.Fill(event.LepBDT[1], weight)


        # extra lepton
        if CRZLTree :
                
                if(int(math.fabs(event.LepLepId[2])) == 11 ) :

                    Z_ExtraEl_LepBDT_MC_DY_hist.Fill(event.LepBDT[2], weight)
                    
                    if math.fabs(event.LepEta[2]) <= 1.479 :  
                        Z_ExtraEl_LepBDT_MC_DY_hist_EB.Fill(event.LepBDT[2], weight)
                    else :
                        Z_ExtraEl_LepBDT_MC_DY_hist_EE.Fill(event.LepBDT[2], weight)

                elif(int(math.fabs(event.LepLepId[2])) == 13 ) :
                    
                    Z_ExtraMu_LepBDT_MC_DY_hist.Fill(event.LepBDT[2], weight)

                    if math.fabs(event.LepEta[2]) <= 1. :
                        Z_ExtraMu_LepBDT_MC_DY_hist_MB.Fill(event.LepBDT[2], weight)
                    else :
                        Z_ExtraMu_LepBDT_MC_DY_hist_ME.Fill(event.LepBDT[2], weight)

                else :
                    print "Error: wrong particle ID!"


    #save histograms in a root file 
    print "saving histograms into root file ..."
    LepBDT_MC_DY_outFile = TFile.Open("LepBDTdistrib_MC_DY_"+ period + "_" + treeText +".root", "RECREATE")
    LepBDT_MC_DY_outFile.cd()

    Z_ele_1st_LepBDT_MC_DY_hist.Write()
    Z_ele_1st_LepBDT_MC_DY_hist_EB.Write()
    Z_ele_1st_LepBDT_MC_DY_hist_EE.Write()
                                                                                   
    Z_mu_1st_LepBDT_MC_DY_hist.Write()
    Z_mu_1st_LepBDT_MC_DY_hist_MB.Write()
    Z_mu_1st_LepBDT_MC_DY_hist_ME.Write()
                                
                                
    if CRZLTree :               
        Z_ExtraEl_LepBDT_MC_DY_hist.Write()
        Z_ExtraEl_LepBDT_MC_DY_hist_EB.Write()
        Z_ExtraEl_LepBDT_MC_DY_hist_EE.Write()
                                
        Z_ExtraMu_LepBDT_MC_DY_hist.Write()
        Z_ExtraMu_LepBDT_MC_DY_hist_MB.Write()
        Z_ExtraMu_LepBDT_MC_DY_hist_ME.Write()


    LepBDT_MC_DY_outFile.Close()
    print "MC DY histo file created!"
# ********************


# ********************
#  do MC TTbar histos
# ********************
if(redoMCTTbarHistos) :

    TH1.SetDefaultSumw2() # set sumw2 = true fro all the histograms created from now on

    # ******************************
    # Define data histograms Z->ee
    # ******************************
    Z_ele_1st_LepBDT_MC_TTbar_hist    = TH1F('Z_ele_1st_LepBDT_MC_TTbar_hist'   , 'LepBDT leading ele'               , 100, -1.1, 1.1) 
    Z_ele_1st_LepBDT_MC_TTbar_hist_EB = TH1F('Z_ele_1st_LepBDT_MC_TTbar_hist_EB', 'LepBDT leading ele in ECAL Barrel', 100, -1.1, 1.1) 
    Z_ele_1st_LepBDT_MC_TTbar_hist_EE = TH1F('Z_ele_1st_LepBDT_MC_TTbar_hist_EE', 'LepBDT leading ele in ECAL Endcap', 100, -1.1, 1.1) 

    # ******************************
    # Define data histograms Z->mumu
    # ******************************
    Z_mu_1st_LepBDT_MC_TTbar_hist    = TH1F('Z_mu_1st_LepBDT_MC_TTbar_hist'   , 'LepBDT leading mu'               , 40, 0., 10.) 
    Z_mu_1st_LepBDT_MC_TTbar_hist_MB = TH1F('Z_mu_1st_LepBDT_MC_TTbar_hist_MB', 'LepBDT leading mu in Muon Barrel', 40, 0., 10.) 
    Z_mu_1st_LepBDT_MC_TTbar_hist_ME = TH1F('Z_mu_1st_LepBDT_MC_TTbar_hist_ME', 'LepBDT leading mu in Muon Endcap', 40, 0., 10.) 

    if CRZLTree :
        Z_ExtraEl_LepBDT_MC_TTbar_hist    = TH1F('Z_ExtraEl_LepBDT_MC_TTbar_hist'               , 'LepBDT extraEl'               , 100, -1.1, 1.1)
        Z_ExtraEl_LepBDT_MC_TTbar_hist_EB = TH1F('Z_ExtraEl_LepBDT_MC_TTbar_hist_EB', 'LepBDT extraEl in ECAL Barrel', 100, -1.1, 1.1)
        Z_ExtraEl_LepBDT_MC_TTbar_hist_EE = TH1F('Z_ExtraEl_LepBDT_MC_TTbar_hist_EE', 'LepBDT extraEl in ECAL Endcap', 100, -1.1, 1.1)

        Z_ExtraMu_LepBDT_MC_TTbar_hist    = TH1F('Z_ExtraMu_LepBDT_MC_TTbar_hist'               , 'LepBDT extraMu'               , 100, -1.1, 1.1)
        Z_ExtraMu_LepBDT_MC_TTbar_hist_MB = TH1F('Z_ExtraMu_LepBDT_MC_TTbar_hist_MB', 'LepBDT extraMu in Muon Barrel', 100, -1.1, 1.1)
        Z_ExtraMu_LepBDT_MC_TTbar_hist_ME = TH1F('Z_ExtraMu_LepBDT_MC_TTbar_hist_ME', 'LepBDT extraMu in Muon Endcap', 100, -1.1, 1.1)

    
    # get partial event weight
    hcounters           = inputMCTTbartree.Get("ZTree/Counters")
    gen_sumWeights      = hcounters.GetBinContent(1)
    partialSampleWeight = lumi * 1000 / gen_sumWeights


    # read tree 
    print "reading tree", inputMCTTbartree.GetName(),treeText,treeMCTTbar.GetName()  ,"..."
    for event in treeMCTTbar:
        if ZTree :
            if ( event.Zsel < 0 ) : continue # skip events that do not pass the trigger
        else :
            if ( event.ZZsel < 0 ) : continue # skip events that do not pass the trigger

        weight = partialSampleWeight*event.xsec*event.overallEventWeight/event.genHEPMCweight

        if (event.ZMass < 80. or event.ZMass > 100.): continue
        if (event.LepPt[0] < 30.) : continue


        ###########  
        # Z -> ee #
        ###########
        if(int(math.fabs(event.LepLepId[0])) == 11) :
            
            if event.LepPt[0] >= event.LepPt[1] :
                Z_ele_1st_LepBDT_MC_TTbar_hist.Fill(event.LepBDT[0], weight)

                if math.fabs(event.LepEta[0]) <= 1.479 :
                    Z_ele_1st_LepBDT_MC_TTbar_hist_EB.Fill(event.LepBDT[0], weight)
                else :
                    Z_ele_1st_LepBDT_MC_TTbar_hist_EE.Fill(event.LepBDT[0], weight)

            else :
                Z_ele_1st_LepBDT_MC_TTbar_hist.Fill(event.LepBDT[1], weight)

                if math.fabs(event.LepEta[1]) <= 1.479 :
                    Z_ele_1st_LepBDT_MC_TTbar_hist_EB.Fill(event.LepBDT[1], weight)
                else :
                    Z_ele_1st_LepBDT_MC_TTbar_hist_EE.Fill(event.LepBDT[1], weight)
          
        ###########  
        # Z->mumu #
        ###########
        if(int(math.fabs(event.LepLepId[0])) == 13) :
            
            if event.LepPt[0] >= event.LepPt[1] :
                Z_mu_1st_LepBDT_MC_TTbar_hist.Fill(event.LepBDT[0], weight)

                if math.fabs(event.LepEta[0]) <= 1. :
                    Z_mu_1st_LepBDT_MC_TTbar_hist_MB.Fill(event.LepBDT[0], weight)
                else :
                    Z_mu_1st_LepBDT_MC_TTbar_hist_ME.Fill(event.LepBDT[0], weight)

            else :
                Z_mu_1st_LepBDT_MC_TTbar_hist.Fill(event.LepBDT[1], weight)

                if math.fabs(event.LepEta[1]) <= 1. :
                    Z_mu_1st_LepBDT_MC_TTbar_hist_MB.Fill(event.LepBDT[1], weight)
                else :
                    Z_mu_1st_LepBDT_MC_TTbar_hist_ME.Fill(event.LepBDT[1], weight)


        # extra lepton
        if CRZLTree :
                
                if(int(math.fabs(event.LepLepId[2])) == 11 ) :

                    Z_ExtraEl_LepBDT_MC_TTbar_hist.Fill(event.LepBDT[2], weight)
                    
                    if math.fabs(event.LepEta[2]) <= 1.479 :  
                        Z_ExtraEl_LepBDT_MC_TTbar_hist_EB.Fill(event.LepBDT[2], weight)
                    else :
                        Z_ExtraEl_LepBDT_MC_TTbar_hist_EE.Fill(event.LepBDT[2], weight)

                elif(int(math.fabs(event.LepLepId[2])) == 13 ) :
                    
                    Z_ExtraMu_LepBDT_MC_TTbar_hist.Fill(event.LepBDT[2], weight)

                    if math.fabs(event.LepEta[2]) <= 1. :
                        Z_ExtraMu_LepBDT_MC_TTbar_hist_MB.Fill(event.LepBDT[2], weight)
                    else :
                        Z_ExtraMu_LepBDT_MC_TTbar_hist_ME.Fill(event.LepBDT[2], weight)

                else :
                    print "Error: wrong particle ID!"


    #save histograms in a root file 
    print "saving histograms into root file ..."
    LepBDT_MC_TTbar_outFile = TFile.Open("LepBDTdistrib_MC_TTbar_"+ period + "_" + treeText +".root", "RECREATE")
    LepBDT_MC_TTbar_outFile.cd()

    Z_ele_1st_LepBDT_MC_TTbar_hist.Write()
    Z_ele_1st_LepBDT_MC_TTbar_hist_EB.Write()
    Z_ele_1st_LepBDT_MC_TTbar_hist_EE.Write()
                                                                                   
    Z_mu_1st_LepBDT_MC_TTbar_hist.Write()
    Z_mu_1st_LepBDT_MC_TTbar_hist_MB.Write()
    Z_mu_1st_LepBDT_MC_TTbar_hist_ME.Write()
                                
                                
    if CRZLTree :               
        Z_ExtraEl_LepBDT_MC_TTbar_hist.Write()
        Z_ExtraEl_LepBDT_MC_TTbar_hist_EB.Write()
        Z_ExtraEl_LepBDT_MC_TTbar_hist_EE.Write()
                                
        Z_ExtraMu_LepBDT_MC_TTbar_hist.Write()
        Z_ExtraMu_LepBDT_MC_TTbar_hist_MB.Write()
        Z_ExtraMu_LepBDT_MC_TTbar_hist_ME.Write()


    LepBDT_MC_TTbar_outFile.Close()
    print "MC TTbar histo file created!"
# ********************


# ****************************************
# create output directory 
# ****************************************
outputDir = "LepBDTdistrib_DATAvsMC_" + str(period) + "_" + str(treeText)
gSystem.Exec("mkdir -p " + outputDir)
print "Output directory created!"

# **************************
# read data histos from file 
# **************************
histoDATA_input = TFile.Open("LepBDTdistrib_DATA_"+ period + "_" + treeText +".root")
print 'Reading file', histoDATA_input.GetName(),'...'

LepBDTDATA_list = []

LepBDTDATA_list.append(histoDATA_input.Get('Z_ele_1st_LepBDT_hist'))
LepBDTDATA_list.append(histoDATA_input.Get('Z_ele_1st_LepBDT_hist_EB'))
LepBDTDATA_list.append(histoDATA_input.Get('Z_ele_1st_LepBDT_hist_EE'))
LepBDTDATA_list.append(histoDATA_input.Get('Z_mu_1st_LepBDT_hist'))
LepBDTDATA_list.append(histoDATA_input.Get('Z_mu_1st_LepBDT_hist_MB'))
LepBDTDATA_list.append(histoDATA_input.Get('Z_mu_1st_LepBDT_hist_ME'))

if CRZLTree :
    LepBDTDATA_list.append(histoDATA_input.Get('Z_ExtraEl_LepBDT_hist'))
    LepBDTDATA_list.append(histoDATA_input.Get('Z_ExtraEl_LepBDT_hist_EB'))
    LepBDTDATA_list.append(histoDATA_input.Get('Z_ExtraEl_LepBDT_hist_EE'))
    LepBDTDATA_list.append(histoDATA_input.Get('Z_ExtraMu_LepBDT_hist'))
    LepBDTDATA_list.append(histoDATA_input.Get('Z_ExtraMu_LepBDT_hist_MB'))
    LepBDTDATA_list.append(histoDATA_input.Get('Z_ExtraMu_LepBDT_hist_ME'))


# ****************************
# read DY MC histos from file 
# ****************************
histoMCDY_input = TFile.Open("LepBDTdistrib_MC_DY_"+ period + "_" + treeText +".root")
print 'Reading file', histoMCDY_input.GetName(),'...'

LepBDTMCDY_list = []

LepBDTMCDY_list.append(histoMCDY_input.Get('Z_ele_1st_LepBDT_MC_DY_hist'))
LepBDTMCDY_list.append(histoMCDY_input.Get('Z_ele_1st_LepBDT_MC_DY_hist_EB'))
LepBDTMCDY_list.append(histoMCDY_input.Get('Z_ele_1st_LepBDT_MC_DY_hist_EE'))
LepBDTMCDY_list.append(histoMCDY_input.Get('Z_mu_1st_LepBDT_MC_DY_hist'))
LepBDTMCDY_list.append(histoMCDY_input.Get('Z_mu_1st_LepBDT_MC_DY_hist_MB'))
LepBDTMCDY_list.append(histoMCDY_input.Get('Z_mu_1st_LepBDT_MC_DY_hist_ME'))

if CRZLTree :
    LepBDTMCDY_list.append(histoMCDY_input.Get('Z_ExtraEl_LepBDT_MC_DY_hist'))
    LepBDTMCDY_list.append(histoMCDY_input.Get('Z_ExtraEl_LepBDT_MC_DY_hist_EB'))
    LepBDTMCDY_list.append(histoMCDY_input.Get('Z_ExtraEl_LepBDT_MC_DY_hist_EE'))
    LepBDTMCDY_list.append(histoMCDY_input.Get('Z_ExtraMu_LepBDT_MC_DY_hist'))
    LepBDTMCDY_list.append(histoMCDY_input.Get('Z_ExtraMu_LepBDT_MC_DY_hist_MB'))
    LepBDTMCDY_list.append(histoMCDY_input.Get('Z_ExtraMu_LepBDT_MC_DY_hist_ME'))


# ******************************
# read TTbar MC histos from file 
# ******************************
histoMCTTbar_input = TFile.Open("LepBDTdistrib_MC_TTbar_"+ period + "_" + treeText +".root")
print 'Reading file', histoMCTTbar_input.GetName(),'...'

LepBDTMCTTbar_list = []

LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_ele_1st_LepBDT_MC_TTbar_hist'))
LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_ele_1st_LepBDT_MC_TTbar_hist_EB'))
LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_ele_1st_LepBDT_MC_TTbar_hist_EE'))
LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_mu_1st_LepBDT_MC_TTbar_hist'))
LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_mu_1st_LepBDT_MC_TTbar_hist_MB'))
LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_mu_1st_LepBDT_MC_TTbar_hist_ME'))

if CRZLTree :
    LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_ExtraEl_LepBDT_MC_TTbar_hist'))
    LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_ExtraEl_LepBDT_MC_TTbar_hist_EB'))
    LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_ExtraEl_LepBDT_MC_TTbar_hist_EE'))
    LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_ExtraMu_LepBDT_MC_TTbar_hist'))
    LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_ExtraMu_LepBDT_MC_TTbar_hist_MB'))
    LepBDTMCTTbar_list.append(histoMCTTbar_input.Get('Z_ExtraMu_LepBDT_MC_TTbar_hist_ME'))


# ******************************
# do DATA vs MC comparison plots  
# ******************************

for i in range(len(LepBDTDATA_list)) : 

    canvas = TCanvas("canvas","canvas",800,800)

    hs = THStack("hs","")

    norm = 1                                                                           # Normalize to MC cross-section 
    #norm = LepBDTDATA_list[i].Integral() / (LepBDTMCTTbar_list[i].Integral() + LepBDTMCDY_list[i].Integral()) # Normalize MC to data

    #DATA hist
    LepBDTDATA_list[i].SetMarkerStyle(20)
    LepBDTDATA_list[i].SetMarkerSize(0.6)

    #MC TTbar hist
    LepBDTMCTTbar_list[i].Scale(norm) # MC normalization
    LepBDTMCTTbar_list[i].SetFillColor(kMagenta+3)
    LepBDTMCTTbar_list[i].SetLineColor(kBlack)
    hs.Add(LepBDTMCTTbar_list[i])

    #MC DY hist
    LepBDTMCDY_list[i].Scale(norm) # MC normalization
    LepBDTMCDY_list[i].SetFillColor(kMagenta-6)
    LepBDTMCDY_list[i].SetLineColor(kBlack)
    hs.Add(LepBDTMCDY_list[i])

    #upper plot pad
    pad1 = TPad("pad1","pad1", 0, 0.3, 1, 1.0)
    pad1.Draw()
    pad1.cd()

    hs.SetMaximum(1.6*max(hs.GetMaximum(),LepBDTDATA_list[i].GetMaximum()))
    LepBDTDATA_list[i].SetMaximum(1.6*max(hs.GetMaximum(),LepBDTDATA_list[i].GetMaximum()))
    # EF for ele BDT
    #hs.SetMinimum(10) 

    hs.Draw("histo")
    LepBDTDATA_list[i].Draw("sameEP")

    hs.SetTitle("")
    hs.GetXaxis().SetTitle("BDT score")
    #hs.GetXaxis().SetRangeUser(0.75,1) #EF for ele BDT
    hs.GetXaxis().SetLabelFont(43)
    hs.GetXaxis().SetLabelSize(15)
    hs.GetYaxis().SetTitleSize(20)
    hs.GetYaxis().SetTitleFont(43)
    hs.GetYaxis().SetTitleOffset(1.8)
    hs.GetYaxis().SetLabelFont(43)
    hs.GetYaxis().SetLabelSize(15)
    hs.GetYaxis().SetTitle("Events")

    gStyle.SetOptStat(0)
    pad1.SetLogy()

    # legend
    legend = TLegend(0.1,0.75,0.3,0.9) #left alignment
    #legend = TLegend(0.7,0.75,0.9,0.9) #right alignment
    legend.AddEntry(LepBDTDATA_list[i],"Data", "p")
    legend.AddEntry(LepBDTMCDY_list[i],"DY MC","f")
    legend.AddEntry(LepBDTMCTTbar_list[i],"t#bar{t} MC","f")
    legend.SetFillColor(kWhite)
    legend.SetLineColor(kBlack)
    legend.SetTextFont(43)
    legend.SetTextSize(20)
    legend.Draw()
  
    canvas.Update()


    #lower plot pad
    canvas.cd()
    pad2 = TPad("pad2","pad2", 0, 0.05, 1, 0.3)
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()    #pad2 becomes the current pad

    
    #define ratio plot
    rp = TH1F(LepBDTDATA_list[i].Clone("rp"))
    rp.SetLineColor(kBlack)
    rp.SetMinimum(0.5)
    rp.SetMaximum(2.)
    rp.SetStats(0)
    rp.Divide(TH1F(LepBDTMCDY_list[i]+LepBDTMCTTbar_list[i]))   #divide histo rp/MC
    rp.SetMarkerStyle(24)
    rp.SetTitle("") 
    
    rp.SetYTitle("Data/MC")
    rp.GetYaxis().SetNdivisions(505)
    rp.GetYaxis().SetTitleSize(20)
    rp.GetYaxis().SetTitleFont(43)
    rp.GetYaxis().SetTitleOffset(1.55)
    rp.GetYaxis().SetLabelFont(43)
    rp.GetYaxis().SetLabelSize(15)

    #rp.GetXaxis().SetRangeUser(0.75,1) #EF for ele BDT
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
    CMS_lumi.CMS_lumi(pad1, 0, 0)
    
    
    canvas.Update()


    canvas.SaveAs(outputDir + "/" + LepBDTDATA_list[i].GetTitle() + ".pdf")
    canvas.SaveAs(outputDir + "/" + LepBDTDATA_list[i].GetTitle() + ".png")


print "plots done"
