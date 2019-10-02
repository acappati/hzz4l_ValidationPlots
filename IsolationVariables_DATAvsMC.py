#!/usr/bin/en math

# ***************************************
# usage: 
#    python IsolationVariables_DATAvsMC.py
#
# ***************************************

import json
import ROOT, math, helper, CMSGraphics, CMS_lumi
from ROOT import TFile, TH1, TH1F, TCanvas, gSystem, TAttFill, TLegend, TRatioPlot, TPad, TStyle, THStack, TPaveText, gStyle
from helper import ReadJSON
from CMSGraphics import makeCMSCanvas, makeLegend
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange


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
    inputDATAtree    = TFile.Open("root://lxcms03//data3/Higgs/190617/Data_2017/AllData/ZZ4lAnalysis.root")         #2017 data (rereco json)   
    inputMCDYtree    = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2017/DYJetsToLL_M50_LO/ZZ4lAnalysis.root") #DYJets 2017 MC (LO)
    inputMCTTbartree = TFile.Open("root://lxcms03//data3/Higgs/190617/MC_2017/TTTo2L2Nu/ZZ4lAnalysis.root")        #TTbarJets 2017 MC
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
    inputDATAtree    = TFile.Open("../ZZ4lAnalysis.root")        #2018 data    
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



# ***********************
# create output directory
# ***********************
OutputPath = "ControlVariablesForBDT_DATAvsMC_" + str(period) + "_" + str(treeText)
gSystem.Exec("mkdir -p " + OutputPath)
print "Output directory created!"



