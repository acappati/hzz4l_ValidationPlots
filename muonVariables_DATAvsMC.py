#!/usr/bin/env python

# ****************************
# usage: 
#    python muonVariables.py
#
# ****************************


import json
import ROOT, math, helper, CMSGraphics, CMS_lumi
from ROOT import TFile, TH1, TH1F, TCanvas, gSystem, TAttFill, TLegend, TRatioPlot, TPad, TStyle, THStack, TPaveText, gStyle
from CMSGraphics import makeCMSCanvas, makeLegend
from helper import ReadJSON
from helper import DoSimpleFit, Result
from ROOT import kBlue, kRed, kBlack, kWhite, kAzure, kOrange, kMagenta
from ROOT import TLorentzVector
ROOT.gSystem.Load('libGenVector')


# *****************************
# Declare all the variables 
# options
# *****************************                                                                                                                         
redoDATAHistos    = True
redoMCDYHistos    = True

# Data periods options                                                                                                                                        
# *****************************                                                                                                                         
period = "data2016"
#period = "data2017"                                                                                
#period = "data2018"                                                                                                                                                 
# *****************************  


# *****************************                                                                                        
# Input file
# *****************************                                                                               
if(period == "data2016"):
    inputDATAtree    = TFile.Open("/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/NEW_trainDATA_CJLSTformat.root") # 2016 Data  
    inputMCDYtree    = TFile.Open("/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/NEW_trainDY_CJLSTformat.root") # DYMC 2016
    lumi     = 35.92  # fb-1
    lumiText = '35.92 fb^{-1}'
    treeDATA    = inputDATAtree.Get("tree")
    treeMCDY    = inputMCDYtree.Get("tree")

elif(period == "data2017"):
    inputDATAtree    = TFile.Open("/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/NEW_trainDATA_CJLSTformat.root") # 2016 Data  
    inputMCDYtree    = TFile.Open("/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/NEW_trainMCDY_CJLSTformat.root") # DYMC 2016
    lumi     = 41.53   # fb-1
    lumiText = '41.53 fb^{-1}'

elif(period == "data2018"):
    inputDATAtree    = TFile.Open("/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/NEW_trainDATA_CJLSTformat.root") # 2016 Data  
    inputMCDYtree    = TFile.Open("/afs/cern.ch/work/e/elfontan/private/HZZ/RUN2_Legacy/CMSSW_10_2_15/src/ZZAnalysis/AnalysisStep/test/hzz4l_ValidationPlots/NEW_trainMCDY_CJLSTformat.root") # DYMC 2016
    lumi     = 58.83   # fb-1
    lumiText = '58.83 fb^{-1}'



