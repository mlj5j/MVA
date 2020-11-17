# SUSY diphoton MVA

This is used for training and testing a boosted decision tree for discrimating between real and fake MET.

##  Getting Started
Clone the repository to your workspace
From the MVA directory do
'''
mkdir Results
mkdir filelists
'''
The code gets file paths from a list in filelists/<filename>.txt and loads them into a TChain for training/testing the BDT.
You have to make the filelist <filename>.txt yourself using xrdfsls as follows from the filelists directory:
'''
xrdfsls /store/group/<restofpath>/ | grep searchstring > searchstring_year.txt
'''
For example:
'''
xrdfsls /store/group/lpcsusyphotons/TreeMakerRandS_BDTv2/ | grep Summer16v3.GJet > GJets_2016.txt
'''

Once you have the filelists made you can go to MVA/tools and run BDT_strong.py to train and test the BDT:
'''
python BDT_strong.py -y1 2016 -s T5Wg_m1700.0d15xx -b GJets -nt 100 -md 10 -n T5Wg_m1700.0d15xx_2016
'''
This would train a BDT using T5Wg files specified in ../filelists/T5Wg_m1700.0d15xx_2016.txt (1700 GeV gluino mass and neutralino mass from 1500-1599 GeV from 2016) with 100 trees with max depth of 10.  The ouput would have the string "T5Wg_m1700.0d15xx_2016" included in the name.