# ********************
#  do DATA histos 
# ********************
if(redoDATAHistos) :

    TH1.SetDefaultSumw2() # set sumw2 = true for all the histograms created from now on

    # ******************************
    # Define data histograms Z->ee
    # ******************************
    #missingHit_hist               = TH1F('missingHit', 'Missing Hit',                                  6, 0, 6) 
    #ele_1st_missingHit_hist       = TH1F('1st_missingHit_ele', 'Missing Hit ele',                      3, 0, 6) 
    ele_1st_chargedHadIso_hist    = TH1F('1st_chargedHadIso_ele', 'ChargedHadIso ele',                 400, 0, 4) 
    ele_1st_chargedHadIso_EB_hist = TH1F('1st_chargedHadIso_EB_ele', 'ChargedHadIso ele in Barrel',    400, 0, 4) 
    ele_1st_chargedHadIso_EE_hist = TH1F('1st_chargedHadIso_EE_ele', 'ChargedHadIso ele in Endcap',    400, 0, 4) 
    ele_1st_neutralHadIso_hist    = TH1F('1st_neutralHadIso_ele', 'NeutralHadIso ele',                 400, 0, 4) 
    ele_1st_neutralHadIso_EB_hist = TH1F('1st_neutralHadIso_EB_ele', 'NeutralHadIso ele in Barrel',    400, 0, 4) 
    ele_1st_neutralHadIso_EE_hist = TH1F('1st_neutralHadIso_EE_ele', 'NeutralHadIso ele in Endcap',    400, 0, 4) 
    ele_1st_photonIso_hist        = TH1F('1st_photonIso_ele', 'PhotonIso ele',                         400, 0, 4) 
    ele_1st_photonIso_EB_hist     = TH1F('1st_photonIso_EB_ele', 'PhotonIso ele in Barrel',            400, 0, 4) 
    ele_1st_photonIso_EE_hist     = TH1F('1st_photonIso_EE_ele', 'PhotonIso ele in Endcap',            400, 0, 4) 
    ele_1st_combRelIsoPF_hist     = TH1F('1st_combRelIsoPF_ele', 'CombRelIsoPF ele',                   100, 0, 1.) 
    ele_1st_combRelIsoPF_EB_hist  = TH1F('1st_combRelIsoPF_EB_ele', 'CombRelIsoPF ele in Barrel',      100, 0, 1.) 
    ele_1st_combRelIsoPF_EE_hist  = TH1F('1st_combRelIsoPF_EE_ele', 'CombRelIsoPF ele in Endcap',      100, 0, 1.) 

    # ******************************
    # Define data histograms Z->mumu
    # ******************************
    #mu_1st_missingHit_hist       = TH1F('1st_missingHit_mu', 'Missing Hit mu',                      3, 0, 6) 
    mu_1st_chargedHadIso_hist    = TH1F('1st_chargedHadIso_mu', 'ChargedHadIso mu',                 400, 0, 4) 
    mu_1st_chargedHadIso_MB_hist = TH1F('1st_chargedHadIso_MB_mu', 'ChargedHadIso mu in Barrel',    400, 0, 4) 
    mu_1st_chargedHadIso_ME_hist = TH1F('1st_chargedHadIso_ME_mu', 'ChargedHadIso mu in Endcap',    400, 0, 4) 
    mu_1st_neutralHadIso_hist    = TH1F('1st_neutralHadIso_mu', 'NeutralHadIso mu',                 400, 0, 4) 
    mu_1st_neutralHadIso_MB_hist = TH1F('1st_neutralHadIso_MB_mu', 'NeutralHadIso mu in Barrel',    400, 0, 4) 
    mu_1st_neutralHadIso_ME_hist = TH1F('1st_neutralHadIso_ME_mu', 'NeutralHadIso mu in Endcap',    400, 0, 4) 
    mu_1st_photonIso_hist        = TH1F('1st_photonIso_mu', 'PhotonIso mu',                         400, 0, 4) 
    mu_1st_photonIso_MB_hist     = TH1F('1st_photonIso_MB_mu', 'PhotonIso mu in Barrel',            400, 0, 4) 
    mu_1st_photonIso_ME_hist     = TH1F('1st_photonIso_ME_mu', 'PhotonIso mu in Endcap',            400, 0, 4) 
    mu_1st_combRelIsoPF_hist     = TH1F('1st_combRelIsoPF_mu', 'CombRelIsoPF mu',                   100, 0, 1.) 
    mu_1st_combRelIsoPF_MB_hist  = TH1F('1st_combRelIsoPF_MB_mu', 'CombRelIsoPF mu in Barrel',      100, 0, 1.) 
    mu_1st_combRelIsoPF_ME_hist  = TH1F('1st_combRelIsoPF_ME_mu', 'CombRelIsoPF mu in Endcap',      100, 0, 1.) 


    #############
    # read tree #
    #############
    print "reading tree", inputDATAtree.GetName(),treeText,treeDATA.GetName()  ,"..."
    
    treeDATA.SetBranchStatus("*",0)  # disable all branches
    if ZTree :
        treeDATA.SetBranchStatus("Zsel",1)
    else :
        treeDATA.SetBranchStatus("ZZsel",1)
    treeDATA.SetBranchStatus("LepLepId",1)
    treeDATA.SetBranchStatus("LepPt",1)
    treeDATA.SetBranchStatus("LepEta",1)
    treeDATA.SetBranchStatus("nCleanedJetsPt30" ,1)
    treeDATA.SetBranchStatus("LepChargedHadIso",1)
    treeDATA.SetBranchStatus("LepNeutralHadIso",1)
    treeDATA.SetBranchStatus("LepPhotonIso",1)
    treeDATA.SetBranchStatus("LepCombRelIsoPF",1)
    treeDATA.SetBranchStatus("ZMass",1)
    #treeDATA.SetBranchStatus("LepMissingHit",1)

    for event in treeDATA:
        if ZTree :
            if ( event.Zsel < 0 ) : continue # skip events that do not pass the trigger
        else :
            if ( event.ZZsel < 0 ) : continue # skip events that do not pass the trigger

        if (event.ZMass < 80. or event.ZMass > 100.): continue
        if (event.LepPt[0] < 30.) : continue

        #missingHit_hist.Fill(LepMissingHit[0])


        ##############
        # Zee histos #
        ##############
        if((int(math.fabs(event.LepLepId[0])) == 11)) :

            if event.LepPt[0] >= event.LepPt[1] :
                ele_1st_chargedHadIso_hist.Fill(event.LepChargedHadIso[0])
                ele_1st_neutralHadIso_hist.Fill(event.LepNeutralHadIso[0])
                ele_1st_photonIso_hist.Fill(event.LepPhotonIso[0])
                ele_1st_combRelIsoPF_hist.Fill(event.LepCombRelIsoPF[0])
                if math.fabs(event.LepEta[0]) <= 1.479 :
                    ele_1st_chargedHadIso_EB_hist.Fill(event.LepChargedHadIso[0])
                    ele_1st_neutralHadIso_EB_hist.Fill(event.LepNeutralHadIso[0])
                    ele_1st_photonIso_EB_hist.Fill(event.LepPhotonIso[0])
                    ele_1st_combRelIsoPF_EB_hist.Fill(event.LepCombRelIsoPF[0])
                else :
                    ele_1st_chargedHadIso_EE_hist.Fill(event.LepChargedHadIso[0])
                    ele_1st_neutralHadIso_EE_hist.Fill(event.LepNeutralHadIso[0])
                    ele_1st_photonIso_EE_hist.Fill(event.LepPhotonIso[0])
                    ele_1st_combRelIsoPF_EE_hist.Fill(event.LepCombRelIsoPF[0])

            else :
                ele_1st_chargedHadIso_hist.Fill(event.LepChargedHadIso[1])
                ele_1st_neutralHadIso_hist.Fill(event.LepNeutralHadIso[1])
                ele_1st_photonIso_hist.Fill(event.LepPhotonIso[1])
                ele_1st_combRelIsoPF_hist.Fill(event.LepCombRelIsoPF[1])
                if math.fabs(event.LepEta[0]) <= 1.479 :
                    ele_1st_chargedHadIso_EB_hist.Fill(event.LepChargedHadIso[1])
                    ele_1st_neutralHadIso_EB_hist.Fill(event.LepNeutralHadIso[1])
                    ele_1st_photonIso_EB_hist.Fill(event.LepPhotonIso[1])
                    ele_1st_combRelIsoPF_EB_hist.Fill(event.LepCombRelIsoPF[1])
                else :
                    ele_1st_chargedHadIso_EE_hist.Fill(event.LepChargedHadIso[1])
                    ele_1st_neutralHadIso_EE_hist.Fill(event.LepNeutralHadIso[1])
                    ele_1st_photonIso_EE_hist.Fill(event.LepPhotonIso[1])
                    ele_1st_combRelIsoPF_EE_hist.Fill(event.LepCombRelIsoPF[1])

        ################
        # Zmumu histos #
        ################
        if((int(math.fabs(event.LepLepId[0])) == 13)) :

            #mu_1st_missingHit_hist.Fill(LepMissingHit)

            if event.LepPt[0] >= event.LepPt[1] :
                mu_1st_chargedHadIso_hist.Fill(event.LepChargedHadIso[0])
                mu_1st_neutralHadIso_hist.Fill(event.LepNeutralHadIso[0])
                mu_1st_photonIso_hist.Fill(event.LepPhotonIso[0])
                mu_1st_combRelIsoPF_hist.Fill(event.LepCombRelIsoPF[0])
                if math.fabs(event.LepEta[0]) <= 1. :
                    mu_1st_chargedHadIso_MB_hist.Fill(event.LepChargedHadIso[0])
                    mu_1st_neutralHadIso_MB_hist.Fill(event.LepNeutralHadIso[0])
                    mu_1st_photonIso_MB_hist.Fill(event.LepPhotonIso[0])
                    mu_1st_combRelIsoPF_MB_hist.Fill(event.LepCombRelIsoPF[0])
                else :
                    mu_1st_chargedHadIso_ME_hist.Fill(event.LepChargedHadIso[0])
                    mu_1st_neutralHadIso_ME_hist.Fill(event.LepNeutralHadIso[0])
                    mu_1st_photonIso_ME_hist.Fill(event.LepPhotonIso[0])
                    mu_1st_combRelIsoPF_ME_hist.Fill(event.LepCombRelIsoPF[0])

            else :
                mu_1st_chargedHadIso_hist.Fill(event.LepChargedHadIso[1])
                mu_1st_neutralHadIso_hist.Fill(event.LepNeutralHadIso[1])
                mu_1st_photonIso_hist.Fill(event.LepPhotonIso[1])
                mu_1st_combRelIsoPF_hist.Fill(event.LepCombRelIsoPF[1])
                if math.fabs(event.LepEta[0]) <= 1. :
                    mu_1st_chargedHadIso_MB_hist.Fill(event.LepChargedHadIso[1])
                    mu_1st_neutralHadIso_MB_hist.Fill(event.LepNeutralHadIso[1])
                    mu_1st_photonIso_MB_hist.Fill(event.LepPhotonIso[1])
                    mu_1st_combRelIsoPF_MB_hist.Fill(event.LepCombRelIsoPF[1])
                else :
                    mu_1st_chargedHadIso_ME_hist.Fill(event.LepChargedHadIso[1])
                    mu_1st_neutralHadIso_ME_hist.Fill(event.LepNeutralHadIso[1])
                    mu_1st_photonIso_ME_hist.Fill(event.LepPhotonIso[1])
                    mu_1st_combRelIsoPF_ME_hist.Fill(event.LepCombRelIsoPF[1])


    #save histograms in a root file                                                                                                                                                                         
    print "saving DATA histograms into root file ..."
    DATA_outFile = TFile.Open("ControlVariablesForBDT_DATA_"+ period + "_" + treeText +".root", "RECREATE")
    DATA_outFile.cd()

    #missingHit_hist.Write()       
    #ele_1st_missingHit_hist.Write()       
    ele_1st_chargedHadIso_hist.Write()   
    ele_1st_chargedHadIso_EB_hist.Write()  
    ele_1st_chargedHadIso_EE_hist.Write()  
    ele_1st_neutralHadIso_hist.Write()     
    ele_1st_neutralHadIso_EB_hist.Write()  
    ele_1st_neutralHadIso_EE_hist.Write()  
    ele_1st_photonIso_hist.Write()         
    ele_1st_photonIso_EB_hist.Write()      
    ele_1st_photonIso_EE_hist.Write()     
    ele_1st_combRelIsoPF_hist.Write()      
    ele_1st_combRelIsoPF_EB_hist.Write()   
    ele_1st_combRelIsoPF_EE_hist.Write()  

    #mu_1st_missingHit_hist.Write()       
    mu_1st_chargedHadIso_hist.Write()   
    mu_1st_chargedHadIso_MB_hist.Write()  
    mu_1st_chargedHadIso_ME_hist.Write()  
    mu_1st_neutralHadIso_hist.Write()     
    mu_1st_neutralHadIso_MB_hist.Write()  
    mu_1st_neutralHadIso_ME_hist.Write()  
    mu_1st_photonIso_hist.Write()         
    mu_1st_photonIso_MB_hist.Write()      
    mu_1st_photonIso_ME_hist.Write()     
    mu_1st_combRelIsoPF_hist.Write()      
    mu_1st_combRelIsoPF_MB_hist.Write()   
    mu_1st_combRelIsoPF_ME_hist.Write()  

    DATA_outFile.Close()
    print "DATA histo file created!"

