////////////////////////////////////////////////////////////////////////////////////////
// This class has been automatically generated on
// Sun Sep 22 15:04:45 2019 by ROOT version 6.12/07
// from TTree tree/tree
// found on file: /eos/user/m/mkovac/Data/Muons/SingleMuon_2016_10_9_2019/train.root
///////////////////////////////////////////////////////////////////////////////////////

#ifndef createNewRootfileDATA_h
#define createNewRootfileDATA_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class createNewRootfileDATA {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           nEvent;
   Int_t           nRun;
   Int_t           nLumi;
   Int_t           n_muons;
   Int_t           vtxN;
   Double_t        mu_Q;
   Double_t        mu_pT;
   Double_t        mu_eta;
   Double_t        mu_phi;
   Double_t        mu_E;
   Bool_t          is_global_mu;
   Bool_t          is_tracker_mu;
   Bool_t          is_pf_mu;
   Int_t           n_matched_stations;
   Int_t           tk_valid_hits;
   Int_t           tk_valid_pixel_hits;
   Int_t           tk_tracker_lay;
   Int_t           tk_pixel_lay;
   Double_t        tk_chi2;
   Double_t        tk_pT_error;
   Int_t           glb_valid_mu_hits;
   Double_t        glb_chi2;
   Double_t        glb_pT_error;
   Double_t        mu_ip;
   Double_t        mu_ip_error;
   Double_t        mu_sip;
   Double_t        mu_dxy;
   Double_t        mu_dz;
   Double_t        mu_pf_charged_had_iso;
   Double_t        mu_pf_neutral_had_iso;
   Double_t        mu_pf_photon_iso;
   Double_t        mu_pu_charged_had_iso;
   Double_t        mu_rho;
   Double_t        mu_dR;
   Float_t         MVA_score;

   // List of branches
   TBranch        *b_nEvent;   //!
   TBranch        *b_nRun;   //!
   TBranch        *b_nLumi;   //!
   TBranch        *b_n_muons;   //!
   TBranch        *b_vtxN;   //!
   TBranch        *b_mu_Q;   //!
   TBranch        *b_mu_pT;   //!
   TBranch        *b_mu_eta;   //!
   TBranch        *b_mu_phi;   //!
   TBranch        *b_mu_E;   //!
   TBranch        *b_is_global_mu;   //!
   TBranch        *b_is_tracker_mu;   //!
   TBranch        *b_is_pf_mu;   //!
   TBranch        *b_n_matched_stations;   //!
   TBranch        *b_tk_valid_hits;   //!
   TBranch        *b_tk_valid_pixel_hits;   //!
   TBranch        *b_tk_tracker_lay;   //!
   TBranch        *b_tk_pixel_lay;   //!
   TBranch        *b_tk_chi2;   //!
   TBranch        *b_tk_pT_error;   //!
   TBranch        *b_glb_valid_mu_hits;   //!
   TBranch        *b_glb_chi2;   //!
   TBranch        *b_glb_pT_error;   //!
   TBranch        *b_mu_ip;   //!
   TBranch        *b_mu_ip_error;   //!
   TBranch        *b_mu_sip;   //!
   TBranch        *b_mu_dxy;   //!
   TBranch        *b_mu_dz;   //!
   TBranch        *b_mu_pf_charged_had_iso;   //!
   TBranch        *b_mu_pf_neutral_had_iso;   //!
   TBranch        *b_mu_pf_photon_iso;   //!
   TBranch        *b_mu_pu_charged_had_iso;   //!
   TBranch        *b_mu_rho;   //!
   TBranch        *b_mu_dR;   //!
   TBranch        *b_MVA_score;   //!

   createNewRootfileDATA(TTree *tree=0);
   virtual ~createNewRootfileDATA();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef createNewRootfileDATA_cxx
createNewRootfileDATA::createNewRootfileDATA(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/eos/user/m/mkovac/Data/Muons/SingleMuon_2016_10_9_2019/train.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/eos/user/m/mkovac/Data/Muons/SingleMuon_2016_10_9_2019/train.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("/eos/user/m/mkovac/Data/Muons/SingleMuon_2016_10_9_2019/train.root:/ntuplizer");
      dir->GetObject("tree",tree);

   }
   Init(tree);
}

