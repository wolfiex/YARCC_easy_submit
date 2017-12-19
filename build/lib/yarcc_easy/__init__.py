import glob,sys,os,re
from argparse import ArgumentParser


'''

A submission program for YARCC

Queue data 
its-48hour	48 hours	69	1462	16/20/24/28 - 64/128/256/512GB
64/128its-7day	7 days	10	180	16/20 - 64/128GB
its-14day	14 days	8	112	16/20 - 64/128GB
its-nvidia-k20	48 hours & 7 days	2	34	10/24 - 64GB
its-nvidia-k40	48 hours & 7 days	2	20	10 - 64GB
its-nvidia-k80	48 hours	1	10	10 - 128GB


'''



print 'remember to run "module load sge" before attempting to submit scripts\n\n'

usr = os.popen('whoami').read().strip()



parser = ArgumentParser(description=u'\u001b[34m The lazy way to submit scripts \u001b[0m')

# Input

parser.add_argument('--command','-c', type=str, default=False ,  help='Command used to run script\n')


parser.add_argument('--ncores', '-p', type=int, default=1, help='Number of Cores')

parser.add_argument('--job_variables','-a', type=str,default='', help='Additional job variables, eg. GC_RUNDIR="/scratch/....\n')

parser.add_argument('--name','-n', type=str, default=usr+' yarcc_easy_submit' ,  help='What you wish to call your job name\n')

parser.add_argument('--email','-l', action='store_true',default=False, help='Email me at start and end\n')

parser.add_argument('--distributed', action='store_true',default=False, help='Email me at start and end\n')

parser.add_argument('--mem', '-m', type=int, default=0, help='Memory in GB')

parser.add_argument('--time','-t', type=str, default='01:00:00' ,  help='wall time hh:mm:ss\n')


parser.add_argument('--output_dir','-o', type=str, default='./YARCC_Outputs' ,  help='Output directory\n')

parser.add_argument('--error_dir','-e', type=str, default='./YARCC_Outputs' ,  help='Error directory\n')

parser.add_argument('--source','-s', type=str, default='' ,  help='Source a file before run\n')




parser.add_argument('--run','-r', action='store_true',default=False,  help='Submit Script\n')

parser.add_argument('--runfile','-f', type=str, default=False ,  help='Custom file for Submit Script\n')

parser.add_argument('--delete','-d', action='store_true',default=False, help='Remove running jobs\n')

parser.add_argument('--watch','-w', action='store_true',default=False, help='View running jobs\n')

parser.add_argument('--checkall', action='store_true',default=False, help='Check submitted jobs\n')









args = parser.parse_args()

#args.perplexity

if args.command :    

    
    print u'\u001b[34m Preparing submission script \u001b[0m'

    string = '#!/usr/bin/bash\n'
    
    string += '### Genearated using https://github.com/wolfiex/YARCC_easy_submit.git ####\n'
    
    string +=  '#$ %s\n'%args.job_variables
    
    string +=  '#$ -cwd -V \n'
    
    string +=  '#$ -l h_rt=%s\n'%args.time
    
    
    if args.ncores>1:
    
        if args.distributed:
            string +=  '#$ -pe ib %d\n'%args.job_variables
        else:
            string +=  '#$ -pe smp %d\n'%args.job_variables
            
            
    if float(args.mem)/args.ncores < args.ncores:
        string +=  '#$ -l h_vmem=%sG\n'%1
    else:
        string +=  '#$ -l h_vmem=%sG\n'%float(args.mem)/args.ncores
    
    if args.email:
        string +=  '#$ -m be\n'
        string +=  '#$ -M %s"york.ac.uk\n'%usr
        
    #string +=  '#$ %s\n'%args.job_variables
    
    if not os.path.dirname(args.output_dir):
        os.makedirs(args.output_dir)
    string +=  '#$ -o %s\n'%args.output_dir
    
    if not os.path.exists(args.error_dir):
        os.makedirs(args.error_dir)
    string +=  '#$ -e %s\n'%args.error_dir
    
    if args.source != '':
        string +=  'source %s\n'%args.source
        
    string += '%s \n'%args.command 
    
    with open('./yarcc.job','w') as f:
        f.write(string)
    
    

if args.run:
    print u'\u001b[34m Submiting Job \u001b[0m'

    if args.runfile:
        runfile = args.runfile
    else:
        runfile = 'yarcc.job'
        
    if not os.path.exists(runfile):
        print u'\u001b[31m No file found to run: \u001b[0m ' + runfile
    else: 
        newfile = os.popen('qsub %s'%runfile).read()
        newid = newfile.split(' ')[2]
        validity = os.popen('qalter -w p %s'%newid).read()
        print validity
        if 'no suitable queues' in validity:
              print u'\u001b[34m\nNo queues: Terminating %s\n\u001b[0m'%newid
              os.system('qdel %s'%newid)
        
        
    
    
        
        
        
        
        
if args.watch:
    os.system('watch qstat -u %s'%usr)
    
    
if args.checkall:
    runs = os.popen('qstat -u %s'%usr).read()
    runs = re.findall(r'(\b\d+[\w\. A-z/]+[\d:]+\b)',runs) 
    print u'\u001b[34m\n Checking all runs:\n\u001b[0m'
    
    for k in runs:
        k = k.split(' ')
        print ' '.join(k[:4])+' - '+ str(os.popen('qalter -w p %s'%k[0]).read())
    
    
if args.delete:
    runs = os.popen('qstat -u %s'%usr).read()
    #runlist = re.findall(r'(\b\d+[\w\s\. \W]+[\t\s ]+\d+/\d+/\d+[\t\s ]\d+:\d+:\d+)',runs)
    runs = re.findall(r'(\b\d+[\w\. A-z/]+[\d:]+\b)',runs)
    print u'\u001b[34m\n Select runs to delete (space separated):\n\u001b[0m'
    if len(runs)>1:
    
        print '   a - Delete all' 
        
        for i,j in enumerate(runs):
            print '%4d - %s'%(i,j)
    
        s = raw_input(u'\u001b[35mMake selection here: \n\u001b[0m')
        
        for k in s.split(' '):
            if k=='': continue
            if k == 'a': os.system('qdel -u %s'%usr)
            else: 
                k = runs[int(k.replace(' ',''))].split(' ')[0]
                  
            os.system('qdel %s'%k)
            
            
            
sys.exit('Finished fine')