# ********************
#  do MC DY histos 
# ********************
if(redoMCDYHistos) :

    TH1.SetDefaultSumw2() # set sumw2 = true for all the histograms created from now on

    # ******************************
    # Define data histograms Z->ee
    # ******************************
    #missingHit_MC_DY_hist               = TH1F('missingHit_MC_DY', 'Missing Hit',                                  6, 0, 6) 
    ele_1st_chargedHadIso_MC_DY_hist    = TH1F('1st_chargedHadIso_MC_DY_ele', 'ChargedHadIso ele DY',                 400, 0, 4) 
    ele_1st_chargedHadIso_EB_MC_DY_hist = TH1F('1st_chargedHadIso_EB_MC_DY_ele', 'ChargedHadIso ele in Barrel DY',    400, 0, 4) 
    ele_1st_chargedHadIso_EE_MC_DY_hist = TH1F('1st_chargedHadIso_EE_MC_DY_ele', 'ChargedHadIso ele in Endcap DY',    400, 0, 4) 
    ele_1st_neutralHadIso_MC_DY_hist    = TH1F('1st_neutralHadIso_MC_DY_ele', 'NeutralHadIso ele DY',                 400, 0, 4) 
    ele_1st_neutralHadIso_EB_MC_DY_hist = TH1F('1st_neutralHadIso_EB_MC_DY_ele', 'NeutralHadIso ele in Barrel DY',    400, 0, 4) 
    ele_1st_neutralHadIso_EE_MC_DY_hist = TH1F('1st_neutralHadIso_EE_MC_DY_ele', 'NeutralHadIso ele in Endcap DY',    400, 0, 4) 
    ele_1st_photonIso_MC_DY_hist        = TH1F('1st_photonIso_MC_DY_ele', 'PhotonIso ele DY',                         400, 0, 4) 
    ele_1st_photonIso_EB_MC_DY_hist     = TH1F('1st_photonIso_EB_MC_DY_ele', 'PhotonIso ele in Barrel DY',            400, 0, 4) 
    ele_1st_photonIso_EE_MC_DY_hist     = TH1F('1st_photonIso_EE_MC_DY_ele', 'PhotonIso ele in Endcap DY',            400, 0, 4) 
    ele_1st_combRelIsoPF_MC_DY_hist     = TH1F('1st_combRelIsoPF_MC_DY_ele', 'CombRelIsoPF ele  DY',                  100, 0, 1.) 
    ele_1st_combRelIsoPF_EB_MC_DY_hist  = TH1F('1st_combRelIsoPF_EB_MC_DY_ele', 'CombRelIsoPF ele in Barrel DY',      100, 0, 1.) 
    ele_1st_combRelIsoPF_EE_MC_DY_hist  = TH1F('1st_combRelIsoPF_EE_MC_DY_ele', 'CombRelIsoPF ele in Endcap DY',      100, 0, 1.) 

    # ******************************
    # Define data histograms Z->mumu
    # ******************************
    mu_1st_chargedHadIso_MC_DY_hist    = TH1F('1st_chargedHadIso_MC_DY_mu', 'ChargedHadIso mu DY',                 400, 0, 4) 
    mu_1st_chargedHadIso_MB_MC_DY_hist = TH1F('1st_chargedHadIso_MB_MC_DY_mu', 'ChargedHadIso mu in Barrel DY',    400, 0, 4) 
    mu_1st_chargedHadIso_ME_MC_DY_hist = TH1F('1st_chargedHadIso_ME_MC_DY_mu', 'ChargedHadIso mu in Endcap DY',    400, 0, 4) 
    mu_1st_neutralHadIso_MC_DY_hist    = TH1F('1st_neutralHadIso_MC_DY_mu', 'NeutralHadIso mu DY',                 400, 0, 4) 
    mu_1st_neutralHadIso_MB_MC_DY_hist = TH1F('1st_neutralHadIso_MB_MC_DY_mu', 'NeutralHadIso mu in Barrel DY',    400, 0, 4) 
    mu_1st_neutralHadIso_ME_MC_DY_hist = TH1F('1st_neutralHadIso_ME_MC_DY_mu', 'NeutralHadIso mu in Endcap DY',    400, 0, 4) 
    mu_1st_photonIso_MC_DY_hist        = TH1F('1st_photonIso_MC_DY_mu', 'PhotonIso mu DY',                         400, 0, 4) 
    mu_1st_photonIso_MB_MC_DY_hist     = TH1F('1st_photonIso_MB_MC_DY_mu', 'PhotonIso mu in Barrel DY',            400, 0, 4) 
    mu_1st_photonIso_ME_MC_DY_hist     = TH1F('1st_photonIso_ME_MC_DY_mu', 'PhotonIso mu in Endcap DY',            400, 0, 4) 
    mu_1st_combRelIsoPF_MC_DY_hist     = TH1F('1st_combRelIsoPF_MC_DY_mu', 'CombRelIsoPF mu DY',                   100, 0, 1.) 
    mu_1st_combRelIsoPF_MB_MC_DY_hist  = TH1F('1st_combRelIsoPF_EB_MC_DY_mu', 'CombRelIsoPF mu in Barrel DY',      100, 0, 1.) 
    mu_1st_combRelIsoPF_ME_MC_DY_hist  = TH1F('1st_combRelIsoPF_EE_MC_DY_mu', 'CombRelIsoPF mu in Endcap DY',      100, 0, 1.) 


    # get partial event weight                                                                                                                                                      
    if (ZTree) :
        hcounters           = inputMCDYtree.Get("ZTree/Counters")
        gen_sumWeights      = hcounters.GetBinContent(1)
        partialSampleWeight = lumi * 1000 / gen_sumWeights
    elif (ZZTree) :
        hcounters           = inputMCDYtree.Get("ZZTree/Counters")
        gen_sumWeights      = hcounters.GetBinContent(40)
        partialSampleWeight = lumi * 1000 / gen_sumWeights
    elif (CRZLTree) :
        hcounters           = inputMCDYtree.Get("CRZLTree/Counters")
        gen_sumWeights      = hcounters.GetBinContent(40)
        partialSampleWeight = lumi * 1000 / gen_sumWeights
    elif (CRZLLTree) :
        hcounters           = inputMCDYtree.Get("CRZLLTree/Counters")
        gen_sumWeights      = hcounters.GetBinContent(40)
        partialSampleWeight = lumi * 1000 / gen_sumWeights

    #############
    # read tree #
    #############
    print "reading tree", inputMCDYtree.GetName(),treeText,treeDATA.GetName()  ,"..."
    
    
    for event in treeMCDY:
        if ZTree :
            if ( event.Zsel < 0 ) : continue # skip events that do not pass the trigger
        else :
            if ( event.ZZsel < 0 ) : continue # skip events that do not pass the trigger

        weight = partialSampleWeight*event.xsec*event.overallEventWeight

        if (event.ZMass < 80. or event.ZMass > 100.): continue
        if (event.LepPt[0] < 30.) : continue

        #missingHit_MC_DY_hist.Fill(LepMissingHit, weight)

        ##############
        # Zee histos #
        ##############
        if((int(math.fabs(event.LepLepId[0])) == 11)) :

            if event.LepPt[0] >= event.LepPt[1] :
                ele_1st_chargedHadIso_MC_DY_hist.Fill(event.LepChargedHadIso[0], weight)
                ele_1st_neutralHadIso_MC_DY_hist.Fill(event.LepNeutralHadIso[0], weight)
                ele_1st_photonIso_MC_DY_hist.Fill(event.LepPhotonIso[0], weight)
                ele_1st_combRelIsoPF_MC_DY_hist.Fill(event.LepCombRelIsoPF[0], weight)
                if math.fabs(event.LepEta[0]) <= 1.479 :
                    ele_1st_chargedHadIso_EB_MC_DY_hist.Fill(event.LepChargedHadIso[0], weight)
                    ele_1st_neutralHadIso_EB_MC_DY_hist.Fill(event.LepNeutralHadIso[0], weight)
                    ele_1st_photonIso_EB_MC_DY_hist.Fill(event.LepPhotonIso[0], weight)
                    ele_1st_combRelIsoPF_EB_MC_DY_hist.Fill(event.LepCombRelIsoPF[0], weight)
                else :
                    ele_1st_chargedHadIso_EE_MC_DY_hist.Fill(event.LepChargedHadIso[0], weight)
                    ele_1st_neutralHadIso_EE_MC_DY_hist.Fill(event.LepNeutralHadIso[0], weight)
                    ele_1st_photonIso_EE_MC_DY_hist.Fill(event.LepPhotonIso[0], weight)
                    ele_1st_combRelIsoPF_EE_MC_DY_hist.Fill(event.LepCombRelIsoPF[0], weight)

            else :
                ele_1st_chargedHadIso_MC_DY_hist.Fill(event.LepChargedHadIso[1], weight)
                ele_1st_neutralHadIso_MC_DY_hist.Fill(event.LepNeutralHadIso[1], weight)
                ele_1st_photonIso_MC_DY_hist.Fill(event.LepPhotonIso[1], weight)
                ele_1st_combRelIsoPF_MC_DY_hist.Fill(event.LepCombRelIsoPF[1], weight)
                if math.fabs(event.LepEta[0]) <= 1.479 :
                    ele_1st_chargedHadIso_EB_MC_DY_hist.Fill(event.LepChargedHadIso[1], weight)
                    ele_1st_neutralHadIso_EB_MC_DY_hist.Fill(event.LepNeutralHadIso[1], weight)
                    ele_1st_photonIso_EB_MC_DY_hist.Fill(event.LepPhotonIso[1], weight)
                    ele_1st_combRelIsoPF_EB_MC_DY_hist.Fill(event.LepCombRelIsoPF[1], weight)
                else :
                    ele_1st_chargedHadIso_EE_MC_DY_hist.Fill(event.LepChargedHadIso[1], weight)
                    ele_1st_neutralHadIso_EE_MC_DY_hist.Fill(event.LepNeutralHadIso[1], weight)
                    ele_1st_photonIso_EE_MC_DY_hist.Fill(event.LepPhotonIso[1]), weight
                    ele_1st_combRelIsoPF_EE_MC_DY_hist.Fill(event.LepCombRelIsoPF[1], weight)

        ################
        # Zmumu histos #
        ################
        if((int(math.fabs(event.LepLepId[0])) == 13)) :

            if event.LepPt[0] >= event.LepPt[1] :
                mu_1st_chargedHadIso_MC_DY_hist.Fill(event.LepChargedHadIso[0], weight)
                mu_1st_neutralHadIso_MC_DY_hist.Fill(event.LepNeutralHadIso[0], weight)
                mu_1st_photonIso_MC_DY_hist.Fill(event.LepPhotonIso[0], weight)
                mu_1st_combRelIsoPF_MC_DY_hist.Fill(event.LepCombRelIsoPF[0], weight)
                if math.fabs(event.LepEta[0]) <= 1.:
                    mu_1st_chargedHadIso_MB_MC_DY_hist.Fill(event.LepChargedHadIso[0], weight)
                    mu_1st_neutralHadIso_MB_MC_DY_hist.Fill(event.LepNeutralHadIso[0], weight)
                    mu_1st_photonIso_MB_MC_DY_hist.Fill(event.LepPhotonIso[0], weight)
                    mu_1st_combRelIsoPF_MB_MC_DY_hist.Fill(event.LepCombRelIsoPF[0], weight)
                else :
                    mu_1st_chargedHadIso_ME_MC_DY_hist.Fill(event.LepChargedHadIso[0], weight)
                    mu_1st_neutralHadIso_ME_MC_DY_hist.Fill(event.LepNeutralHadIso[0], weight)
                    mu_1st_photonIso_ME_MC_DY_hist.Fill(event.LepPhotonIso[0], weight)
                    mu_1st_combRelIsoPF_ME_MC_DY_hist.Fill(event.LepCombRelIsoPF[0], weight)

            else :
                mu_1st_chargedHadIso_MC_DY_hist.Fill(event.LepChargedHadIso[1], weight)
                mu_1st_neutralHadIso_MC_DY_hist.Fill(event.LepNeutralHadIso[1], weight)
                mu_1st_photonIso_MC_DY_hist.Fill(event.LepPhotonIso[1], weight)
                mu_1st_combRelIsoPF_MC_DY_hist.Fill(event.LepCombRelIsoPF[1], weight)
                if math.fabs(event.LepEta[0]) <= 1. :
                    mu_1st_chargedHadIso_MB_MC_DY_hist.Fill(event.LepChargedHadIso[1], weight)
                    mu_1st_neutralHadIso_MB_MC_DY_hist.Fill(event.LepNeutralHadIso[1], weight)
                    mu_1st_photonIso_MB_MC_DY_hist.Fill(event.LepPhotonIso[1], weight)
                    mu_1st_combRelIsoPF_MB_MC_DY_hist.Fill(event.LepCombRelIsoPF[1], weight)
                else :
                    mu_1st_chargedHadIso_ME_MC_DY_hist.Fill(event.LepChargedHadIso[1], weight)
                    mu_1st_neutralHadIso_ME_MC_DY_hist.Fill(event.LepNeutralHadIso[1], weight)
                    mu_1st_photonIso_ME_MC_DY_hist.Fill(event.LepPhotonIso[1], weight)
                    mu_1st_combRelIsoPF_ME_MC_DY_hist.Fill(event.LepCombRelIsoPF[1], weight)


    #save histograms in a root file                                                                                                                               
    print "saving MC DY histograms into root file ..."
    MCDY_outFile = TFile.Open("ControlVariablesForBDT_MCDY_"+ period + "_" + treeText +".root", "RECREATE")
    MCDY_outFile.cd()

    #missingHit_MC_DY_hist.Write()       
    ele_1st_chargedHadIso_MC_DY_hist.Write()   
    ele_1st_chargedHadIso_EB_MC_DY_hist.Write()  
    ele_1st_chargedHadIso_EE_MC_DY_hist.Write()  
    ele_1st_neutralHadIso_MC_DY_hist.Write()     
    ele_1st_neutralHadIso_EB_MC_DY_hist.Write()  
    ele_1st_neutralHadIso_EE_MC_DY_hist.Write()  
    ele_1st_photonIso_MC_DY_hist.Write()         
    ele_1st_photonIso_EB_MC_DY_hist.Write()      
    ele_1st_photonIso_EE_MC_DY_hist.Write()     
    ele_1st_combRelIsoPF_MC_DY_hist.Write()      
    ele_1st_combRelIsoPF_EB_MC_DY_hist.Write()   
    ele_1st_combRelIsoPF_EE_MC_DY_hist.Write()  

    mu_1st_chargedHadIso_MC_DY_hist.Write()   
    mu_1st_chargedHadIso_MB_MC_DY_hist.Write()  
    mu_1st_chargedHadIso_ME_MC_DY_hist.Write()  
    mu_1st_neutralHadIso_MC_DY_hist.Write()     
    mu_1st_neutralHadIso_MB_MC_DY_hist.Write()  
    mu_1st_neutralHadIso_ME_MC_DY_hist.Write()  
    mu_1st_photonIso_MC_DY_hist.Write()         
    mu_1st_photonIso_MB_MC_DY_hist.Write()      
    mu_1st_photonIso_ME_MC_DY_hist.Write()     
    mu_1st_combRelIsoPF_MC_DY_hist.Write()      
    mu_1st_combRelIsoPF_MB_MC_DY_hist.Write()   
    mu_1st_combRelIsoPF_ME_MC_DY_hist.Write()  

    MCDY_outFile.Close()
    print "MC DY histo file created!"

