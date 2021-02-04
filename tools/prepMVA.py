from ROOT import *
from array import array
import numpy as np
import sys
import argparse
import math

gROOT.SetBatch(1)

fname = sys.argv[1]
print 'Loading {0}'.format(fname)



#parser = argparse.ArgumentParser(description='Adding some branches to prepare a file for MVA training')
#parser.add_argument('-k', dest='keyword', help='dataset name without .root (ie T5Wg_m1500.0d1200 )')

#flist = open('../usefulthings/filelist_all.txt', 'r')
#args = parser.parse_args()
#keyword = args.keyword

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

#fname = 'root://cmseos.fnal.gov/{0}'.format(args.fin)

#ch.Add(fname)

#finname = 'root://cmseos.fnal.gov//store/group/lpcsusyphotons/TreeMakerRandS_BDT/{0}.root'.format(args.fin)

Isdata = False
if 'Run20' in fname:
    Isdata = True

n_evt = ccounter.GetEntries()
print "tcounter should have {0} entries".format(n_evt)

#fout = TFile.Open(foutname, "RECREATE")
#fout.mkdir('TreeMaker2')
#fout.cd('TreeMaker2/')

tree = ch.CloneTree(0)
entries = ch.GetEntries()
 
#--------------Adding branches--------------------------------------------
EventWeight = np.zeros(1,dtype=float)
mva_dPhi1 = np.zeros(1,dtype=float)
mva_dPhi2 = np.zeros(1,dtype=float)
mva_minOmega = np.zeros(1,dtype=float)
PhotonsAUX = ROOT.std.vector('TLorentzVector')()


xsec = np.zeros(1,dtype=float)

IsEnriched = False
if 'DoubleEMEnriched' in fname:
    print 'updating xsection for GJet_DoubleEMEnriched process!'
    ch.SetBranchAddress('CrossSection', xsec)
    IsEnriched = True

b_EventWeight = tree.Branch('EventWeight', EventWeight, 'EventWeight/D')
b_mva_dPhi1 = tree.Branch('mva_dPhi1', mva_dPhi1, 'mva_dPhi1/D')
b_mva_dPhi2 = tree.Branch('mva_dPhi2', mva_dPhi2, 'mva_dPhi2/D')
b_mva_minOmega = tree.Branch('mva_minOmega', mva_minOmega, 'mva_minOmega/D')
b_PhotonsAUX = tree.Branch('PhotonsAUX', PhotonsAUX)

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

    dphi1 = ch.JetsAUX[0].Phi() - ch.HardMETPhi
    if dphi1 >= math.pi:
        dphi1 = dphi1 - 2*math.pi
    if dphi1 < -math.pi:
        dphi1 = dphi1 + 2*math.pi
    
    if IsEnriched:
        xsec[0] = 113100.0

    PhotonsAUX.clear()
    for ipho, pho in enumerate(ch.Photons):
        if not pho.Pt()>75: continue
        if not bool(ch.Photons_fullID[ipho]): continue
        if not abs(pho.Eta())<2.4: continue
        tlvpho = TLorentzVector()
        tlvpho.SetPtEtaPhiE(pho.Pt(), pho.Eta(), pho.Phi(), pho.E())
        PhotonsAUX.push_back(tlvpho)

    dphi = 99.0
    minomega = 99.0
    omegas = []
    for jet in ch.JetsAUX:
        if jet.Pt()>30:
            dphi = jet.Phi() - ch.HardMETPhi
            if dphi >= math.pi:
                dphi = dphi - 2*math.pi
            if dphi < -math.pi:
                dphi = dphi + 2*math.pi
            dphi = abs(dphi)
#            print dphi
            omegas.append(np.arctan(np.sin(min(dphi, 0.5*math.pi))/(jet.Pt()/ch.mva_HardMET)))

    for omega in omegas:
        #print omega
        minomega = min(minomega, omega)

    mva_minOmega[0] = minomega

####----------------------------------------------------------
    dphi2 = ch.JetsAUX[1].Phi() - ch.HardMETPhi
    if dphi2 >= math.pi:
        dphi2 = dphi2 - 2*math.pi
    if dphi2 < -math.pi:
        dphi2 = dphi2 + 2*math.pi

    mva_dPhi1[0] = abs(dphi1)
    mva_dPhi2[0] = abs(dphi2)
#    mva_dPhi1[0] = min(abs(ch.JetsAUX[0].Phi() - ch.HardMETPhi), abs(ch.HardMETPhi - ch.JetsAUX[0].Phi()))
#    mva_dPhi2[0] = min(abs(ch.JetsAUX[1].Phi() - ch.HardMETPhi), abs(ch.HardMETPhi - ch.JetsAUX[1].Phi()))


     
    if ch.IsRandS:
        if Isdata:
            EventWeight[0] = 1.0/ch.NSmearsPerEvent
        else:
            EventWeight[0] = ch.CrossSection*ch.puWeight/(ch.NSmearsPerEvent*n_evt)

    if not ch.IsRandS:
        if Isdata:
            EventWeight[0] = 1.0
        else:
            EventWeight[0] = ch.CrossSection*ch.puWeight/n_evt
    
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

    
