
#Do relevent imports
from ROOT import TChain, gROOT, TFile, TCut, TMVA, TLorentzVector
import numpy as np
import sys
import argparse

#  An example of running this would be
#  python BDT_strong.py -y1 2016 -s SMS-T5Wg_m1700.0d15xx -b GJets -nt 100 -md 10 -n T5Wg_m1700.0d15xx_2016
#  This would train a BDT using T5Wg files specified in ../filelists/T5Wg_m1700.0d15xx_2016.txt (1700 GeV gluino mass and neutralino mass from 1500-1599 GeV from 2016) with 100 trees with max depth of 10.  
#  The ouput would have the string "T5Wg_m1700.0d15xx_2016" included in the name.

gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description="Training BDT to separate real and fake MET")



parser.add_argument('-s', '--signal', dest='sig_name', help='This is the sample used for signal, ie ZGGtonunuGG ')
parser.add_argument('-y', dest='year', help='This is the year (obviously)')
#parser.add_argument('-y2', dest='year2', default='0', help='This is the second year to include. Leave blank if only doing one year')
#parser.add_argument('-y3', dest='year3', default='0', help='This is the third year to include. Leave blank if only doing one year')

parser.add_argument('-b', '--background', dest='back_name', help='This is the sample used for the backbaround, ie GJets or QCD')

parser.add_argument('-m', '--mode', dest='mode', default='RandS', help='If training on RandS samples, you should put RandS here.')

parser.add_argument('-n', '--name', dest='name', default='test', help='This is a string appended to the output file name to serve as an identifier')
parser.add_argument('-nt', '--ntrees', dest='Ntrees', type = int, help = 'This is the number of trees in the bdt')
parser.add_argument('-md', '--maxdepth', dest='maxdepth', type = int, help = 'This is the maximum depth for each tree')

args = parser.parse_args()

year = args.year
sig_name = args.sig_name
back_name = args.back_name

#Read file lists to make TChains.  There should be one TChain for signal and one for background
if args.mode=='RandS':
     print "Rebalance and smear has been selected"
     sig = TChain("TreeMaker2/PreSelection")
     bkg = TChain("TreeMaker2/PreSelection")
else:
     sig = TChain("PreSelection")
     bkg = TChain('PreSelection')

Isfastsim = False

if 'SMS' in sig_name:
     Isfastsim = True

if '2016' in year:
     sig_name = 'Summer16v3Fast.{0}'.format(sig_name)
     back_name = 'Summer16v3.{0}'.format(back_name)
if '2017' in year:
     sig_name = 'Fall17Fast.{0}'.format(sig_name)
     back_name = 'Fall17.{0}'.format(back_name)
if '2018' in year:
     sig_name = 'Autumn18Fast.{0}'.format(sig_name)
     back_name = 'Autumn18.{0}'.format(back_name)

if not Isfastsim:
     sig_name = sig_name.replace('Fast','')



flist = open('../filelists/filelist_mvaprepped.txt')
for line in flist:
     if sig_name in line:
          sig.Add('root://cmseos.fnal.gov/{0}'.format(line.strip()))
     if back_name in line:
          bkg.Add('root://cmseos.fnal.gov/{0}'.format(line.strip()))
#     if 'Summer16v3.GJet_Pt' in line:
#          bkg.Add('root://cmseos.fnal.gov/{0}'.format(line.strip()))

flist.close()     

fout = TFile.Open("../Results/BDT_output_{3}_{0}_{1}trees_{2}maxdepth.root".format(args.name, args.Ntrees, args.maxdepth, year),"RECREATE")

TMVA.Tools.Instance()

factory = TMVA.Factory("TMVAClassification", fout, "V:!Silent:Color:Transformations=I:DrawProgressBar:AnalysisType=Classification")


loader = TMVA.DataLoader("dataset_bdt_{3}_{0}_{1}trees_{2}maxdepth".format(args.name, args.Ntrees, args.maxdepth, year))

#Add TChains to factory
loader.AddSignalTree(sig, 1.0)
loader.AddBackgroundTree(bkg, 1.0)

if args.mode == 'RandS':
#     loader.AddVariable('mva_Ngoodjets','I')
     loader.AddVariable('mva_ST','F')
     loader.AddVariable('mva_Pt_jets','F')
     loader.AddVariable('mva_dPhi_GG','F')
     loader.AddVariable('mva_Photons0Et','F')
     loader.AddVariable('mva_Photons1Et','F')
     loader.AddVariable('mva_HardMET','F')
     loader.AddVariable('mva_Pt_GG','F')
     loader.AddVariable('mva_ST_jets','F')
     loader.AddVariable('mva_min_dPhi','F')
     loader.AddVariable('mva_dPhi1','F')
     loader.AddVariable('mva_dPhi2','F')
     loader.AddVariable('mva_dPhi_GGHardMET','F')
