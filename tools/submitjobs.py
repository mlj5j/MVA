import os, sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/applyXsec.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default='Summer16.SMS-T1tttt_mGluino-1200_mLSP-800',help="file")
parser.add_argument("-quickrun", "--quickrun", type=bool, default=False,help="Quick practice run (True, False)")
parser.add_argument("-forcetemplates", "--forcetemplates", type=str, default=False,help="you can use this to override the template choice")


args = parser.parse_args()

fnamekeyword = args.fnamekeyword.strip()
quickrun = args.quickrun
analyzer = args.analyzer

istest = False
skipFilesWithErrorFile = True


#try: 
#	moreargs = ' '.join(sys.argv)
#	moreargs = moreargs.split('--fnamekeyword')[-1]	
#	moreargs = ' '.join((moreargs.split()[1:]))
#except: moreargs = ''

#moreargs = moreargs.strip()
#print 'moreargs', moreargs

    
cwd = os.getcwd()

#fnamefilename = 'usefulthings/filelistDiphotonBig.txt'
#fnamefilename = 'usefulthings/filelist_test.txt'
fnamefilename = 'filelists/filelist_training.txt'
fnamefile = open(fnamefilename)


fnamelines = fnamefile.readlines()
fnamefile.close()
import random
random.shuffle(fnamelines)

if 'Summer16' in fnamekeyword:
        year = 2016
if 'Fall17' in fnamekeyword:
        year = 2017
if 'Autumn18' in fnamekeyword:
        year = 2018

if 'ZGG' in fnamekeyword:
        sample = 'ZGGtonunuGG'
if 'T6Wg' in fnamekeyword:
        sample = 'signal'

if ( not os.path.exists(os.path.expandvars("$X509_USER_PROXY")) ):
    print "#### No GRID PROXY detected. Please do voms-proxy-init -voms cms before submitting Condor jobs ####.\nEXITING"
    quit()


def main():
    counter = 0    
    for fname_ in fnamelines:
        if not (fnamekeyword in fname_): continue
        fname = fname_.strip()
        foutname = fname.split('/')[-1]
        job = analyzer.split('/')[-1].replace('.py','').replace('.jdl','')+'-'+fname.split('/')[-1].strip()
        #from utils import pause
        #pause()
        job = job.replace('.root','')
        print 'creating jobs:',job
        jdlname = 'jobs/'+job+'.jdl'        
        newjdl = open(jdlname,'w')
        newjdl.write(jdltemplate.replace('CWD',cwd).replace('JOBKEY',job))
        newjdl.close()
        if skipFilesWithErrorFile:
            errfilename = 'jobs/'+job+'.err'
            if os.path.exists(errfilename): 
                print 'skipping you...', errfilename
                continue
        newsh = open('jobs/'+job+'.sh','w')
        newshstr = shtemplate.replace('ANALYZER',analyzer).replace('FNAMEKEYWORD',fname).replace('FOUT',foutname)
        newsh.write(newshstr)
        newsh.close()
        if not os.path.exists('output/'+fnamekeyword.replace(' ','')): 
            os.system('mkdir output/'+fnamekeyword.replace(' ',''))
        os.chdir('output/'+fnamekeyword.replace(' ',''))
        cmd =  'condor_submit '+'../../jobs/'+job+'.jdl'        
        print cmd
        if not istest: os.system(cmd)
        counter+=1
        os.chdir('../../')
        

    print 'counter', counter
jdltemplate = '''
universe = vanilla
Executable = CWD/jobs/JOBKEY.sh
Output = CWD/jobs/JOBKEY.out
Error = CWD/jobs/JOBKEY.err
Log = CWD/jobs/JOBKEY.log
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files=CWD/tools, CWD/filelists
x509userproxy = $ENV(X509_USER_PROXY)
Queue 1
'''

shtemplate = '''#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc820
echo $PWD
ls
scram project CMSSW_10_2_21
cd CMSSW_10_2_21/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}
echo $PWD
export x509userproxy=/uscms/home/mjoyce/x509up_u51387
ls
echo python ANALYZER FNAMEKEYWORD
python ANALYZER FNAMEKEYWORD

for f in *.root
do 
   xrdcp -f "$f" root://cmseos.fnal.gov//store/user/lpcsusyphotons/TreeMakerRandS_mvaprep/FOUT
done
rm *.root
'''

main()
print 'done'
##   xrdcp "$f" root://cmseos.fnal.gov//store/user/lpcsusyphotons/TreeMakerRandS_v2/
##TreeMakerRandS/