# ********************
#  do DATA histos 
# ********************
if(redoDATAHistos) :

    TH1.SetDefaultSumw2() # set sumw2 = true for all the histograms created from now on

    mu_eta_lowPt_hist                   = TH1F('eta_mu_lowPt',    'eta_mu_lowPt',                                     40, -3., 3.)
    global_valid_mu_hits_lowPt_hist     = TH1F('global_valid_mu_hits_lowPt', 'global_valid_mu_hits_lowPt',           65, -5., 60.) 
    global_chi2_lowPt_hist              = TH1F('global_chi2_lowPt', 'global_chi2_lowPt',                              50, 0., 50.) 
    tracker_valid_hits_lowPt_hist       = TH1F('tracker_valid_hits_lowPt', 'tracker_valid_hits_lowPt',                40, 0., 40.) 
    tracker_valid_pixel_hits_lowPt_hist = TH1F('tracker_valid_pixel_hits_lowPt', 'tracker_valid_pixel_hits_lowPt',    12, 0., 12.) 
    mu_photonIso_lowPt_hist             = TH1F('photonIso_mu_lowPt', 'PhotonIso_mu_lowPt',                            100, 0., 4.)
    mu_chargedHadIso_lowPt_hist         = TH1F('chargedHadIso_mu_lowPt', 'ChargedHadIso_mu_lowPt',                    100, 0., 4.)
    mu_neutralHadIso_lowPt_hist         = TH1F('neutralHadIso_mu_lowPt', 'NeutralHadIso_mu_lowPt',                    100, 0., 4.)
    mu_rho_lowPt_hist                   = TH1F('rho_mu_lowPt', 'Rho_mu_lowPt',                                       100, 0., 40.)
    mu_Nvtx_lowPt_hist                  = TH1F('Nvtx_lowPt', 'Nvtx_lowPt',                                            40, 0., 40.)
    mu_sip_lowPt_hist                   = TH1F('sip_mu_lowPt', 'Sip_mu_lowPt',                                       100, 0., 10.)
    mu_dxy_lowPt_hist                   = TH1F('dxy_mu_lowPt', 'dxy_mu_lowPt',                                       100, 0., 10.)
    mu_dz_lowPt_hist                    = TH1F('dz_mu_lowPt',  'dz_mu_lowPt',                                       100, 0., 100.)

    mu_eta_highPt_hist                   = TH1F('eta_mu_highPt',    'eta_mu_highPt',                                  40, -3., 3.)
    global_valid_mu_hits_highPt_hist     = TH1F('global_valid_mu_hits_highPt', 'global_valid_mu_hits_highPt',        65, -5., 60.) 
    global_chi2_highPt_hist              = TH1F('global_chi2_highPt', 'global_chi2_highPt',                           50, 0., 50.) 
    tracker_valid_hits_highPt_hist       = TH1F('tracker_valid_hits_highPt', 'tracker_valid_hits_highPt',             40, 0., 40.) 
    tracker_valid_pixel_hits_highPt_hist = TH1F('tracker_valid_pixel_hits_highPt', 'tracker_valid_pixel_hits_highPt', 12, 0., 12.) 
    mu_photonIso_highPt_hist             = TH1F('photonIso_mu_highPt', 'PhotonIso_mu_highPt',                         100, 0., 4.)
    mu_chargedHadIso_highPt_hist         = TH1F('chargedHadIso_mu_highPt', 'ChargedHadIso_mu_highPt',                 100, 0., 4.)
    mu_neutralHadIso_highPt_hist         = TH1F('neutralHadIso_mu_highPt', 'NeutralHadIso_mu_highPt',                 100, 0., 4.)
    mu_rho_highPt_hist                   = TH1F('rho_mu_highPt', 'Rho_mu_highPt',                                    100, 0., 40.)
    mu_Nvtx_highPt_hist                  = TH1F('Nvtx_highPt', 'Nvtx_highPt',                                         40, 0., 40.)
    mu_sip_highPt_hist                   = TH1F('sip_mu_highPt', 'Sip_mu_highPt',                                    100, 0., 10.)
    mu_dxy_highPt_hist                   = TH1F('dxy_mu_highPt', 'dxy_mu_highPt',                                    100, 0., 10.)
    mu_dz_highPt_hist                    = TH1F('dz_mu_highPt',  'dz_mu_highPt',                                    100, 0., 100.)


    ##############
    # read TTree #
    ##############
    print "reading tree", inputDATAtree.GetName(), treeDATA.GetName()  ,"..."

    n_event = 0 
    for event in treeDATA:
        n_event += 1 
        if (n_event == 1000) : break
        if(n_event % int((treeDATA.GetEntries()/50)) == 0):
                print "{} %".format(str(100*n_event/treeDATA.GetEntries() + 1))

        #print "============"
        #print "Size: \t ",  event.pT_muon.size()
        tag = TLorentzVector()                                                                                                                            
        probe = TLorentzVector()                                                                                                                     
        Z = TLorentzVector()                                                                                                                                                                           
        
        #for i in range (event.pT_muon.size()):
        if (event.pT_muon.size() == 2):
            #print "CARICHE: \t ",  event.Q_muon.at(0), event.Q_muon.at(1)
            if (not (event.Q_muon.at(0) + event.Q_muon.at(1))==0): continue
            #print "PARTICELLA 0: \t ",  event.pT_muon.at(0), event.eta_muon.at(0), event.phi_muon.at(0), event.E_muon.at(0) 
            #print "PARTICELLA 1: \t ",  event.pT_muon.at(1), event.eta_muon.at(1), event.phi_muon.at(1), event.E_muon.at(1)
 
            relPFIso_0 = (event.pf_charged_had_iso.at(0) + max (0, event.pf_neutral_had_iso.at(0) + event.pf_photon_iso.at(0) - 0.5 * event.pu_charged_had_iso.at(0))) / event.pT_muon.at(0)
            relPFIso_1 = (event.pf_charged_had_iso.at(1) + max (0, event.pf_neutral_had_iso.at(1) + event.pf_photon_iso.at(1) - 0.5 * event.pu_charged_had_iso.at(1))) / event.pT_muon.at(1)

            if (event.pT_muon.at(0) > 30. and event.is_pf_muon.at(0) and event.sip_muon.at(0) < 4. and relPFIso_0 < 0.2 and event.dxy_muon.at(0) < 0.5 and event.dz_muon.at(0) < 1.):
                #print "0 TAG e 1 PROBE!"
                pb = "at1"
                tag.SetPtEtaPhiE (event.pT_muon.at(0), event.eta_muon.at(0), event.phi_muon.at(0), event.E_muon.at(0))                                                                 
                probe.SetPtEtaPhiE (event.pT_muon.at(1), event.eta_muon.at(1), event.phi_muon.at(1), event.E_muon.at(1))                                                                 
            elif (event.pT_muon.at(1) > 30. and event.is_pf_muon.at(1) and event.sip_muon.at(1) < 4. and relPFIso_1 < 0.2 and event.dxy_muon.at(1) < 0.5 and event.dz_muon.at(1) < 1.):
                #print "1 TAG e 0 PROBE!"
                pb = "at0"
                tag.SetPtEtaPhiE (event.pT_muon.at(1), event.eta_muon.at(1), event.phi_muon.at(1), event.E_muon.at(1))                                                                 
                probe.SetPtEtaPhiE (event.pT_muon.at(0), event.eta_muon.at(0), event.phi_muon.at(0), event.E_muon.at(0))                                                                 
                
            Z = tag + probe                                                                                                                                                 
            #print "Z mass is: \t", Z.M()
            if (Z.M() < 80. or Z.M() > 100.) : continue              

            if (pb == "at1"):
                if (event.dxy_muon.at(1) > 0.5 or event.dz_muon.at(1) > 1.) : continue

                if (event.pT_muon.at(1) < 10.):
                    mu_eta_lowPt_hist.Fill(event.eta_muon[1]) 
                    global_valid_mu_hits_lowPt_hist.Fill(event.global_valid_mu_hits[1])
                    global_chi2_lowPt_hist.Fill(event.global_chi2[1])
                    tracker_valid_hits_lowPt_hist.Fill(event.tracker_valid_hits[1])
                    tracker_valid_pixel_hits_lowPt_hist.Fill(event.tracker_valid_pixel_hits[1])
                    mu_photonIso_lowPt_hist.Fill(event.pf_photon_iso[1])
                    mu_chargedHadIso_lowPt_hist.Fill(event.pf_charged_had_iso[1])
                    mu_neutralHadIso_lowPt_hist.Fill(event.pf_neutral_had_iso[1])
                    mu_rho_lowPt_hist.Fill(event.rho_muon[1])
                    mu_Nvtx_lowPt_hist.Fill(event.Nvtx[1])
                    mu_sip_lowPt_hist.Fill(event.sip_muon[1])
                    mu_dxy_lowPt_hist.Fill(event.dxy_muon[1])
                    mu_dz_lowPt_hist.Fill(event.dz_muon[1])

                elif (event.pT_muon.at(1) >= 10.):
                    mu_eta_highPt_hist.Fill(event.eta_muon[1]) 
                    global_valid_mu_hits_highPt_hist.Fill(event.global_valid_mu_hits[1])
                    global_chi2_highPt_hist.Fill(event.global_chi2[1])
                    tracker_valid_hits_highPt_hist.Fill(event.tracker_valid_hits[1])
                    tracker_valid_pixel_hits_highPt_hist.Fill(event.tracker_valid_pixel_hits[1])
                    mu_photonIso_highPt_hist.Fill(event.pf_photon_iso[1])
                    mu_chargedHadIso_highPt_hist.Fill(event.pf_charged_had_iso[1])
                    mu_neutralHadIso_highPt_hist.Fill(event.pf_neutral_had_iso[1])
                    mu_rho_highPt_hist.Fill(event.rho_muon[1])
                    mu_Nvtx_highPt_hist.Fill(event.Nvtx[1])
                    mu_sip_highPt_hist.Fill(event.sip_muon[1])
                    mu_dxy_highPt_hist.Fill(event.dxy_muon[1])
                    mu_dz_highPt_hist.Fill(event.dz_muon[1])

            elif (pb == "at0"):
                if (event.dxy_muon.at(0) > 0.5 or event.dz_muon.at(0) > 1.) : continue

                if (event.pT_muon.at(0) < 10.):
                    mu_eta_lowPt_hist.Fill(event.eta_muon[0]) 
                    global_valid_mu_hits_lowPt_hist.Fill(event.global_valid_mu_hits[0])
                    global_chi2_lowPt_hist.Fill(event.global_chi2[0])
                    tracker_valid_hits_lowPt_hist.Fill(event.tracker_valid_hits[0])
                    tracker_valid_pixel_hits_lowPt_hist.Fill(event.tracker_valid_pixel_hits[0])
                    mu_photonIso_lowPt_hist.Fill(event.pf_photon_iso[0])
                    mu_chargedHadIso_lowPt_hist.Fill(event.pf_charged_had_iso[0])
                    mu_neutralHadIso_lowPt_hist.Fill(event.pf_neutral_had_iso[0])
                    mu_rho_lowPt_hist.Fill(event.rho_muon[0])
                    mu_Nvtx_lowPt_hist.Fill(event.Nvtx[0])
                    mu_sip_lowPt_hist.Fill(event.sip_muon[0])
                    mu_dxy_lowPt_hist.Fill(event.dxy_muon[0])
                    mu_dz_lowPt_hist.Fill(event.dz_muon[0])

                elif (event.pT_muon.at(0) >= 10.):
                    mu_eta_highPt_hist.Fill(event.eta_muon[0]) 
                    global_valid_mu_hits_highPt_hist.Fill(event.global_valid_mu_hits[0])
                    global_chi2_highPt_hist.Fill(event.global_chi2[0])
                    tracker_valid_hits_highPt_hist.Fill(event.tracker_valid_hits[0])
                    tracker_valid_pixel_hits_highPt_hist.Fill(event.tracker_valid_pixel_hits[0])
                    mu_photonIso_highPt_hist.Fill(event.pf_photon_iso[0])
                    mu_chargedHadIso_highPt_hist.Fill(event.pf_charged_had_iso[0])
                    mu_neutralHadIso_highPt_hist.Fill(event.pf_neutral_had_iso[0])
                    mu_rho_highPt_hist.Fill(event.rho_muon[0])
                    mu_Nvtx_highPt_hist.Fill(event.Nvtx[0])
                    mu_sip_highPt_hist.Fill(event.sip_muon[0])
                    mu_dxy_highPt_hist.Fill(event.dxy_muon[0])
                    mu_dz_highPt_hist.Fill(event.dz_muon[0])


    #save histograms in a root file 
    print "saving histograms into root file ..."
    DATA_outFile = TFile.Open("muonBDTvariables_DATA_"+ period +".root", "RECREATE")
    DATA_outFile.cd()

    mu_eta_lowPt_hist.Write()
    global_valid_mu_hits_lowPt_hist.Write()
    global_chi2_lowPt_hist.Write()
    tracker_valid_hits_lowPt_hist.Write()
    tracker_valid_pixel_hits_lowPt_hist.Write()
    mu_photonIso_lowPt_hist.Write()
    mu_chargedHadIso_lowPt_hist.Write()
    mu_neutralHadIso_lowPt_hist.Write()
    mu_rho_lowPt_hist.Write()
    mu_Nvtx_lowPt_hist.Write()
    mu_sip_lowPt_hist.Write()
    mu_dxy_lowPt_hist.Write()
    mu_dz_lowPt_hist.Write()

    mu_eta_highPt_hist.Write()
    global_valid_mu_hits_highPt_hist.Write()
    global_chi2_highPt_hist.Write()
    tracker_valid_hits_highPt_hist.Write()
    tracker_valid_pixel_hits_highPt_hist.Write()
    mu_photonIso_highPt_hist.Write()
    mu_chargedHadIso_highPt_hist.Write()
    mu_neutralHadIso_highPt_hist.Write()
    mu_rho_highPt_hist.Write()
    mu_Nvtx_highPt_hist.Write()
    mu_sip_highPt_hist.Write()
    mu_dxy_highPt_hist.Write()
    mu_dz_highPt_hist.Write()

    DATA_outFile.Close()