#     loader.AddVariable('mva_minOmega','F')
     loader.AddSpectator('mva_Ngoodjets', 'I')
#     loader.AddVariable('mass_GG','F')

else:
#Add variables and spectators to factory
     loader.AddVariable('Ngoodjets','I')
     loader.AddVariable('ST','F')
     loader.AddVariable('Pt_jets','F')
     loader.AddVariable('dPhi_GG','F')

#basic attempt
     loader.AddVariable('Photons[0].Et()','F')
     loader.AddVariable('Photons[1].Et()','F')
     loader.AddVariable('HardMET','F')
     loader.AddVariable('Pt_GG','F')
     loader.AddVariable('ST_jets','F')

#--Some deltaPhi variables:
     loader.AddVariable('min_dPhi','F')
     loader.AddVariable('dPhi_GGHardMET','F')

#Define cuts to be applied
sigcuts = TCut('min_dPhi>-1 && min_dPhi<10 && Photons_isEB[0]==1 && Photons_isEB[1]==1 && Photons[0].Et()>80 && Photons[1].Et()>80 && mva_Ngoodjets>1') 
bkgcuts = TCut('min_dPhi>-1 && min_dPhi<10 && Photons_isEB[0]==1 && Photons_isEB[1]==1 && Photons[0].Et()>80 && Photons[1].Et()>80 && mva_Ngoodjets>1')

sigcuts_RandS = TCut('Pho1_hasPixelSeed==0 && Pho2_hasPixelSeed==0 && IsRandS==0 && HardMETPt>110 && Photons_isEB[0]==1 && Photons_isEB[1]==1 && mva_Ngoodjets>1 && mva_Photons0Et>80 && mva_Photons1Et>80')
bkgcuts_RandS = TCut('Pho1_hasPixelSeed==0 && Pho2_hasPixelSeed===0 && HardMETPt>110 && Photons_isEB[0]==1 && Photons_isEB[1]==1 && mva_Ngoodjets>1 && mva_Photons0Et>80 && mva_Photons1Et>80')


#Prepare trees for training and testing (I think this just applies the cuts)
if args.mode == 'RandS':
     loader.PrepareTrainingAndTestTree(sigcuts_RandS, bkgcuts_RandS, "SplitMode=random:!V")

else:
     loader.PrepareTrainingAndTestTree(sigcuts, bkgcuts, "SplitMode=random:!V")
#Use BookMethod to specify BDT

#factory.BookMethod(loader, TMVA.Types.kBDT, 'BDT_otherthing', '!H:!V:NTrees=200:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex')

factory.BookMethod(loader, TMVA.Types.kBDT, 'BDT_{0}trees_{1}maxdepth'.format(args.Ntrees, args.maxdepth), "NTrees={0}:MaxDepth={1}".format(args.Ntrees, args.maxdepth))

#factory.BookMethod(loader, TMVA.Types.kBDT, 'BDTB_{0}trees_{1}maxdepth'.format(args.Ntrees, args.maxdepth), "NTrees={0}:MaxDepth={1}:BoostType=Bagging".format(args.Ntrees, args.maxdepth))

#factory.BookMethod(loader, TMVA.Types.kBDT, 'BDTRA_{0}trees_{1}maxdepth'.format(args.Ntrees, args.maxdepth), "NTrees={0}:MaxDepth={1}:BoostType=RealAdaBoost".format(args.Ntrees, args.maxdepth))

#factory.BookMethod(loader, TMVA.Types.kBDT, 'BDTF{0}trees_{1}maxdepth'.format(args.Ntrees, args.maxdepth), "NTrees={0}:MaxDepth={1}:UseFisherCuts".format(args.Ntrees, args.maxdepth))

#factory.BookMethod(loader, TMVA.Types.kBDT, 'BDT_15D', "NTrees=200:MaxDepth=15")
#Train, test, and evaluate
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
#close output file
fout.Close()
#Open output file in TMVAGUI (must be in batch mode I think)
print 'TMVA Classification is done!'

#gROOT.ProcessLine(fout)
c = factory.GetROCCurve(loader)
c.Draw()
#sys.stdin.readline()