# ********************
#  do MC TTbar histos 
# ********************
if(redoMCTTbarHistos) :

    TH1.SetDefaultSumw2() # set sumw2 = true for all the histograms created from now on

    # ******************************
    # Define data histograms Z->ee
    # ******************************
    #missingHit_MC_TTbar_hist               = TH1F('1st_missingHit_MC_TTbar', 'Missing Hit',                                      6, 0, 6) 
    ele_1st_chargedHadIso_MC_TTbar_hist    = TH1F('1st_chargedHadIso_MC_TTbar_ele', 'ChargedHadIso ele TT',                 400, 0, 4) 
    ele_1st_chargedHadIso_EB_MC_TTbar_hist = TH1F('1st_chargedHadIso_EB_MC_TTbar_ele', 'ChargedHadIso ele in Barrel TT',    400, 0, 4) 
    ele_1st_chargedHadIso_EE_MC_TTbar_hist = TH1F('1st_chargedHadIso_EE_MC_TTbar_ele', 'ChargedHadIso ele in Endcap TT',    400, 0, 4) 
    ele_1st_neutralHadIso_MC_TTbar_hist    = TH1F('1st_neutralHadIso_MC_TTbar_ele', 'NeutralHadIso ele TT',                 400, 0, 4) 
    ele_1st_neutralHadIso_EB_MC_TTbar_hist = TH1F('1st_neutralHadIso_EB_MC_TTbar_ele', 'NeutralHadIso ele in Barrel TT',    400, 0, 4) 
    ele_1st_neutralHadIso_EE_MC_TTbar_hist = TH1F('1st_neutralHadIso_EE_MC_TTbar_ele', 'NeutralHadIso ele in Endcap TT',    400, 0, 4) 
    ele_1st_photonIso_MC_TTbar_hist        = TH1F('1st_photonIso_MC_TTbar_ele', 'PhotonIso ele TT',                         400, 0, 4) 
    ele_1st_photonIso_EB_MC_TTbar_hist     = TH1F('1st_photonIso_EB_MC_TTbar_ele', 'PhotonIso ele in Barrel TT',            400, 0, 4) 
    ele_1st_photonIso_EE_MC_TTbar_hist     = TH1F('1st_photonIso_EE_MC_TTbar_ele', 'PhotonIso ele in Endcap TT',            400, 0, 4) 
    ele_1st_combRelIsoPF_MC_TTbar_hist     = TH1F('1st_combRelIsoPF_MC_TTbar_ele', 'CombRelIsoPF ele TT',                   100, 0, 1.) 
    ele_1st_combRelIsoPF_EB_MC_TTbar_hist  = TH1F('1st_combRelIsoPF_EB_MC_TTbar_ele', 'CombRelIsoPF ele in Barrel TT',      100, 0, 1.) 
    ele_1st_combRelIsoPF_EE_MC_TTbar_hist  = TH1F('1st_combRelIsoPF_EE_MC_TTbar_ele', 'CombRelIsoPF ele in Endcap TT',      100, 0, 1.) 

    # ******************************
    # Define data histograms Z->mumu
    # ******************************
    mu_1st_chargedHadIso_MC_TTbar_hist    = TH1F('1st_chargedHadIso_MC_TTbar_mu', 'ChargedHadIso mu TT',                 400, 0, 4) 
    mu_1st_chargedHadIso_MB_MC_TTbar_hist = TH1F('1st_chargedHadIso_MB_MC_TTbar_mu', 'ChargedHadIso mu in Barrel TT',    400, 0, 4) 
    mu_1st_chargedHadIso_ME_MC_TTbar_hist = TH1F('1st_chargedHadIso_ME_MC_TTbar_mu', 'ChargedHadIso mu in Endcap TT',    400, 0, 4) 
    mu_1st_neutralHadIso_MC_TTbar_hist    = TH1F('1st_neutralHadIso_MC_TTbar_mu', 'NeutralHadIso mu TT',                 400, 0, 4) 
    mu_1st_neutralHadIso_MB_MC_TTbar_hist = TH1F('1st_neutralHadIso_MB_MC_TTbar_mu', 'NeutralHadIso mu in Barrel TT',    400, 0, 4) 
    mu_1st_neutralHadIso_ME_MC_TTbar_hist = TH1F('1st_neutralHadIso_ME_MC_TTbar_mu', 'NeutralHadIso mu in Endcap TT',    400, 0, 4) 
    mu_1st_photonIso_MC_TTbar_hist        = TH1F('1st_photonIso_MC_TTbar_mu', 'PhotonIso mu TT',                         400, 0, 4) 
    mu_1st_photonIso_MB_MC_TTbar_hist     = TH1F('1st_photonIso_MB_MC_TTbar_mu', 'PhotonIso mu in Barrel TT',            400, 0, 4) 
    mu_1st_photonIso_ME_MC_TTbar_hist     = TH1F('1st_photonIso_ME_MC_TTbar_mu', 'PhotonIso mu in Endcap TT',            400, 0, 4) 
    mu_1st_combRelIsoPF_MC_TTbar_hist     = TH1F('1st_combRelIsoPF_MC_TTbar_mu', 'CombRelIsoPF mu TT',                   100, 0, 1.) 
    mu_1st_combRelIsoPF_MB_MC_TTbar_hist  = TH1F('1st_combRelIsoPF_MB_MC_TTbar_mu', 'CombRelIsoPF mu in Barrel TT',      100, 0, 1.) 
    mu_1st_combRelIsoPF_ME_MC_TTbar_hist  = TH1F('1st_combRelIsoPF_ME_MC_TTbar_mu', 'CombRelIsoPF mu in Endcap TT',      100, 0, 1.) 


    # get partial event weight                                                                                                       
    if (ZTree) :
        hcounters           = inputMCTTbartree.Get("ZTree/Counters")
        gen_sumWeights      = hcounters.GetBinContent(1)
        partialSampleWeight = lumi * 1000 / gen_sumWeights
    elif (ZZTree) :
        hcounters           = inputMCTTbartree.Get("ZZTree/Counters")
        gen_sumWeights      = hcounters.GetBinContent(40)
        partialSampleWeight = lumi * 1000 / gen_sumWeights
    elif (CRZLTree) :
        hcounters           = inputMCTTbartree.Get("CRZLTree/Counters")
        gen_sumWeights      = hcounters.GetBinContent(40)
        partialSampleWeight = lumi * 1000 / gen_sumWeights
    elif (CRZLLTree) :
        hcounters           = inputMCTTbartree.Get("CRZLLTree/Counters")
        gen_sumWeights      = hcounters.GetBinContent(40)
        partialSampleWeight = lumi * 1000 / gen_sumWeights

    #############
    # read tree #
    #############
    print "reading tree", inputMCTTbartree.GetName(),treeText,treeDATA.GetName()  ,"..."
    
    for event in treeMCTTbar:
        if ZTree :
            if ( event.Zsel < 0 ) : continue # skip events that do not pass the trigger
        else :
            if ( event.ZZsel < 0 ) : continue # skip events that do not pass the trigger

        weight = partialSampleWeight*event.xsec*event.overallEventWeight

        if (event.ZMass < 80. or event.ZMass > 100.): continue
        if (event.LepPt[0] < 30.) : continue

        #missingHit_MC_TTbar_hist.Fill(LepMissingHit, weight)

        ##############
        # Zee histos #
        ##############
        if((int(math.fabs(event.LepLepId[0])) == 11)) :

            if event.LepPt[0] >= event.LepPt[1] :
                ele_1st_chargedHadIso_MC_TTbar_hist.Fill(event.LepChargedHadIso[0], weight)
                ele_1st_neutralHadIso_MC_TTbar_hist.Fill(event.LepNeutralHadIso[0], weight)
                ele_1st_photonIso_MC_TTbar_hist.Fill(event.LepPhotonIso[0], weight)
                ele_1st_combRelIsoPF_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[0], weight)
                if math.fabs(event.LepEta[0]) <= 1.479 :
                    ele_1st_chargedHadIso_EB_MC_TTbar_hist.Fill(event.LepChargedHadIso[0], weight)
                    ele_1st_neutralHadIso_EB_MC_TTbar_hist.Fill(event.LepNeutralHadIso[0], weight)
                    ele_1st_photonIso_EB_MC_TTbar_hist.Fill(event.LepPhotonIso[0], weight)
                    ele_1st_combRelIsoPF_EB_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[0], weight)
                else :
                    ele_1st_chargedHadIso_EE_MC_TTbar_hist.Fill(event.LepChargedHadIso[0], weight)
                    ele_1st_neutralHadIso_EE_MC_TTbar_hist.Fill(event.LepNeutralHadIso[0], weight)
                    ele_1st_photonIso_EE_MC_TTbar_hist.Fill(event.LepPhotonIso[0], weight)
                    ele_1st_combRelIsoPF_EE_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[0], weight)

            else :
                ele_1st_chargedHadIso_MC_TTbar_hist.Fill(event.LepChargedHadIso[1], weight)
                ele_1st_neutralHadIso_MC_TTbar_hist.Fill(event.LepNeutralHadIso[1], weight)
                ele_1st_photonIso_MC_TTbar_hist.Fill(event.LepPhotonIso[1], weight)
                ele_1st_combRelIsoPF_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[1], weight)
                if math.fabs(event.LepEta[0]) <= 1.479 :
                    ele_1st_chargedHadIso_EB_MC_TTbar_hist.Fill(event.LepChargedHadIso[1], weight)
                    ele_1st_neutralHadIso_EB_MC_TTbar_hist.Fill(event.LepNeutralHadIso[1], weight)
                    ele_1st_photonIso_EB_MC_TTbar_hist.Fill(event.LepPhotonIso[1], weight)
                    ele_1st_combRelIsoPF_EB_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[1], weight)
                else :
                    ele_1st_chargedHadIso_EE_MC_TTbar_hist.Fill(event.LepChargedHadIso[1], weight)
                    ele_1st_neutralHadIso_EE_MC_TTbar_hist.Fill(event.LepNeutralHadIso[1], weight)
                    ele_1st_photonIso_EE_MC_TTbar_hist.Fill(event.LepPhotonIso[1], weight)
                    ele_1st_combRelIsoPF_EE_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[1], weight)

        ################
        # Zmumu histos #
        ################
        if((int(math.fabs(event.LepLepId[0])) == 13)) :

            if event.LepPt[0] >= event.LepPt[1] :
                mu_1st_chargedHadIso_MC_TTbar_hist.Fill(event.LepChargedHadIso[0], weight)
                mu_1st_neutralHadIso_MC_TTbar_hist.Fill(event.LepNeutralHadIso[0], weight)
                mu_1st_photonIso_MC_TTbar_hist.Fill(event.LepPhotonIso[0], weight)
                mu_1st_combRelIsoPF_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[0], weight)
                if math.fabs(event.LepEta[0]) <= 1. :
                    mu_1st_chargedHadIso_MB_MC_TTbar_hist.Fill(event.LepChargedHadIso[0], weight)
                    mu_1st_neutralHadIso_MB_MC_TTbar_hist.Fill(event.LepNeutralHadIso[0], weight)
                    mu_1st_photonIso_MB_MC_TTbar_hist.Fill(event.LepPhotonIso[0], weight)
                    mu_1st_combRelIsoPF_MB_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[0], weight)
                else :
                    mu_1st_chargedHadIso_ME_MC_TTbar_hist.Fill(event.LepChargedHadIso[0], weight)
                    mu_1st_neutralHadIso_ME_MC_TTbar_hist.Fill(event.LepNeutralHadIso[0], weight)
                    mu_1st_photonIso_ME_MC_TTbar_hist.Fill(event.LepPhotonIso[0], weight)
                    mu_1st_combRelIsoPF_ME_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[0], weight)

            else :
                mu_1st_chargedHadIso_MC_TTbar_hist.Fill(event.LepChargedHadIso[1], weight)
                mu_1st_neutralHadIso_MC_TTbar_hist.Fill(event.LepNeutralHadIso[1], weight)
                mu_1st_photonIso_MC_TTbar_hist.Fill(event.LepPhotonIso[1], weight)
                mu_1st_combRelIsoPF_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[1], weight)
                if math.fabs(event.LepEta[0]) <= 1. :
                    mu_1st_chargedHadIso_MB_MC_TTbar_hist.Fill(event.LepChargedHadIso[1], weight)
                    mu_1st_neutralHadIso_MB_MC_TTbar_hist.Fill(event.LepNeutralHadIso[1], weight)
                    mu_1st_photonIso_MB_MC_TTbar_hist.Fill(event.LepPhotonIso[1], weight)
                    mu_1st_combRelIsoPF_MB_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[1], weight)
                else :
                    mu_1st_chargedHadIso_ME_MC_TTbar_hist.Fill(event.LepChargedHadIso[1], weight)
                    mu_1st_neutralHadIso_ME_MC_TTbar_hist.Fill(event.LepNeutralHadIso[1], weight)
                    mu_1st_photonIso_ME_MC_TTbar_hist.Fill(event.LepPhotonIso[1], weight)
                    mu_1st_combRelIsoPF_ME_MC_TTbar_hist.Fill(event.LepCombRelIsoPF[1], weight)


    #save histograms in a root file                                                                                                                                                                         
    print "saving MC TTbar histograms into root file ..."
    MCTTbar_outFile = TFile.Open("ControlVariablesForBDT_MCTTbar_"+ period + "_" + treeText +".root", "RECREATE")
    MCTTbar_outFile.cd()

    #missingHit_MC_TTbar_hist.Write()       
    ele_1st_chargedHadIso_MC_TTbar_hist.Write()   
    ele_1st_chargedHadIso_EB_MC_TTbar_hist.Write()  
    ele_1st_chargedHadIso_EE_MC_TTbar_hist.Write()  
    ele_1st_neutralHadIso_MC_TTbar_hist.Write()     
    ele_1st_neutralHadIso_EB_MC_TTbar_hist.Write()  
    ele_1st_neutralHadIso_EE_MC_TTbar_hist.Write()  
    ele_1st_photonIso_MC_TTbar_hist.Write()         
    ele_1st_photonIso_EB_MC_TTbar_hist.Write()      
    ele_1st_photonIso_EE_MC_TTbar_hist.Write()     
    ele_1st_combRelIsoPF_MC_TTbar_hist.Write()      
    ele_1st_combRelIsoPF_EB_MC_TTbar_hist.Write()   
    ele_1st_combRelIsoPF_EE_MC_TTbar_hist.Write()  

    mu_1st_chargedHadIso_MC_TTbar_hist.Write()   
    mu_1st_chargedHadIso_MB_MC_TTbar_hist.Write()  
    mu_1st_chargedHadIso_ME_MC_TTbar_hist.Write()  
    mu_1st_neutralHadIso_MC_TTbar_hist.Write()     
    mu_1st_neutralHadIso_MB_MC_TTbar_hist.Write()  
    mu_1st_neutralHadIso_ME_MC_TTbar_hist.Write()  
    mu_1st_photonIso_MC_TTbar_hist.Write()         
    mu_1st_photonIso_MB_MC_TTbar_hist.Write()      
    mu_1st_photonIso_ME_MC_TTbar_hist.Write()     
    mu_1st_combRelIsoPF_MC_TTbar_hist.Write()      
    mu_1st_combRelIsoPF_MB_MC_TTbar_hist.Write()   
    mu_1st_combRelIsoPF_ME_MC_TTbar_hist.Write()  

    MCTTbar_outFile.Close()
    print "MC TTbar histo file created!"