createNewRootfileDATA::~createNewRootfileDATA()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t createNewRootfileDATA::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t createNewRootfileDATA::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void createNewRootfileDATA::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("nEvent", &nEvent, &b_nEvent);
   fChain->SetBranchAddress("nRun", &nRun, &b_nRun);
   fChain->SetBranchAddress("nLumi", &nLumi, &b_nLumi);
   fChain->SetBranchAddress("n_muons", &n_muons, &b_n_muons);
   fChain->SetBranchAddress("vtxN", &vtxN, &b_vtxN);
   fChain->SetBranchAddress("mu_Q", &mu_Q, &b_mu_Q);
   fChain->SetBranchAddress("mu_pT", &mu_pT, &b_mu_pT);
   fChain->SetBranchAddress("mu_eta", &mu_eta, &b_mu_eta);
   fChain->SetBranchAddress("mu_phi", &mu_phi, &b_mu_phi);
   fChain->SetBranchAddress("mu_E", &mu_E, &b_mu_E);
   fChain->SetBranchAddress("is_global_mu", &is_global_mu, &b_is_global_mu);
   fChain->SetBranchAddress("is_tracker_mu", &is_tracker_mu, &b_is_tracker_mu);
   fChain->SetBranchAddress("is_pf_mu", &is_pf_mu, &b_is_pf_mu);
   fChain->SetBranchAddress("n_matched_stations", &n_matched_stations, &b_n_matched_stations);
   fChain->SetBranchAddress("tk_valid_hits", &tk_valid_hits, &b_tk_valid_hits);
   fChain->SetBranchAddress("tk_valid_pixel_hits", &tk_valid_pixel_hits, &b_tk_valid_pixel_hits);
   fChain->SetBranchAddress("tk_tracker_lay", &tk_tracker_lay, &b_tk_tracker_lay);
   fChain->SetBranchAddress("tk_pixel_lay", &tk_pixel_lay, &b_tk_pixel_lay);
   fChain->SetBranchAddress("tk_chi2", &tk_chi2, &b_tk_chi2);
   fChain->SetBranchAddress("tk_pT_error", &tk_pT_error, &b_tk_pT_error);
   fChain->SetBranchAddress("glb_valid_mu_hits", &glb_valid_mu_hits, &b_glb_valid_mu_hits);
   fChain->SetBranchAddress("glb_chi2", &glb_chi2, &b_glb_chi2);
   fChain->SetBranchAddress("glb_pT_error", &glb_pT_error, &b_glb_pT_error);
   fChain->SetBranchAddress("mu_ip", &mu_ip, &b_mu_ip);
   fChain->SetBranchAddress("mu_ip_error", &mu_ip_error, &b_mu_ip_error);
   fChain->SetBranchAddress("mu_sip", &mu_sip, &b_mu_sip);
   fChain->SetBranchAddress("mu_dxy", &mu_dxy, &b_mu_dxy);
   fChain->SetBranchAddress("mu_dz", &mu_dz, &b_mu_dz);
   fChain->SetBranchAddress("mu_pf_charged_had_iso", &mu_pf_charged_had_iso, &b_mu_pf_charged_had_iso);
   fChain->SetBranchAddress("mu_pf_neutral_had_iso", &mu_pf_neutral_had_iso, &b_mu_pf_neutral_had_iso);
   fChain->SetBranchAddress("mu_pf_photon_iso", &mu_pf_photon_iso, &b_mu_pf_photon_iso);
   fChain->SetBranchAddress("mu_pu_charged_had_iso", &mu_pu_charged_had_iso, &b_mu_pu_charged_had_iso);
   fChain->SetBranchAddress("mu_rho", &mu_rho, &b_mu_rho);
   fChain->SetBranchAddress("mu_dR", &mu_dR, &b_mu_dR);
   fChain->SetBranchAddress("MVA_score", &MVA_score, &b_MVA_score);
   Notify();
}

Bool_t createNewRootfileDATA::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void createNewRootfileDATA::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t createNewRootfileDATA::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef createNewRootfileDATA_cxx