# ********************
#  do MC DY histos
# ********************
if(redoMCDYHistos):

    TH1.SetDefaultSumw2() # set sumw2 = true for all the histograms created from now on

    mu_eta_lowPt_DY_hist                   = TH1F('eta_mu_lowPt_DY',    'eta_mu_lowPt_DY',                                  40, -3., 3.)
    global_valid_mu_hits_lowPt_DY_hist     = TH1F('global_valid_mu_hits_lowPt_DY', 'global_valid_mu_hits_lowPt_DY',        65, -5., 60.) 
    global_chi2_lowPt_DY_hist              = TH1F('global_chi2_lowPt_DY', 'global_chi2_lowPt_DY',                           50, 0., 50.) 
    tracker_valid_hits_lowPt_DY_hist       = TH1F('tracker_valid_hits_lowPt_DY', 'tracker_valid_hits_lowPt_DY',             40, 0., 40.) 
    tracker_valid_pixel_hits_lowPt_DY_hist = TH1F('tracker_valid_pixel_hits_lowPt_DY', 'tracker_valid_pixel_hits_lowPt_DY', 12, 0., 12.) 
    mu_photonIso_lowPt_DY_hist             = TH1F('photonIso_mu_lowPt_DY', 'PhotonIso_mu_lowPt_DY',                         100, 0., 4.)
    mu_chargedHadIso_lowPt_DY_hist         = TH1F('chargedHadIso_mu_lowPt_DY', 'ChargedHadIso_mu_lowPt_DY',                 100, 0., 4.)
    mu_neutralHadIso_lowPt_DY_hist         = TH1F('neutralHadIso_mu_lowPt_DY', 'NeutralHadIso_mu_lowPt_DY',                 100, 0., 4.)
    mu_rho_lowPt_DY_hist                   = TH1F('rho_mu_lowPt_DY', 'Rho_mu_lowPt_DY',                                    100, 0., 40.)
    mu_Nvtx_lowPt_DY_hist                  = TH1F('Nvtx_lowPt_DY', 'Nvtx_lowPt_DY',                                         40, 0., 40.)
    mu_sip_lowPt_DY_hist                   = TH1F('sip_mu_lowPt_DY', 'Sip_mu_lowPt_DY',                                    100, 0., 10.)
    mu_dxy_lowPt_DY_hist                   = TH1F('dxy_mu_lowPt_DY', 'dxy_mu_lowPt_DY',                                    100, 0., 10.)
    mu_dz_lowPt_DY_hist                    = TH1F('dz_mu_lowPt_DY',  'dz_mu_lowPt_DY',                                    100, 0., 100.)

    mu_eta_highPt_DY_hist                   = TH1F('eta_mu_highPt_DY',    'eta_mu_highPt_DY',                                  40, -3., 3.)
    global_valid_mu_hits_highPt_DY_hist     = TH1F('global_valid_mu_hits_highPt_DY', 'global_valid_mu_hits_highPt_DY',        65, -5., 60.) 
    global_chi2_highPt_DY_hist              = TH1F('global_chi2_highPt_DY', 'global_chi2_highPt_DY',                           50, 0., 50.) 
    tracker_valid_hits_highPt_DY_hist       = TH1F('tracker_valid_hits_highPt_DY', 'tracker_valid_hits_highPt_DY',             40, 0., 40.) 
    tracker_valid_pixel_hits_highPt_DY_hist = TH1F('tracker_valid_pixel_hits_highPt_DY', 'tracker_valid_pixel_hits_highPt_DY', 12, 0., 12.) 
    mu_photonIso_highPt_DY_hist             = TH1F('photonIso_mu_highPt_DY', 'PhotonIso_mu_highPt_DY',                         100, 0., 4.)
    mu_chargedHadIso_highPt_DY_hist         = TH1F('chargedHadIso_mu_highPt_DY', 'ChargedHadIso_mu_highPt_DY',                 100, 0., 4.)
    mu_neutralHadIso_highPt_DY_hist         = TH1F('neutralHadIso_mu_highPt_DY', 'NeutralHadIso_mu_highPt_DY',                 100, 0., 4.)
    mu_rho_highPt_DY_hist                   = TH1F('rho_mu_highPt_DY', 'Rho_mu_highPt_DY',                                    100, 0., 40.)
    mu_Nvtx_highPt_DY_hist                  = TH1F('Nvtx_highPt_DY', 'Nvtx_highPt_DY',                                         40, 0., 40.)
    mu_sip_highPt_DY_hist                   = TH1F('sip_mu_highPt_DY', 'Sip_mu_highPt_DY',                                    100, 0., 10.)
    mu_dxy_highPt_DY_hist                   = TH1F('dxy_mu_highPt_DY', 'dxy_mu_highPt_DY',                                    100, 0., 10.)
    mu_dz_highPt_DY_hist                    = TH1F('dz_mu_highPt_DY',  'dz_mu_highPt_DY',                                    100, 0., 100.)


    # read tree 
    print "reading tree", inputMCDYtree.GetName(), treeMCDY.GetName()  ,"..."

    n_event = 0 
    for event in treeMCDY:
        n_event += 1 
        if (n_event == 1000) : break
        if(n_event % int((treeMCDY.GetEntries()/50)) == 0):
                print "{} %".format(str(100*n_event/treeMCDY.GetEntries() + 1))

        tag = TLorentzVector()                                                                                                                            
        probe = TLorentzVector()                                                                                                                     
        Z = TLorentzVector()                                                                                                                                                                           
        
        if (event.pT_muon.size() == 2):
            if (not (event.Q_muon.at(0) + event.Q_muon.at(1))==0): continue
            print "PARTICELLA 0: \t ",  event.pT_muon.at(0), event.eta_muon.at(0), event.phi_muon.at(0), event.E_muon.at(0) 
            print "PARTICELLA 1: \t ",  event.pT_muon.at(1), event.eta_muon.at(1), event.phi_muon.at(1), event.E_muon.at(1)

            relPFIso_0 = (event.pf_charged_had_iso.at(0) + max (0, event.pf_neutral_had_iso.at(0) + event.pf_photon_iso.at(0) - 0.5 * event.pu_charged_had_iso.at(0))) / event.pT_muon.at(0)
            relPFIso_1 = (event.pf_charged_had_iso.at(1) + max (0, event.pf_neutral_had_iso.at(1) + event.pf_photon_iso.at(1) - 0.5 * event.pu_charged_had_iso.at(1))) / event.pT_muon.at(1)

            if (event.pT_muon.at(0) > 30. and event.is_pf_muon.at(0) and event.sip_muon.at(0) < 4. and relPFIso_0 < 0.2 and event.dxy_muon.at(0) < 0.5 and event.dz_muon.at(0) < 1.):
                print "0 TAG e 1 PROBE!"
                pb = "at1"
                tag.SetPtEtaPhiE (event.pT_muon.at(0), event.eta_muon.at(0), event.phi_muon.at(0), event.E_muon.at(0))                                                                 
                probe.SetPtEtaPhiE (event.pT_muon.at(1), event.eta_muon.at(1), event.phi_muon.at(1), event.E_muon.at(1))                                                                 
            if (event.pT_muon.at(1) > 30. and event.is_pf_muon.at(1) and event.sip_muon.at(1) < 4. and relPFIso_1 < 0.2 and event.dxy_muon.at(1) < 0.5 and event.dz_muon.at(1) < 1.):
                print "1 TAG e 0 PROBE!"
                pb = "at0"
                tag.SetPtEtaPhiE (event.pT_muon.at(1), event.eta_muon.at(1), event.phi_muon.at(1), event.E_muon.at(1))                                                                 
                probe.SetPtEtaPhiE (event.pT_muon.at(0), event.eta_muon.at(0), event.phi_muon.at(0), event.E_muon.at(0))                                                                 
                
            Z = tag + probe                                                                                                                                                 
            if (Z.M() < 80. or Z.M() > 100.) : continue              

            if (pb == "at1"):
                if (event.dxy_muon.at(1) > 0.5 or event.dz_muon.at(1) > 1.) : continue

                if (event.pT_muon.at(1) < 10.) :
                    mu_eta_lowPt_DY_hist.Fill(event.eta_muon[1]) 
                    global_valid_mu_hits_lowPt_DY_hist.Fill(event.global_valid_mu_hits[1])
                    global_chi2_lowPt_DY_hist.Fill(event.global_chi2[1])
                    tracker_valid_hits_lowPt_DY_hist.Fill(event.tracker_valid_hits[1])
                    tracker_valid_pixel_hits_lowPt_DY_hist.Fill(event.tracker_valid_pixel_hits[1])
                    mu_photonIso_lowPt_DY_hist.Fill(event.pf_photon_iso[1])
                    mu_chargedHadIso_lowPt_DY_hist.Fill(event.pf_charged_had_iso[1])
                    mu_neutralHadIso_lowPt_DY_hist.Fill(event.pf_neutral_had_iso[1])
                    mu_rho_lowPt_DY_hist.Fill(event.rho_muon[1])
                    mu_Nvtx_lowPt_DY_hist.Fill(event.Nvtx[1])
                    mu_sip_lowPt_DY_hist.Fill(event.sip_muon[1])
                    mu_dxy_lowPt_DY_hist.Fill(event.dxy_muon[1])
                    mu_dz_lowPt_DY_hist.Fill(event.dz_muon[1])

                elif (event.pT_muon.at(1) >= 10.) :
                    mu_eta_highPt_DY_hist.Fill(event.eta_muon[1]) 
                    global_valid_mu_hits_highPt_DY_hist.Fill(event.global_valid_mu_hits[1])
                    global_chi2_highPt_DY_hist.Fill(event.global_chi2[1])
                    tracker_valid_hits_highPt_DY_hist.Fill(event.tracker_valid_hits[1])
                    tracker_valid_pixel_hits_highPt_DY_hist.Fill(event.tracker_valid_pixel_hits[1])
                    mu_photonIso_highPt_DY_hist.Fill(event.pf_photon_iso[1])
                    mu_chargedHadIso_highPt_DY_hist.Fill(event.pf_charged_had_iso[1])
                    mu_neutralHadIso_highPt_DY_hist.Fill(event.pf_neutral_had_iso[1])
                    mu_rho_highPt_DY_hist.Fill(event.rho_muon[1])
                    mu_Nvtx_highPt_DY_hist.Fill(event.Nvtx[1])
                    mu_sip_highPt_DY_hist.Fill(event.sip_muon[1])
                    mu_dxy_highPt_DY_hist.Fill(event.dxy_muon[1])
                    mu_dz_highPt_DY_hist.Fill(event.dz_muon[1])

            elif (pb == "at0"):
                if (event.dxy_muon.at(0) > 0.5 or event.dz_muon.at(0) > 1.) : continue

                if (event.pT_muon.at(0) < 10.) :
                    mu_eta_lowPt_DY_hist.Fill(event.eta_muon[0]) 
                    global_valid_mu_hits_lowPt_DY_hist.Fill(event.global_valid_mu_hits[0])
                    global_chi2_lowPt_DY_hist.Fill(event.global_chi2[0])
                    tracker_valid_hits_lowPt_DY_hist.Fill(event.tracker_valid_hits[0])
                    tracker_valid_pixel_hits_lowPt_DY_hist.Fill(event.tracker_valid_pixel_hits[0])
                    mu_photonIso_lowPt_DY_hist.Fill(event.pf_photon_iso[0])
                    mu_chargedHadIso_lowPt_DY_hist.Fill(event.pf_charged_had_iso[0])
                    mu_neutralHadIso_lowPt_DY_hist.Fill(event.pf_neutral_had_iso[0])
                    mu_rho_lowPt_DY_hist.Fill(event.rho_muon[0])
                    mu_Nvtx_lowPt_DY_hist.Fill(event.Nvtx[0])
                    mu_sip_lowPt_DY_hist.Fill(event.sip_muon[0])
                    mu_dxy_lowPt_DY_hist.Fill(event.dxy_muon[0])
                    mu_dz_lowPt_DY_hist.Fill(event.dz_muon[0])

                elif (event.pT_muon.at(0) >= 10.) :
                    mu_eta_highPt_DY_hist.Fill(event.eta_muon[0]) 
                    global_valid_mu_hits_highPt_DY_hist.Fill(event.global_valid_mu_hits[0])
                    global_chi2_highPt_DY_hist.Fill(event.global_chi2[0])
                    tracker_valid_hits_highPt_DY_hist.Fill(event.tracker_valid_hits[0])
                    tracker_valid_pixel_hits_highPt_DY_hist.Fill(event.tracker_valid_pixel_hits[0])
                    mu_photonIso_highPt_DY_hist.Fill(event.pf_photon_iso[0])
                    mu_chargedHadIso_highPt_DY_hist.Fill(event.pf_charged_had_iso[0])
                    mu_neutralHadIso_highPt_DY_hist.Fill(event.pf_neutral_had_iso[0])
                    mu_rho_highPt_DY_hist.Fill(event.rho_muon[0])
                    mu_Nvtx_highPt_DY_hist.Fill(event.Nvtx[0])
                    mu_sip_highPt_DY_hist.Fill(event.sip_muon[0])
                    mu_dxy_highPt_DY_hist.Fill(event.dxy_muon[0])
                    mu_dz_highPt_DY_hist.Fill(event.dz_muon[0])

    #save histograms in a root file 
    print "Saving DY histograms into root file ..."
    MC_DY_outFile = TFile.Open("muonBDTvariables_MC_DY_"+ period +".root", "RECREATE")
    MC_DY_outFile.cd()

    mu_eta_lowPt_DY_hist.Write()
    global_valid_mu_hits_lowPt_DY_hist.Write()
    global_chi2_lowPt_DY_hist.Write()
    tracker_valid_hits_lowPt_DY_hist.Write()
    tracker_valid_pixel_hits_lowPt_DY_hist.Write()
    mu_photonIso_lowPt_DY_hist.Write()
    mu_chargedHadIso_lowPt_DY_hist.Write()
    mu_neutralHadIso_lowPt_DY_hist.Write()
    mu_rho_lowPt_DY_hist.Write()
    mu_Nvtx_lowPt_DY_hist.Write()
    mu_sip_lowPt_DY_hist.Write()
    mu_dxy_lowPt_DY_hist.Write()
    mu_dz_lowPt_DY_hist.Write()

    mu_eta_highPt_DY_hist.Write()
    global_valid_mu_hits_highPt_DY_hist.Write()
    global_chi2_highPt_DY_hist.Write()
    tracker_valid_hits_highPt_DY_hist.Write()
    tracker_valid_pixel_hits_highPt_DY_hist.Write()
    mu_photonIso_highPt_DY_hist.Write()
    mu_chargedHadIso_highPt_DY_hist.Write()
    mu_neutralHadIso_highPt_DY_hist.Write()
    mu_rho_highPt_DY_hist.Write()
    mu_Nvtx_highPt_DY_hist.Write()
    mu_sip_highPt_DY_hist.Write()
    mu_dxy_highPt_DY_hist.Write()
    mu_dz_highPt_DY_hist.Write()

    MC_DY_outFile.Close()
    print "MC DY histo file created!"
