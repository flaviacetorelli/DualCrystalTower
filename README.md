# DualCrystalTower 

This is an example of a single barrel ECAL+HCAL tower  with crystals (PbWO4). 
The width is 20x20cm, while the length is 100cm. It has 5 layers, each has 20 cm depth.
The first layer mimics the ECAL with 22.4X0. The other 4 layers are HCAL with about 3.9 lambda(I).
The total depth of this tower is about 4.93 lambda (including the ECAL section).

Check the ECAL geometry using this top-level file SimpleECAL.xml that includes "ECalBarrel_DualCrystal.xml":

```bash
geoDisplay DRSingleCrystal.xml 
```

Run this example using the script "A_RUN". It  makes the ROOT file (usieng Sarah's example). This program works when using material "PbWO4". This does not give scintillation photons, but you will see Cherenkov photons.

This program is based on the SingleDualCrystal by Sarah Eno (eno@umd.edu).

Here is an example:  K- beam (5 GeV) 


![K-beam example](compact/images/kaon_5gev.png?raw=true)



##  Installation 

```bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_101/x86_64-centos7-gcc11-opt/setup.sh
git clone https://github.com/AIDASoft/DD4hep.git
cd DD4hep/examples
git clone git@github.com:chekanov/DualCrystalTower.git 
# edit CMakeLists.txt and add DualCrystalTower to
# SET(DD4HEP _EXAMPLES "AlignDet CLICSiD ClientTests Conditions DDCMS DDCodex DDDigi DDG4 DDG4_MySensDet LHeD Optica\
lSurfaces Persistency DDCAD SimpleDetector DualCrystalTower"
CACHE STRING "List of DD4hep Examples to build")

cd ..
mkdir build
mkdir install
cd build/
cmake -DDD4HEP_USE_GEANT4=ON -DBoost_NO_BOOST_CMAKE=ON -DDD4HEP_USE_LCIO=ON -DBUILD_TESTING=ON -DROOT_DIR=$ROOTSYS -D CMAKE_BUILD_TYPE=Release -DDD4HEP_BUILD_EXAMPLES=ON ..
make -j4
make install
cd ..
source bin/thisdd4hep.sh
```

S.Chekanov (ANL)