# ****************************************                                                                                           
# create output directory                                                                                                                               
# ****************************************                                                                                                              
outputDir = "ControlVariablesForBDT_DATAvsMC_" + str(period) + "_" + str(treeText)
gSystem.Exec("mkdir -p " + outputDir)
print "Output directory created!"

# **************************                                                                                                                     
# read data histos from file                                                                                                                  
# **************************                                                                                                                 
histoDATA_input = TFile.Open("ControlVariablesForBDT_DATA_"+ period + "_" + treeText +".root")
print 'Reading file', histoDATA_input.GetName(),'...'

DATA_list = []

#DATA_list.append(histoDATA_input.Get('missingHit'))
DATA_list.append(histoDATA_input.Get('1st_chargedHadIso_ele'))
DATA_list.append(histoDATA_input.Get('1st_chargedHadIso_EB_ele'))
DATA_list.append(histoDATA_input.Get('1st_chargedHadIso_EE_ele'))
DATA_list.append(histoDATA_input.Get('1st_neutralHadIso_ele'))
DATA_list.append(histoDATA_input.Get('1st_neutralHadIso_EB_ele'))
DATA_list.append(histoDATA_input.Get('1st_neutralHadIso_EE_ele'))
DATA_list.append(histoDATA_input.Get('1st_photonIso_ele'))
DATA_list.append(histoDATA_input.Get('1st_photonIso_EB_ele'))
DATA_list.append(histoDATA_input.Get('1st_photonIso_EE_ele'))
DATA_list.append(histoDATA_input.Get('1st_combRelIsoPF_ele'))
DATA_list.append(histoDATA_input.Get('1st_combRelIsoPF_EB_ele'))
DATA_list.append(histoDATA_input.Get('1st_combRelIsoPF_EE_ele'))