# ********************




# ****************************************
# create output directory 
# ****************************************
outputDir = "muonBDTvariables_DATAvsMC_" + str(period)
gSystem.Exec("mkdir -p " + outputDir)
print "Output directory created!"

# **************************
# read data histos from file 
# **************************
histoDATA_input = TFile.Open("muonBDTvariables_DATA_"+ period +".root")
print 'Reading file', histoDATA_input.GetName(),'...'

DATA_list = []

DATA_list.append(histoDATA_input.Get('eta_mu_lowPt'))
DATA_list.append(histoDATA_input.Get('global_valid_mu_hits_lowPt'))
DATA_list.append(histoDATA_input.Get('global_chi2_lowPt'))
DATA_list.append(histoDATA_input.Get('tracker_valid_hits_lowPt'))
DATA_list.append(histoDATA_input.Get('tracker_valid_pixel_hits_lowPt'))
DATA_list.append(histoDATA_input.Get('photonIso_mu_lowPt'))
DATA_list.append(histoDATA_input.Get('chargedHadIso_mu_lowPt'))
DATA_list.append(histoDATA_input.Get('neutralHadIso_mu_lowPt'))
DATA_list.append(histoDATA_input.Get('rho_mu_lowPt'))
DATA_list.append(histoDATA_input.Get('Nvtx_lowPt'))
DATA_list.append(histoDATA_input.Get('sip_mu_lowPt'))
DATA_list.append(histoDATA_input.Get('dxy_mu_lowPt'))
DATA_list.append(histoDATA_input.Get('dz_mu_lowPt'))

