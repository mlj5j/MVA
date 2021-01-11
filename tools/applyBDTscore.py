from ROOT import *
from array import array
import numpy as np
import sys
import argparse
import math

gROOT.SetBatch(1)

fname = sys.argv[1]
print 'Loading {0}'.format(fname)


tcounter = TTree('tcounter', 'tcounter')

ccounter = TChain('tcounter')
ch = TChain('TreeMaker2/PreSelection')


if '/store/' in fname:
    ch.Add('root://cmseos.fnal.gov/{0}'.format(fname))
    ccounter.Add('root://cmseos.fnal.gov/{0}'.format(fname))
    print 'Adding root://cmseos.fnal.gov/{0}'.format(fname)
else:
    print 'File path may not be properly formatted.'


fnameout = fname.split('/')[-1].replace('.root', '_mvaprep.root')
print 'out file is {0}'.format(fnameout)
fout = TFile.Open(fnameout, 'recreate')
fout.mkdir('TreeMaker2')
fout.cd('TreeMaker2')



Isdata = False
if 'Run20' in fname:
    Isdata = True


n_evt = ccounter.GetEntries()
print "tcounter should have {0} entries".format(n_evt)


tree = ch.CloneTree(0)
entries = ch.GetEntries()

mva_ST = array('f',[0])
mva_Pt_jets = array('f',[0])
mva_dPhi_GG = array('f',[0])
mva_Photons0Et = array('f',[0])
mva_Photons1Et = array('f',[0])
mva_HardMET = array('f',[0])
mva_Pt_GG = array('f',[0])
mva_ST_jets = array('f',[0])
mva_min_dPhi = array('f',[0])
mva_dPhi_GGHardMET = array('f',[0])
mva_dPhi1 = array('f',[0])
mva_dPhi2 = array('f',[0])
#mva_minOmega = array('f',[0])
mva_Ngoodjets = array('i',[0])

reader = TMVA.Reader()
reader.AddVariable('mva_ST', mva_ST)
reader.AddVariable('mva_Pt_jets', mva_Pt_jets)
reader.AddVariable('mva_dPhi_GG', mva_dPhi_GG)
reader.AddVariable('mva_Photons0Et', mva_Photons0Et)
reader.AddVariable('mva_Photons1Et', mva_Photons1Et)
reader.AddVariable('mva_HardMET', mva_HardMET)
reader.AddVariable('mva_Pt_GG', mva_Pt_GG)
reader.AddVariable('mva_ST_jets', mva_ST_jets)
reader.AddVariable('mva_min_dPhi', mva_min_dPhi)
reader.AddVariable('mva_dPhi1', mva_dPhi1)
reader.AddVariable('mva_dPhi2', mva_dPhi2)
reader.AddVariable('mva_dPhi_GGHardMET', mva_dPhi_GGHardMET)
#reader.AddVariable('mva_minOmega', mva_minOmega)
reader.AddSpectator('mva_Ngoodjets', mva_Ngoodjets)

reader.BookMVA("BDT",'tools/TMVAClassification_BDT_100trees_4maxdepth.weights.xml')
#reader.BookMVA("BDT",'dataset_bdt_2016_T5Wg_m1800_100trees_4maxdepth/weights/TMVAClassification_BDT_100trees_4maxdepth.weights.xml')
 
#--------------Adding branches--------------------------------------------

mva_BDTstrong_v2 = np.zeros(1,dtype=float)
#testcounter = np.zeros(1,dtype=float)
b_mva_BDTstrong_v2 = tree.Branch('mva_BDTstrong_v2', mva_BDTstrong_v2, 'mva_BDTstrong_v2/D')
#b_testcounter= tree.Branch('testcounter', testcounter, 'testcounter/D')
 
#print mva_BDTstrong_v2[0]
#entries = 5
for j_entry in range(entries):
    i_entry = ch.LoadTree(j_entry)
    if i_entry < 0:
        break
    nb = ch.GetEntry(j_entry)
    if nb<=0:
        continue
    if j_entry%500==0:
        print 'Processing entry {0}'.format(j_entry)

    if j_entry == 0:
        if ch.TriggerPass[21] == -1:
            i_trig = 22
        else: i_trig = 21

    mva_ST[0] = ch.mva_ST
    mva_Pt_jets[0] = ch.mva_Pt_jets
    mva_dPhi_GG[0] = ch.mva_dPhi_GG
    mva_Photons0Et[0] = ch.mva_Photons0Et
    mva_Photons1Et[0] = ch.mva_Photons1Et
    mva_HardMET[0] = ch.mva_HardMET
    mva_Pt_GG[0] = ch.mva_Pt_GG
    mva_ST_jets[0] = ch.mva_ST_jets
    mva_min_dPhi[0] = ch.mva_min_dPhi
    mva_dPhi_GGHardMET[0] = ch.mva_dPhi_GGHardMET
    mva_dPhi1[0] = ch.mva_dPhi1
    mva_dPhi2[0] = ch.mva_dPhi2
    mva_BDTstrong_v2[0] = reader.EvaluateMVA('BDT')
#    mva_minOmega[0] = ch.mva_minOmega
#    print 'after bdt {0}'.format(mva_BDTstrong_v2[0])
    tree.Fill()

for i in range(n_evt):
    tcounter.Fill()

fout.cd()
#tree.Write()
fout.cd('../')
tcounter.Write()
#ccounter.Print()
#fout.Write()
fout.cd('TreeMaker2')
tree.Write()
fout.Close()
#sys.stdin.readline()

    
