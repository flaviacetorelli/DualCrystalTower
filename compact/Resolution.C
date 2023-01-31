#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TBranch.h"
#include "TBrowser.h"
#include "TH2.h"
#include "TRandom.h"
#include "DD4hep/Printout.h"
#include "DD4hep/Objects.h"
#include "DD4hep/Factories.h"
#include "DDG4/Geant4Particle.h"
#include "DDG4/Geant4Data.h"
#include "../src/DualCrystalCalorimeterHit.h"

#include <vector>
#include <algorithm>

// way too slow if track all photons for now
// so randomly delete photons after creation according to this fraction
// keep 1 photon out of 1000
// const double supressRandom=0.001;


// information about hit channel IT numbers
const int nchan = 4;
const int ichan[nchan] = {64,73,74,75};  // channel 74 is the crystal, 73 and 75 the two kill media
std::string namechan[nchan] = {"air","PD1","crystal","PD2"};


void Resolution(int num_evtsmax, const char* inputfilename, float beamE, const char* outputfilename ) {


  typedef std::vector<dd4hep::sim::Geant4Particle*> GenParts;
  typedef std::vector<CalVision::DualCrystalCalorimeterHit*> CalHits;

  // read in libraries that define the classes
  Long_t result;
  char text[1024];
  const char* dd4hep = gSystem->Getenv("DD4hepINSTALL");
  snprintf(text,sizeof(text)," -I%s/include -D__DD4HEP_DDEVE_EXCLUSIVE__ -Wno-shadow -g -O0",dd4hep);
  gSystem->AddIncludePath(text);
  TString fname = "libDDG4IO";
  const char* io_lib = gSystem->FindDynamicLibrary(fname,kTRUE);
  result = gSystem->Load("libDDG4IO");
  result = gSystem->Load("libDDEvePlugins");
  result = gSystem->Load("libDDEvePlugins");
  result = gSystem->Load("libDualCrystalTower");
  result = gSystem->Load("libDDG4Plugins");

  // define histograms
  //gen particles
  TH1F *hgenPsize = new TH1F("hgenPsize","number of generator particles",600,0.,40000);
  TH1F *hgenPdgID = new TH1F("hgenpdgID","pdgID of generator particles",600,-200,200);


  // calorimeter infor
  TH1F *hchan = new TH1F("hchan","channel ID number",1028,0.,1028);
  TH1F *hcEcalE = new TH1F("hcEcalE","sum crystal ecal energy",100,0.,100.);
  TH1F *hcEcalncer = new TH1F("hcEcalncer","total number of cerenkov",100,0.,10000);
  TH1F *hcEcalncer0 = new TH1F("hcEcalncer0","total number of cerenkov chan 0",100,0.,10000);
  TH1F *hcEcalncer1 = new TH1F("hcEcalncer1","total number of cerenkov chan 1",100,0.,10000);
  TH1F *hcEcalncer2 = new TH1F("hcEcalncer2","total number of cerenkov chan 2",100,0.,10000);
  TH1F *hcEcalncer3 = new TH1F("hcEcalncer3","total number of cerenkov chan 3",100,0.,10000);

  TH1F *hcEcalE0 = new TH1F("hcEcalE0","energy chan 0",100,0.,10000);
  TH1F *hcEcalE1 = new TH1F("hcEcalE1","energy chan 1",100,0.,10000);
  TH1F *hcEcalE2 = new TH1F("hcEcalE2","energy chan 2",100,0.,10000);
  TH1F *hcEcalE3 = new TH1F("hcEcalE3","energy chan 3",100,0.,10000);

  TH1F *wave_cherenk  = new TH1F("wave_cherenk ","wave of cherenkov",100,0.,1000);
  TH1F *wave_scintil  = new TH1F("wave_scintil ","wave of scinittilation",100,0.,1000);

  TH1F *heest = new TH1F("heest","ratio estimated to true energy",1000,0.0,3.0);
  TH1F *heest_meass = new TH1F("heest_meass","ratio to true energy using Cherenkov+Scintillation",1000,0.0,1000.0);
  TH1F *heest_scint = new TH1F("heest_scint","ratio to true energy using Scintillation (e- for calibration)",1000,0.0,10.0);
  TH1F *heest_cherenk = new TH1F("heest_cherenk","ratio to true energy using Cherenkov (e- for calibration)",1000,0.0,10.0);

  // max value for multiplicity
  float maxCherenkov=5000000.;
  float maxScintil=5000000.;

  TH2F *depos_scintil = new TH2F("depos_scintil","NScintilation vs Depos", 1000,0.,100., 1000, 0.0, maxScintil);
  TH2F *depos_cherenk = new TH2F("depos_cherenk","Cherenkov vs Depos",     1000,0.,100., 1000, 0.0,  maxCherenkov);
  TH2F *schint_cherenk = new TH2F("schint_cherenk","Scintil vs Cherenkov", 1000,0., maxScintil, 1000, 0.0, maxCherenkov);

  // after calibration
  TH2F *schint_cherenk_calib = new TH2F("schint_cherenk_calib","Scintil vs Cherenkov (e- calibrated)", 3000,0.,30000., 3000, 0.0, 30000.0);
  TH2F *schint_cherenk_calib_rel = new TH2F("schint_cherenk_calib_rel","Scintil vs Cherenkov (e- calibrated, normalized)", 3000,0.,1.2, 3000, 0.0, 1.2);

  TH1F *scintilVsdepos = new TH1F("scintilPerMeV","L: N of scintillation per MeV",1000,0., 1000);
  TH1F *cherenkVsdepos = new TH1F("cherenkPerMeV","L: N of cherenkov per MeV",1000,0., 1000);
  TH1F *scintil_cherenkVsdepos = new TH1F("scintil_cherenkPerMeV","N of cherenkov per MeV",1000,0., 1000);

  TH1F *scintil= new TH1F("scintil","N of scintillation",50000,0., maxScintil);
  TH1F *cherenk= new TH1F("cherenk","N of cherenkov",50000,0., maxCherenkov);
  TH1F *scintil_cherenk= new TH1F("scintil_cherenk","Combined  scintillation and cherenkov",50000,0., maxCherenkov+maxScintil);
  TH1F *cherenkDIVscintil= new TH1F("cherenkDIVscintil","Nr of cherenkov / scintillation",100, 0., 2.0);


  // open data and output file for histograms

  //  const char* inputfilename="/data/users/eno/dd4hep/DD4hep/DDDetectors/compact/testSid.root";
  // const char* outputfilename="hist.root";

  // get Tree
  //  TFile *f = new TFile(inputfilename);
  //f->Print();
  GenParts* pgenparts = new GenParts();
  CalHits* pcalhits = new CalHits();
  int num_evt,nbyte;

  TFile* f = TFile::Open(inputfilename);
  TTree* t = (TTree*)f->Get("EVENT;1");
  t->Print();



  
  // loop over events
  TBranch* b_mc = t->GetBranch("MCParticles");
  TBranch* b_ecal = t->GetBranch("DRCNoSegment");
  int ihaha = b_mc->GetEntries();
  num_evt= std::min(ihaha,num_evtsmax);
  std::cout<<" doing "<<b_mc->GetName()<<std::endl;
  std::cout<<"num_evt gen loop is "<<num_evt<<std::endl;
  
  
  if(num_evt>0) {


    // find branches
    GenParts* gens = new GenParts();
    b_mc->SetAddress(&gens);
    CalHits* ecalhits = new CalHits();
    b_ecal->SetAddress(&ecalhits);


    int SCEPRINT2=10;
    for(int ievt=0;ievt<num_evt; ++ievt) {
      std::cout<<std::endl<<std::endl<<"event number is "<<ievt<<std::endl;


      // gen particles
      nbyte = b_mc->GetEntry(ievt);
      if( nbyte>0) {
	if(ievt<SCEPRINT2) std::cout<<gens->size()<<" Gen particles "<<std::endl;
      }
      hgenPsize->Fill(gens->size());
      for(size_t i=0;i<gens->size(); ++i) {
        dd4hep::sim::Geant4Particle* agen =gens->at(i);
        hgenPdgID->Fill(agen->pdgID);
      }



    // ECAL hits  
    // there are hits in the crystal and also the photodetectors "kill media"
    // in the crystal, photons created in the crystal are counted and their wavelengths stored
    // in the photodetector, photons that enter are counted, wavelength stored, and then they are killed


      int nbyte = b_ecal->GetEntry(ievt);
      if( nbyte>0) {
        if(ievt<SCEPRINT2) std::cout<<ecalhits->size()<<" Ecal Hits "<<std::endl;
      }
      float esum=0.;
      float esumchan[nchan]={0.,0.,0.,0.};
      int ncerchan[nchan]={0,0,0,0};
      int nscintchan[nchan]={0,0,0,0};
      int ncertot=0;
      int nscinttot=0;
      int SCEPRINT=10;
      for(size_t i=0;i<ecalhits->size(); ++i) {
	CalVision::DualCrystalCalorimeterHit* aecalhit =ecalhits->at(i);
	//	std::cout<<"       "<<i<<" energy "<<aecalhit->energyDeposit<<std::endl;
	esum+=aecalhit->energyDeposit;
	ncertot+=aecalhit->ncerenkov;
	nscinttot+=aecalhit->nscintillator;
	if(i<SCEPRINT&&ievt<SCEPRINT2) std::cout<<" hit channel is "<<aecalhit->cellID<<" in hex is "<< std::hex<< aecalhit->cellID<<std::dec<<" "<<aecalhit->energyDeposit<<" "<<aecalhit->ncerenkov<<" "<<aecalhit->nscintillator<<std::endl;


	// see ../src/DRCrystal_geo.cpp to see the assignments
	//int ihitchan=aecalhit->cellID;
	//int idet = (ihitchan & 0xC0)>>6;  // this assignment is made in SCEPCALConstants.xml
	//int ilayer = (ihitchan & 0x38)>>3; // this is 1 for crystal and detectors, 0 for air around it
	//int islice = (ihitchan & 0x07);  //   this is 1 or 4 for photodetectors, 2 for crystal

        int ihitchan=aecalhit->cellID;
        int idet = (ihitchan) & 0x07;
        int ix = (ihitchan >>3) & 0x1F ;  // is this right?
        if(ix>16) ix=ix-32;
        int iy =(ihitchan >>8) & 0x1F ; // is this right?
        if(iy>16) iy=iy-32;
        int  islice = (ihitchan >>13) & 0x07;
        int  ilayer = (ihitchan>> 16) & 0x07;


	// channels are 64 air
	//             73 75 detectors
	//            74 crystal
	if(i<SCEPRINT&&ievt<SCEPRINT2) std::cout<<" idet,ilayer,islice is ("<<idet<<","<<ilayer<<","<<islice<<")"<<std::endl;

        //std::cout<<" idet,ilayer,islice is ("<<idet<<","<<ilayer<<","<<islice<<")"<<std::endl;


	// print out wavelength spectra
	int ijchan=aecalhit->nbin;
        int bmin = aecalhit->wavelenmin;
        int bmax = aecalhit->wavelenmax;
        float binsize=(bmax-bmin)/float(ijchan); 
 
	for (int j=0;j<ijchan;j++) {
	 //std::cout<<"  ncerwave["<<j<<"]="<<(aecalhit->ncerwave)[j]<<std::endl;
	 //std::cout<<"  nscintwave["<<j<<"]="<<(aecalhit->nscintwave)[j]<<std::endl;
         // let's unpack
         // ibin = (wavelength-hit->wavelenmin)/binsize;
         float xw= (j*binsize)+bmin; 
         wave_scintil->Fill(xw,(aecalhit->nscintwave)[j]);
         wave_cherenk->Fill(xw,(aecalhit->ncerwave)[j]); 
	}
	hchan->Fill(aecalhit->cellID);

        std::cout<<"Total number of channels=" << nchan << endl;
 
      // there is a better way to do this
	int jchan=aecalhit->cellID;
	int kchan=-1;
	for( int i=0;i<nchan;i++ ) {
	  if(ichan[i]==jchan) kchan=i;
	}
	if(kchan==-1) {
	  std::cout<<"unknown hit channel is "<< aecalhit->cellID<<std::endl;
	} else {
	  esumchan[kchan]+=aecalhit->energyDeposit;
	  ncerchan[kchan]+=aecalhit->ncerenkov;
	  nscintchan[kchan]+=aecalhit->nscintillator;
	}


      }  // end loop over hits

      // Does not work as expected giving a smaller fraction of photons
      // convert back to the expected rate since we fill 1 photon from every 1000
      //nscinttot = nscinttot /  supressRandom;
      //ncertot = ncertot / supressRandom;

    
      hcEcalE->Fill(esum/1000.);
      hcEcalncer->Fill(ncertot);
      hcEcalncer0->Fill(ncerchan[0]);
      hcEcalncer1->Fill(ncerchan[1]);
      hcEcalncer2->Fill(ncerchan[2]);
      hcEcalncer3->Fill(ncerchan[3]);
      hcEcalE0->Fill(esumchan[0]);
      hcEcalE1->Fill(esumchan[1]);
      hcEcalE2->Fill(esumchan[2]);
      hcEcalE3->Fill(esumchan[3]);

      // kludge for now
      float mainee=beamE*1000;
      heest->Fill((esum)/mainee);

 
      // reconstructed from Scintillation
      // this calibration found using e- guns 5 GeV
      float calibration_scint= 0.00524;
      float energy_scint = calibration_scint * nscinttot;
      heest_scint->Fill(energy_scint / mainee);


      // corrected energy for Scinitallation + Cherenkov 
      // https://arxiv.org/pdf/0707.4021.pdf
      // this calibration found using e- guns 5 GeV 
      float calibration_cherenkov = 0.00792; 
      float energy_cherenkov = calibration_cherenkov * ncertot;
      heest_cherenk->Fill(energy_cherenkov / mainee);


      
      // scatter plot for calibrated signals
      schint_cherenk_calib->Fill(energy_scint, energy_cherenkov);
      schint_cherenk_calib_rel->Fill(energy_scint/mainee, energy_cherenkov/mainee);
 
      float h_over_e_S=0.58; // h/e for scinittilation 
      float h_over_e_C=0.39; // h/e for cherenkov 
      //float kappa=(1-h_over_e_S) / (1-h_over_e_C);
 
      float kappa=0.68; 
      float a1=( energy_scint - kappa * energy_cherenkov);
      float a2= 1 - kappa;

      // overall calibration
      float calibration = 1.0;
      float energy_rec = (calibration)*a1/a2;
      heest_meass->Fill(energy_rec/mainee);

       /* debug 
       std::cout<<" True energy =  "<< mainee  << std::endl;
       std::cout<<" Hit energy deposit =  "<<esum << std::endl;
       std::cout<<" kappa = "<< kappa  << std::endl;
       std::cout<<" Scint energy = "<< energy_scint  << std::endl;
       std::cout<<" Cherenkov energy = "<< energy_cherenkov   << std::endl;
       std::cout<<" a1 = "<< a1   << std::endl;
       std::cout<<" a2 = "<< a2   << std::endl;
       std::cout<<" Cherenkov+Scint energy = "<< energy_rec  << std::endl;
       */

      if(ievt<SCEPRINT2) std::cout<<" total energy deposit "<<esum<< " reco energy =" <<  energy_rec << std::endl;
      float check=0.;
      for( int i=0;i<nchan;i++) {
	if(ievt<SCEPRINT2) std::cout<<"esum ["<<namechan[i]<<"]="<<esumchan[i]<<std::endl;
	check+=esumchan[i];
      }
      if(ievt<SCEPRINT2) std::cout<<" check total energy desposit "<<check<<std::endl;

      if(ievt<SCEPRINT2) std::cout<<" total number of cherenkov is "<<ncertot<<std::endl;
      check=0;
      for( int i=0;i<nchan;i++) {
	if(ievt<SCEPRINT2) std::cout<<"ncerenkov ["<<namechan[i]<<"]="<<ncerchan[i]<<std::endl;
	check+=ncerchan[i];
      }
      if(ievt<SCEPRINT2) std::cout<<" check ncerenkov "<<check<<std::endl;


      if(ievt<SCEPRINT2) std::cout<<" total number of scintillator is "<<nscinttot<<std::endl;
      check=0;
      for( int i=0;i<nchan;i++) {
	if(ievt<SCEPRINT2) std::cout<<"nscintillator ["<<namechan[i]<<"]="<<nscintchan[i]<<std::endl;
	check+=nscintchan[i];
      }
      if(ievt<SCEPRINT2) std::cout<<" check nscintillator "<<check<<std::endl;

       float  esumcrystal = esum;

       // look at correlations
       depos_scintil->Fill(esumcrystal, (float)nscinttot);
       depos_cherenk->Fill(esumcrystal, (float)ncertot);
       schint_cherenk->Fill((float)nscinttot, (float)ncertot);

       // light per MeV. Luminosyty Photons/MeV =300 See: http://scintillator.lbl.gov/
       scintilVsdepos->Fill(nscinttot/ (esumcrystal) );
       cherenkVsdepos->Fill(ncertot/ (esumcrystal) );
       scintil_cherenkVsdepos->Fill( (nscinttot+ncertot)/ (esumcrystal) );

       // just count  
       scintil->Fill(nscinttot);
       cherenk->Fill(ncertot);
       scintil_cherenk->Fill(nscinttot+ncertot);
       if (nscinttot>0) cherenkDIVscintil->Fill(ncertot/(float)nscinttot);


    }  //end loop over events
  }  // end if no events
    
  


  
 
 
  f->Close();

  TFile * out = new TFile(outputfilename,"RECREATE");
  hgenPsize->Write();
  hgenPdgID->Write();
  hcEcalE->Write();
  hcEcalncer->Write();
  hcEcalncer0->Write();
  hcEcalncer1->Write();
  hcEcalncer2->Write();
  hcEcalncer3->Write();

  wave_cherenk->Write();
  wave_scintil->Write();

  // corrected ratios
  heest->Write();
  heest_meass->Write();
  heest_scint->Write();
  heest_cherenk->Write();

  // sergei
  depos_scintil->Write();
  depos_cherenk->Write();
  schint_cherenk->Write();
  schint_cherenk_calib->Write();
  schint_cherenk_calib_rel->Write();
  scintilVsdepos->Write();
  cherenkVsdepos->Write();
  scintil->Write();
  cherenk->Write();
  cherenkDIVscintil->Write();
  scintil_cherenk->Write();
  scintil_cherenkVsdepos->Write();


  out->Close();

}



