#!/usr/bin/env python

import math
import ROOT
from ROOT import *


# open input file
inputDataFile = ROOT.TFile("fitsip_mu.root")
inputDataFile.cd()

#define and take input ttree
tData = inputDataFile.Get("T")


#define variable of interest
sip1 = RooRealVar("sip1","sip1",0,40)

#define pdf
ml = RooRealVar("mean","mean landau Zjet MC",0.6,0.,10.)
sl = RooRealVar("sigma","sigma landau1 Zjet MC", 0.2,0.1,10.)

landau = RooLandau("landau","landau Zjet MC",sip1,ml,sl)


#define dataset
tdata = RooDataSet("tdata","tdata",RooArgSet(sip1),RooFit.Import(tData))


#define range
sip1.setRange("range0-2",0,2)


#do the fit 
landau.fitTo(tdata,RooFit.Range("range0-2"))


#define frame 
xframe = sip1.frame(0.,10.)
tdata.plotOn(xframe)
landau.plotOn(xframe, RooFit.NormRange("range0-2"))


#do the plot
c = TCanvas("landau_fit","landau_fit")
c.cd()
xframe.Draw()
c.SaveAs("landau_fit.png")
  
