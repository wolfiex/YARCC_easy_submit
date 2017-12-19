# YARCC_easy_submit
### An easy submission script for YARCC programs.
It automatically:

* checks if a submission may be accepted in a queue upon submission
* easily creates a jobfile and submits this
* allows simple delettion of jobs. 

Run with  `python -m yarcc_easy <args>`. the `-m` loads the module.




#### For shortcuts we may add aliases to our .bashrc/.profile
```
alias psub='python -m yarcc_easy'

```This means we can run  "python -m yarcc_easy --help" as:```

psub --help

```




#### Allowed arguments may be viewed using 

```
python -m yarcc_easy --help

remember to run "module load sge" before attempting to submit scripts


usage: -c [-h] [--command COMMAND] [--ncores NCORES]
          [--job_variables JOB_VARIABLES] [--name NAME] [--email]
          [--distributed] [--mem MEM] [--time TIME] [--output_dir OUTPUT_DIR]
          [--error_dir ERROR_DIR] [--source SOURCE] [--run]
          [--runfile RUNFILE] [--delete] [--watch] [--checkall]

 The lazy way to submit scripts 

optional arguments:
  -h, --help            show this help message and exit
  --command COMMAND, -c COMMAND
                        Command used to run script
  --ncores NCORES, -p NCORES
                        Number of Cores
  --job_variables JOB_VARIABLES, -a JOB_VARIABLES
                        Additional job variables, eg. GC_RUNDIR="/scratch/....
  --name NAME, -n NAME  What you wish to call your job name
  --email, -l           Email me at start and end
  --distributed         Email me at start and end
  --mem MEM, -m MEM     Memory in GB
  --time TIME, -t TIME  wall time hh:mm:ss
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory
  --error_dir ERROR_DIR, -e ERROR_DIR
                        Error directory
  --source SOURCE, -s SOURCE
                        Source a file before run
  --run, -r             Submit Script
  --runfile RUNFILE, -f RUNFILE
                        Custom file for Submit Script
  --delete, -d          Remove running jobs
  --watch, -w           View running jobs
  --checkall            Check submitted jobs

```

#### To submit a job
```
python -m yarcc_easy --ncores 2 --email --mem 11 --run --command '<method to run file here eg. python file.py>'

```


#### To check all jobs§
```
python -m yarcc_easy --checkall

```


#### To watch jobs§
```
python -m yarcc_easy --watch

```


#### To delete a Job
```
python -m yarcc_easy -d


Select runs to delete (space separated):

   a - Delete all
   0 - 1548098 0.00000 yarcc.job  usr123        qw    12/18/2017 22:57:53
   1 - 1548100 0.00000 yarcc.job  usr123        qw    12/18/2017 22:57:57
   2 - 1548101 0.00000 yarcc.job  usr123        qw    12/18/2017 22:58:35
   3 - 1548102 0.00000 yarcc.job  usr123        qw    12/18/2017 22:59:26
   4 - 1548103 0.00000 yarcc.job  usr123        qw    12/18/2017 23:00:27
   5 - 1548104 0.00000 yarcc.job  usr123        qw    12/18/2017 23:00:54
   
```


