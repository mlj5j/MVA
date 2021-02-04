from ROOT import *
import sys, os
import argparse
import math


fout = TFile("optimizeBDTplots.root",'recreate')

parser = argparse.ArgumentParser(description = 'Finding optimal BDT cut')
parser.add_argument('-s', dest='sigkey', type=str, help='Should be something like Summer16v3Fast.SMS-T5Wg_m1900')
parser.add_argument('-b', dest='bkgkey', type=str, help='Should be something like Summer16v3.GJets_DR')
args = parser.parse_args()

sigkey = args.sigkey
bkgkey = args.bkgkey

flistname = '../filelists/filelist_BDTapplied.txt'
flist = open(flistname)
fnamelines = flist.readlines()
flist.close()

chsig = TChain('TreeMaker2/PreSelection')
chbkg = TChain('TreeMaker2/PreSelection')


#hsigBDT = makeTh1('hsigBDT', 'signal BDT', 20, -1, 1)
#hbkgBDT = makeTh1('hbkgBDT', 'background BDT', 20, -1, 1)
grsignif = TGraph()
hsigBDT = TH1F('hsigBDT','hsigBDT',100, -1, 1)
hsigBDT.Sumw2()
hbkgBDT = TH1F('hbkgBDT','hbkgBDT',100, -1, 1)
hbkgBDT.Sumw2()
hsignif = TH2F('hsignif', 'Significance vs BDT score', 100, -1, 1, 50, 0, 7)
hsignif.Sumw2()

for fname_ in fnamelines:
    if sigkey in fname_:
        fname = fname_.strip()
        chsig.Add('root://cmseos.fnal.gov/{0}'.format(fname))
    if bkgkey in fname_:
        fname = fname_.strip()
        chbkg.Add('root://cmseos.fnal.gov/{0}'.format(fname))


sig_entries = chsig.GetEntries()

for j_entry in range(sig_entries):
    i_entry = chsig.LoadTree(j_entry)
    if i_entry < 0:
        break
    nb = chsig.GetEntry(j_entry)
    if nb<=0:
        continue
    if j_entry%500==0:
        print 'Processing entry {0} of {1}'.format(j_entry, sig_entries)
    if 'TTJets' in sigkey:
        if not chsig.Pho1_hasPixelSeed: continue
        if not chsig.Pho2_hasPixelSeed: continue
    if chsig.mva_Photons0Et < 80: continue
    if chsig.mva_Photons1Et < 80: continue
    if chsig.mva_Ngoodjets < 2: continue
    if abs(chsig.PhotonsAUX[0].Eta()) > 1.442: continue
    if abs(chsig.PhotonsAUX[1].Eta()) > 1.442: continue
 #   if chsig.mva_min_dPhi < 0.5: continue
    if chsig.mva_HardMET < 100: continue
    if chsig.IsRandS: continue
    if abs(chsig.HardMetMinusMet)>90: continue
#    weight = 137000*chsig.CrossSection*chsig.puWeight
    weight = 137000*chsig.EventWeight
    if 'SMS' in sigkey:
        if chsig.Pho1_hasPixelSeed: continue
        if chsig.Pho2_hasPixelSeed: continue
        weight = 4*weight
    hsigBDT.Fill(chsig.mva_BDTstrong_v2, weight)

bkg_entries = chbkg.GetEntries()

for j_entry in range(bkg_entries):
    i_entry = chbkg.LoadTree(j_entry)
    if i_entry < 0:
        break
    nb = chbkg.GetEntry(j_entry)
    if nb<=0:
        continue
    if j_entry%5000==0:
        print 'Processing entry {0} of {1}'.format(j_entry, bkg_entries)

    if chbkg.mva_Photons0Et < 80: continue
    if chbkg.mva_Photons1Et < 80: continue
    if chbkg.mva_Ngoodjets < 2: continue
    if 'DYJets' in bkgkey or 'GJets' in bkgkey:
        if not chbkg.Pho1_hasPixelSeed: continue
        if not chbkg.Pho2_hasPixelSeed: continue
    else:
        if chbkg.Pho1_hasPixelSeed: continue
        if chbkg.Pho2_hasPixelSeed: continue
    if abs(chbkg.HardMetMinusMet)>90: continue
    if abs(chbkg.PhotonsAUX[0].Eta()) > 1.442: continue
    if abs(chbkg.PhotonsAUX[1].Eta()) > 1.442: continue
#    if chbkg.mva_min_dPhi < 0.5: continue
    if chbkg.mva_HardMET < 100: continue
    weight = 137000*chbkg.EventWeight
    hbkgBDT.Fill(chbkg.mva_BDTstrong_v2, weight)

for i in range(hsigBDT.GetNbinsX()):
    s = hsigBDT.Integral() - hsigBDT.Integral(0, i+1)
    b = hbkgBDT.Integral() - hbkgBDT.Integral(0, i+1)
    db = 0.25*b
    if s==0 and b==0: continue
    #signif = s/(math.sqrt(b + 0.04*b**2))
    signif = s/(math.sqrt(s + b + db**2))
    print 'Significance is {0} at BDT={1}'.format(signif, hsigBDT.GetBinCenter(i))
    hsignif.Fill(hsigBDT.GetBinCenter(i), signif)
    grsignif.SetPoint(i, hsigBDT.GetBinCenter(i), signif)

grsignif.SetTitle('Significance for {0} and {1}; BDT score; Significance'.format(sigkey, bkgkey))
#c1 = mkcanvas()
c1 = TCanvas('c1', 'c1', 500, 500)
c1.cd()
grsignif.Draw("A*")
c1.Write()


c2 = TCanvas('c2', 'c2', 500, 500)
c2.cd()
hsigBDT.Draw()
hsigBDT.Write()
hbkgBDT.Write()
hsignif.Write()
#grsignif.Write()
fout.Close()

sys.stdin.readline()

#        signif = s/(math.sqrt(b + 0.04*b**2))
        #signif = s/(math.sqrt(s + b))
        #signif = math.sqrt(2*(s+b)*math.log(1+s/b)-2*s)
