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
### On LXPLUS

Source the environment.

```bash
source /cvmfs/sft.cern.ch/lcg/views/dev4/latest/x86_64-centos7-gcc11-opt/setup.sh 
```

### Local
Source the environment.

```bash
source /PATH/root_6-24-06_install/bin/thisroot.sh
source /PATH/LCIO/setup.sh
source /PATH/geant4-11.0.0_install/bin/geant4.sh
source /PATH/DD4hep_install/bin/thisdd4hep.sh
```
You can add these lines to your .bashrc file.

### Installing the repo

Clone this repo:

```bash
git clone git@github.com:flaviacetorelli/DualCrystalTower.git 
```

Compile:

```bash
cmake -B build -S . -D CMAKE_INSTALL_PREFIX=install
cmake --build build -- install
```

Now to let the programs know where to find our freshly built detector, we have to update this env variable

```bash
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
```

Compile and install after every modification of the c++ detector constructor code.

```bash
cmake --build build -- install
```



