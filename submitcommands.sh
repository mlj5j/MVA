#python tools/submitjobs.py --analyzer tools/prepMVA.py --fnamekeyword Summer16v3.ZGG --directoryout TreeMakerRandS_mvaprep
#python tools/submitjobs.py --analyzer tools/prepMVA.py --fnamekeyword Summer16v3.GJets --directoryout TreeMakerRandS_mvaprep
#python tools/submitjobs.py --analyzer tools/prepMVA.py --fnamekeyword Summer16v3Fast.SMS-T6Wg --directoryout TreeMakerRandS_mvaprep
#python tools/submitjobs.py --analyzer tools/prepMVA.py --fnamekeyword Summer16v3Fast.SMS-T5Wg --directoryout TreeMakerRandS_mvaprep
#python tools/submitjobs.py --analyzer tools/prepMVA.py --fnamekeyword Summer16v3.WGJets --directoryout TreeMakerRandS_mvaprep
#python tools/submitjobs.py --analyzer tools/prepMVA.py --fnamekeyword Summer16v3.GJet_Pt --directoryout TreeMakerRandS_mvaprep
#python tools/submitjobs.py --analyzer tools/prepMVA.py --fnamekeyword Summer16v3.TTJets --directoryout TreeMakerRandS_mvaprep
#python tools/submitjobs.py --analyzer tools/prepMVA.py --fnamekeyword Run2016  --directoryout TreeMakerRandS_mvaprep

python tools/submitjobs.py --analyzer tools/applyBDTscore.py --fnamekeyword Summer16v3.ZGG --directoryout TreeMakerRandS_BDTapplied
python tools/submitjobs.py --analyzer tools/applyBDTscore.py --fnamekeyword Summer16v3.GJets --directoryout TreeMakerRandS_BDTapplied
python tools/submitjobs.py --analyzer tools/applyBDTscore.py --fnamekeyword Summer16v3Fast.SMS-T6Wg --directoryout TreeMakerRandS_BDTapplied
python tools/submitjobs.py --analyzer tools/applyBDTscore.py --fnamekeyword Summer16v3Fast.SMS-T5Wg --directoryout TreeMakerRandS_BDTapplied
python tools/submitjobs.py --analyzer tools/applyBDTscore.py --fnamekeyword Summer16v3.WGJets --directoryout TreeMakerRandS_BDTapplied
#python tools/submitjobs.py --analyzer tools/applyBDTscore.py --fnamekeyword Summer16v3.GJet_Pt --directoryout TreeMakerRandS_BDTapplied
#python tools/submitjobs.py --analyzer tools/applyBDTscore.py --fnamekeyword Summer16v3.TTJets --directoryout TreeMakerRandS_BDTapplied

python tools/submitjobs.py --analyzer tools/applyBDTscore.py --fnamekeyword Run2016 --directoryout TreeMakerRandS_BDTapplied