DATA_list.append(histoDATA_input.Get('1st_chargedHadIso_mu'))
DATA_list.append(histoDATA_input.Get('1st_chargedHadIso_MB_mu'))
DATA_list.append(histoDATA_input.Get('1st_chargedHadIso_ME_mu'))
DATA_list.append(histoDATA_input.Get('1st_neutralHadIso_mu'))
DATA_list.append(histoDATA_input.Get('1st_neutralHadIso_MB_mu'))
DATA_list.append(histoDATA_input.Get('1st_neutralHadIso_ME_mu'))
DATA_list.append(histoDATA_input.Get('1st_photonIso_mu'))
DATA_list.append(histoDATA_input.Get('1st_photonIso_MB_mu'))
DATA_list.append(histoDATA_input.Get('1st_photonIso_ME_mu'))
DATA_list.append(histoDATA_input.Get('1st_combRelIsoPF_mu'))
DATA_list.append(histoDATA_input.Get('1st_combRelIsoPF_MB_mu'))
DATA_list.append(histoDATA_input.Get('1st_combRelIsoPF_ME_mu'))


histoMCDY_input = TFile.Open("ControlVariablesForBDT_MCDY_"+ period + "_" + treeText +".root")
print 'Reading file', histoMCDY_input.GetName(),'...'

