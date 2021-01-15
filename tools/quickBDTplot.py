from ROOT import *
import numpy as np
import sys


keyword = sys.argv[1]

flistname = '../filelists/filelist_BDTapplied.txt'
flist = open(flistname)
fnamelines = flist.readlines()
flist.close()

ch = TChain('TreeMaker2/PreSelection')
hBDT = TH1F('hBDT','hBDT',20, -1, 1)
hBDT.Sumw2()
for fname_ in fnamelines:
    if not keyword in fname_: continue
    fname = fname_.strip()
    ch.Add('root://cmseos.fnal.gov/{0}'.format(fname))

entries = ch.GetEntries()

for j_entry in range(entries):
    i_entry = ch.LoadTree(j_entry)
    if i_entry < 0:
        break
    nb = ch.GetEntry(j_entry)
    if nb<=0:
        continue
    if j_entry%500==0:
        print 'Processing entry {0}'.format(j_entry)

    if ch.mva_Photons0Et < 80: continue
    if ch.mva_Photons1Et < 80: continue
    if ch.mva_Ngoodjets < 2: continue
    if ch.mva_min_dPhi < 0.5: continue
    if ch.mva_HardMET < 110: continue

    hBDT.Fill(ch.mva_BDTstrong_v2, ch.EventWeight)

c1 = TCanvas('c1', 'c1', 500, 500)
hBDT.Draw()

sys.stdin.readline()
