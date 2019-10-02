#define createNewRootfileDY_cxx
#include "createNewRootfileDY.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void createNewRootfileDY::Loop()
{
  TString infilename  = "/eos/user/m/mkovac/Data/Muons/DY_2016_10_9_2019/train.root";
  TString outfilename = "trainDY_CJLSTformat.root";

  TFile *f_in = TFile::Open(infilename, "READ");
  std::cout << "Opening and processing file \t" << infilename << std::endl;

  TTree *DYtree = (TTree*)f_in->Get("ntuplizer/tree");

  TFile * outfile = new TFile ( outfilename, "RECREATE" );
  TTree * tree    = new TTree ( "tree", "Muon pairs for T&P" );
  
  // Declaration of branch types                                               
  std::vector<Int_t>   Event;                                                                                         
  std::vector<Int_t>   Run;                                                                                 
  std::vector<Float_t> Q_muon;                                                                      
  std::vector<Float_t> pT_muon;                                                                              
  std::vector<Float_t> eta_muon;                                                                                                            
  std::vector<Float_t> phi_muon;                                                                        
  std::vector<Float_t> E_muon;                                                                                                                   
  std::vector<Float_t> rho_muon;                                                                                                                   
  //std::vector<Float_t> NgenPU;                                                                                                                   
  std::vector<Float_t> Nvtx;                                                                                                                   
  std::vector<Bool_t>  is_global_muon;                                          
  std::vector<Bool_t>  is_tracker_muon;                                                                           
  std::vector<Bool_t>  is_pf_muon;                                                                               
  std::vector<Int_t>   tracker_valid_hits;                                                                                                     
  std::vector<Int_t>   tracker_valid_pixel_hits;                 
  std::vector<Int_t>   global_valid_mu_hits;                                                              
  std::vector<Int_t>   global_chi2;                                                                       
  std::vector<Float_t> sip_muon;                                                                       
  std::vector<Float_t> dxy_muon;                                                    
  std::vector<Float_t> dz_muon;                                                                         
  std::vector<Float_t> pf_charged_had_iso;                                                                     
  std::vector<Float_t> pf_neutral_had_iso;                                                       
  std::vector<Float_t> pf_photon_iso;                                            
  std::vector<Float_t> pu_charged_had_iso;                                                                           
                                              
  tree -> Branch ("Event", &Event);                                                              
  tree -> Branch ("Run", &Run);                                                                            
  tree -> Branch ("Q_muon", &Q_muon);                                                           
  tree -> Branch ("pT_muon", &pT_muon);                                            
  tree -> Branch ("eta_muon", &eta_muon);                                                           
  tree -> Branch ("phi_muon", &phi_muon);                                                                 
  tree -> Branch ("E_muon", &E_muon);                                                                      
  tree -> Branch ("rho_muon", &rho_muon);                                                         
  //tree -> Branch ("NgenPU", &NgenPU);                                                         
  tree -> Branch ("Nvtx", &Nvtx);                                                         
  tree -> Branch ("is_global_muon", &is_global_muon);                                                
  tree -> Branch ("is_tracker_muon", &is_tracker_muon);                                                                                      
  tree -> Branch ("is_pf_muon", &is_pf_muon);                                                                                       
  tree -> Branch ("tracker_valid_hits", &tracker_valid_hits);                                                                           
  tree -> Branch ("tracker_valid_pixel_hits", &tracker_valid_pixel_hits);                                                                          
  tree -> Branch ("global_valid_mu_hits", &global_valid_mu_hits);                                      
  tree -> Branch ("global_chi2", &global_chi2);                                                       
  tree -> Branch ("sip_muon", &sip_muon);                                
  tree -> Branch ("dxy_muon", &dxy_muon);                                                                                 
  tree -> Branch ("dz_muon", &dz_muon);                                                                                                            
  tree -> Branch ("pf_charged_had_iso", &pf_charged_had_iso);                                                                            
  tree -> Branch ("pf_neutral_had_iso", &pf_neutral_had_iso);
  tree -> Branch ("pf_photon_iso", &pf_photon_iso);									    
  tree -> Branch ("pu_charged_had_iso", &pu_charged_had_iso);                                        



  if (fChain == 0) return;
  Long64_t nentries = fChain->GetEntriesFast();
  std::cout << "Number of entries in Data tree " << nentries << "\n";
  Long64_t nbytes = 0, nb = 0;
  
  Int_t ev = 0;
  
  for (Long64_t jentry=0; jentry<nentries;jentry++) 
    {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      if  ((jentry % 100000) == 0) std::cout << "Event " << jentry << '\n';

      if (nEvent == ev)
	{
	  Event.push_back(nEvent);
	  Run.push_back(nRun);
	  Q_muon.push_back(mu_Q);
	  pT_muon.push_back(mu_pT);
	  eta_muon.push_back(mu_eta);
	  phi_muon.push_back(mu_phi);
	  E_muon.push_back(mu_E);
	  rho_muon.push_back(mu_rho);
	  //NgenPU.push_back(genNpu);
	  Nvtx.push_back(vtxN);
	  is_global_muon.push_back(is_global_mu);
	  is_tracker_muon.push_back(is_tracker_mu);
	  is_pf_muon.push_back(is_pf_mu);
	  tracker_valid_hits.push_back(tk_valid_hits);
	  tracker_valid_pixel_hits.push_back(tk_valid_pixel_hits);
	  global_valid_mu_hits.push_back(glb_valid_mu_hits);
	  global_chi2.push_back(glb_chi2);
	  sip_muon.push_back(mu_sip);
	  dxy_muon.push_back(mu_dxy);
	  dz_muon.push_back(mu_dz);
	  pf_charged_had_iso.push_back(mu_pf_charged_had_iso);
	  pf_neutral_had_iso.push_back(mu_pf_neutral_had_iso);
	  pf_photon_iso.push_back(mu_pf_photon_iso);
	  pu_charged_had_iso.push_back(mu_pu_charged_had_iso);
	  ev = nEvent;
	 }

       else if (nEvent != ev)
	 {
           if (Event.size() >= 2)
             {
               tree->Fill();
               //std::cout << "\t FILLED\n";                                                                                                             
             }
	   Event.clear();
	   Run.clear();
	   Q_muon.clear();
	   pT_muon.clear();
	   eta_muon.clear();
	   phi_muon.clear();
	   E_muon.clear();
	   rho_muon.clear();
	   //NgenPU.clear();
	   Nvtx.clear();
	   is_global_muon.clear();
	   is_tracker_muon.clear();
	   is_pf_muon.clear();
	   tracker_valid_hits.clear();
	   tracker_valid_pixel_hits.clear();
	   global_valid_mu_hits.clear();
	   global_chi2.clear();
	   sip_muon.clear();
	   dxy_muon.clear();
	   dz_muon.clear();
	   pf_charged_had_iso.clear();
	   pf_neutral_had_iso.clear();
	   pf_photon_iso.clear();
	   pu_charged_had_iso.clear();

	   Event.push_back(nEvent);
	   Run.push_back(nRun);
	   Q_muon.push_back(mu_Q);
	   pT_muon.push_back(mu_pT);
	   eta_muon.push_back(mu_eta);
	   phi_muon.push_back(mu_phi);
	   E_muon.push_back(mu_E);
	   rho_muon.push_back(mu_rho);
	   //NgenPU.push_back(genNpu);
	   Nvtx.push_back(vtxN);
	   is_global_muon.push_back(is_global_mu);
	   is_tracker_muon.push_back(is_tracker_mu);
	   is_pf_muon.push_back(is_pf_mu);
	   tracker_valid_hits.push_back(tk_valid_hits);
	   tracker_valid_pixel_hits.push_back(tk_valid_pixel_hits);
	   global_valid_mu_hits.push_back(glb_valid_mu_hits);
	   global_chi2.push_back(glb_chi2);
	   sip_muon.push_back(mu_sip);
	   dxy_muon.push_back(mu_dxy);
	   dz_muon.push_back(mu_dz);
	   pf_charged_had_iso.push_back(mu_pf_charged_had_iso);
	   pf_neutral_had_iso.push_back(mu_pf_neutral_had_iso);
	   pf_photon_iso.push_back(mu_pf_photon_iso);
	   pu_charged_had_iso.push_back(mu_pu_charged_had_iso);
	   
	   ev = nEvent;
	 }
     }

tree->Write();                                                                                                                              
tree->Print();                                                                                                                            
                                                                                                                                                                      
delete tree;                                                                                                                                              
outfile->Write();                                                                                                                                     
outfile->Close();                                                                                                                    
delete outfile;                                                 
}