MCDY_list = []

#MCDY_list.append(histoMCDY_input.Get('missingHit_MC_DY'))
MCDY_list.append(histoMCDY_input.Get('1st_chargedHadIso_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_chargedHadIso_EB_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_chargedHadIso_EE_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_neutralHadIso_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_neutralHadIso_EB_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_neutralHadIso_EE_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_photonIso_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_photonIso_EB_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_photonIso_EE_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_combRelIsoPF_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_combRelIsoPF_EB_MC_DY_ele'))
MCDY_list.append(histoMCDY_input.Get('1st_combRelIsoPF_EE_MC_DY_ele'))

MCDY_list.append(histoMCDY_input.Get('1st_chargedHadIso_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_chargedHadIso_MB_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_chargedHadIso_ME_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_neutralHadIso_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_neutralHadIso_MB_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_neutralHadIso_ME_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_photonIso_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_photonIso_MB_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_photonIso_ME_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_combRelIsoPF_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_combRelIsoPF_MB_MC_DY_mu'))
MCDY_list.append(histoMCDY_input.Get('1st_combRelIsoPF_ME_MC_DY_mu'))


histoMCTTbar_input = TFile.Open("ControlVariablesForBDT_MCTTbar_"+ period + "_" + treeText +".root")
print 'Reading file', histoMCTTbar_input.GetName(),'...'