DATA_list.append(histoDATA_input.Get('eta_mu_highPt'))
DATA_list.append(histoDATA_input.Get('global_valid_mu_hits_highPt'))
DATA_list.append(histoDATA_input.Get('global_chi2_highPt'))
DATA_list.append(histoDATA_input.Get('tracker_valid_hits_highPt'))
DATA_list.append(histoDATA_input.Get('tracker_valid_pixel_hits_highPt'))
DATA_list.append(histoDATA_input.Get('photonIso_mu_highPt'))
DATA_list.append(histoDATA_input.Get('chargedHadIso_mu_highPt'))
DATA_list.append(histoDATA_input.Get('neutralHadIso_mu_highPt'))
DATA_list.append(histoDATA_input.Get('rho_mu_highPt'))
DATA_list.append(histoDATA_input.Get('Nvtx_highPt'))
DATA_list.append(histoDATA_input.Get('sip_mu_highPt'))
DATA_list.append(histoDATA_input.Get('dxy_mu_highPt'))
DATA_list.append(histoDATA_input.Get('dz_mu_highPt'))


# ****************************
# read DY MC histos from file 
# ****************************
histoMCDY_input = TFile.Open("muonBDTvariables_MC_DY_"+ period + ".root")
print 'Reading file', histoMCDY_input.GetName(),'...'

