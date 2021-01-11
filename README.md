# SUSY diphoton MVA

This is used for training and testing a boosted decision tree for discrimating between real and fake MET.

##  Getting Started
Clone the repository to your workspace

#  Prepare files for MVA
Go to the tools directory and open "submitjobs.py".  Make sure it's reading the txt file "filelist_skimmed.txt".
From the MVA directory you can open the file `submitcommands.sh`.  This file contains the commands for submitting jobs to condor for each keyword/dataset.  Make sure all of the commands that include "applyBDT.py" are commented.  

#  Apply BDT
In the MVA directory you can use the following command (I'll probably automate this eventually):
```
xrdfsls /store/group/lpcsusyphotons/TreeMakerRandS_mvaprep > filelists/filelist_mva.txt
```

Go to "submitjobs.py" in the tools directory and change the file being read to "filelist_mva.txt".

Go back to the `submitcommands.sh`, comment the lines with "prepMVA", and uncomment the lines with "applyBDT.py".  This will submit jobs to condor to apply the BDT to all of the files.  


#Ignore the rest of this README because it's older and needs to be updated.



```
mkdir Results
mkdir filelists
```

The code gets file paths from a list in filelists/<filename>.txt and loads them into a TChain for training/testing the BDT.
You have to make the filelist <filename>.txt yourself using xrdfsls as follows from the filelists directory:
```
xrdfsls /store/group/<restofpath>/ | grep searchstring > searchstring_year.txt
```
For example:
```
xrdfsls /store/group/lpcsusyphotons/TreeMakerRandS_BDTv2/ | grep Summer16v3.GJet > GJets_2016.txt
```
## Running
Once you have the filelists made you can go to MVA/tools and run BDT_strong.py to train and test the BDT:
```
python BDT_strong.py -y1 2016 -s T5Wg_m1700.0d15xx -b GJets -nt 100 -md 10 -n T5Wg_m1700.0d15xx_2016
```
This would train a BDT using T5Wg files specified in ../filelists/T5Wg_m1700.0d15xx_2016.txt (1700 GeV gluino mass and neutralino mass from 1500-1599 GeV from 2016) with 100 trees with max depth of 10.  The ouput would have the string "T5Wg_m1700.0d15xx_2016" included in the name.