MCTTbar_list = []

#MCTTbar_list.append(histoMCTTbar_input.Get('missingHit_MC_TTbar'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_chargedHadIso_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_chargedHadIso_EB_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_chargedHadIso_EE_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_neutralHadIso_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_neutralHadIso_EB_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_neutralHadIso_EE_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_photonIso_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_photonIso_EB_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_photonIso_EE_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_combRelIsoPF_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_combRelIsoPF_EB_MC_TTbar_ele'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_combRelIsoPF_EE_MC_TTbar_ele'))

MCTTbar_list.append(histoMCTTbar_input.Get('1st_chargedHadIso_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_chargedHadIso_MB_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_chargedHadIso_ME_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_neutralHadIso_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_neutralHadIso_MB_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_neutralHadIso_ME_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_photonIso_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_photonIso_MB_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_photonIso_ME_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_combRelIsoPF_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_combRelIsoPF_MB_MC_TTbar_mu'))
MCTTbar_list.append(histoMCTTbar_input.Get('1st_combRelIsoPF_ME_MC_TTbar_mu'))



# ******************************
# do DATA vs MC comparison plots  
# ******************************

for i in range(len(DATA_list)) : 

    canvas = TCanvas("canvas","canvas",800,800)

    hs = THStack("hs","")

    norm = 1                                                                                 # Normalize to MC cross-section 
    #norm = DATA_list[i].Integral() / (MCTTbar_list[i].Integral() + MCDY_list[i].Integral()) # Normalize MC to data

    #DATA hist
    DATA_list[i].SetMarkerStyle(20)
    DATA_list[i].SetMarkerSize(0.6)

    #MC TTbar hist
    MCTTbar_list[i].Scale(norm) # MC normalization
    MCTTbar_list[i].SetFillColor(kAzure-3)
    MCTTbar_list[i].SetLineColor(kBlack)
    hs.Add(MCTTbar_list[i])

    #MC DY hist
    MCDY_list[i].Scale(norm) # MC normalization
    MCDY_list[i].SetFillColor(kAzure+6)
    MCDY_list[i].SetLineColor(kBlack)
    hs.Add(MCDY_list[i])

    #upper plot pad
    pad1 = TPad("pad1","pad1", 0, 0.3, 1, 1.0)
    pad1.Draw()
    pad1.cd()

    hs.SetMaximum(1.4*max(hs.GetMaximum(),DATA_list[i].GetMaximum()))
    DATA_list[i].SetMaximum(1.4*max(hs.GetMaximum(),DATA_list[i].GetMaximum()))

    hs.Draw("histo")
    DATA_list[i].Draw("sameEP")

    hs.SetTitle("")
    hs.GetXaxis().SetTitle(DATA_list[i].GetTitle())
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
    legend.AddEntry(DATA_list[i],"Data", "p")
    legend.AddEntry(MCDY_list[i],"DY MC","f")
    legend.AddEntry(MCTTbar_list[i],"t#bar{t} MC","f")
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
    rp = TH1F(DATA_list[i].Clone("rp"))
    rp.SetLineColor(kBlack)
    rp.SetMinimum(0.5)
    rp.SetMaximum(2.)
    rp.SetStats(0)
    rp.Divide(TH1F(MCDY_list[i]+MCTTbar_list[i]))   #divide histo rp/MC
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

    canvas.SaveAs(outputDir + "/" + DATA_list[i].GetTitle() + ".pdf")
    canvas.SaveAs(outputDir + "/" + DATA_list[i].GetTitle() + ".png")

print "plots done"