MCDY_list = []

MCDY_list.append(histoMCDY_input.Get('eta_mu_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('global_valid_mu_hits_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('global_chi2_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('tracker_valid_hits_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('tracker_valid_pixel_hits_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('photonIso_mu_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('chargedHadIso_mu_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('neutralHadIso_mu_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('rho_mu_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('Nvtx_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('sip_mu_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('dxy_mu_lowPt_DY'))
MCDY_list.append(histoMCDY_input.Get('dz_mu_lowPt_DY'))

MCDY_list.append(histoMCDY_input.Get('eta_mu_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('global_valid_mu_hits_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('global_chi2_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('tracker_valid_hits_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('tracker_valid_pixel_hits_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('photonIso_mu_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('chargedHadIso_mu_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('neutralHadIso_mu_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('rho_mu_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('Nvtx_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('sip_mu_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('dxy_mu_highPt_DY'))
MCDY_list.append(histoMCDY_input.Get('dz_mu_highPt_DY'))



# ******************************
# do DATA vs MC comparison plots  
# ******************************

x_axis_list = ["#eta", "Global valid #mu hits", "Global chi2", "Tracker valid hits", "Tracker valid pixel hits", "Photon iso", "Charged hadron iso", "Neutral hadron iso", "Rho", "Nvtx", "SIP", "dxy", "dz", "#eta", "Global valid #mu hits", "Global chi2", "Tracker valid hits", "Tracker valid pixel hits", "Photon iso", "Charged hadron iso", "Neutral hadron iso", "Rho", "Nvtx", "SIP", "dxy", "dz"] 

for i in range(len(DATA_list)) : 

    canvas = TCanvas ("canvas", "canvas", 800, 800)

    hs = THStack("hs","")

    #norm = 1                                                  # Normalize to MC cross-section 
    norm = DATA_list[i].Integral() / MCDY_list[i].Integral() # Normalize MC to data

    #DATA hist
    DATA_list[i].SetMarkerStyle(20)
    DATA_list[i].SetMarkerSize(0.6)
    #DATA_list[i].Rebin(4)

    #MC DY hist
    MCDY_list[i].Scale(norm) # MC normalization
    MCDY_list[i].SetFillColor(kAzure-3)
    MCDY_list[i].SetLineColor(kBlack)
    #MCDY_list[i].Rebin(4)
    hs.Add(MCDY_list[i])

    #upper plot pad
    pad1 = TPad("pad1","pad1", 0, 0.3, 1, 1.0)
    pad1.Draw()
    pad1.cd()

    hs.SetMaximum(1.6*max(hs.GetMaximum(), DATA_list[i].GetMaximum()))
    DATA_list[i].SetMaximum(1.6*max(hs.GetMaximum(), DATA_list[i].GetMaximum()))
    hs.SetMinimum(10) #EF for ele BDT

    hs.Draw("histo")
    DATA_list[i].Draw("sameEP")

    hs.SetTitle("")
    hs.GetXaxis().SetTitle(x_axis_list[i])
    hs.GetXaxis().SetLabelFont(43)
    hs.GetXaxis().SetLabelSize(15)
    hs.GetYaxis().SetTitleSize(20)
    hs.GetYaxis().SetTitleFont(43)
    hs.GetYaxis().SetTitleOffset(1.2)
    hs.GetYaxis().SetLabelFont(43)
    hs.GetYaxis().SetLabelSize(15)
    hs.GetYaxis().SetTitle("Events")

    gStyle.SetOptStat(0)
    pad1.SetLogy()

    # legend
    legend = TLegend(0.7,0.75,0.9,0.9) #left alignment
    #legend = TLegend(0.7,0.75,0.9,0.9) #right alignment
    legend.AddEntry(DATA_list[i],"Data", "p")
    legend.AddEntry(MCDY_list[i],"DY MC","f")
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
    rp.Divide(TH1F(MCDY_list[i]))   #divide histo rp/MC
    rp.SetMarkerStyle(24)
    rp.SetTitle("") 
    
    rp.SetYTitle("Data/MC")
    rp.GetYaxis().SetNdivisions(505)
    rp.GetYaxis().SetTitleSize(20)
    rp.GetYaxis().SetTitleFont(43)
    rp.GetYaxis().SetTitleOffset(1.55)
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
    CMS_lumi.CMS_lumi(pad1, 0, 0)
    
    
    canvas.Update()


    canvas.SaveAs(outputDir + "/" + DATA_list[i].GetTitle() + ".pdf")
    canvas.SaveAs(outputDir + "/" + DATA_list[i].GetTitle() + ".png")

print "plots done"
