"""Wrapper for sbatch used by the merced cluster to lint submitted scripts """

__version__ = '0.0.1'

import sys
import subprocess


def call_sbatch(args):
    return subprocess.run(['sbatch',argv[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main(call_sbatch=call_sbatch):
    sub_script = sys.argv[1:]
    result = call_sbatch(argv[1])
    print ("Result: ",result)
    used_wallclock = False
    used_exclusive = False
    with open(subscripts) as f:
        for l in f.readlines():
            if not l.startswith('#SBATCH'):
                continue
            if ('--exclusive' in l):
                used_exclusive = True
            if ('-t' in l):
                used_wallclock = True
                #To-do: If user doesn't request for all the cores on the node on full.q, do not let them submit the job
            if ('full.q' in l):
                    print("You are submitting your job to full.q without requesting for full node. Please use this flag IF and ONLY IF you are using all the cores on the node")

    jid = result.stdout.decode().split(' ')[-1].strip()

    if used_exclusive:
        with open('exclusive_jobs', 'a') as f:
            f.write('Job' +str(jid) +'was submitted with exclusive')
        print("WARNING: You are using --exclusive flag in your submission file. This blocks other users from running jobs on the same node as your job. Please use this flag IF and ONLY IF you are absolutely sure you need an entire node")
    if used_wallclock == False:
        print ("You have not specified a wall-clock limit for your job to run. Please specify wall-clock time for scheduler to schedule your jobs more efficiently")



if __name__ == '__main__':
    main()
