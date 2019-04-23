"""Wrapper for sbatch used by the merced cluster to lint submitted scripts """

__version__ = "0.0.1"

import sys
import subprocess

SBATCH = "/act/slurm/bin/sbatch"


def call_sbatch(args):

    return subprocess.run(
        [SBATCH] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


def helper(argv, *, call_sbatch=call_sbatch):
    sub_script = []
    if argv:
        sub_script = argv[1:]

    result = call_sbatch(sub_script)

    if '--debug' in argv:
        def debug(*args, **kwargs):
            print(*args, **kwargs)
        debug('debug log enabled')
    else:
        def debug(*args, **kwargs):
            pass

    try:
        used_wallclock = False
        used_exclusive = False
        if not sub_script:
            debug('no subscript')
            sys.exit(sub_script)
        with open(sub_script[0]) as f:
            for l in f.readlines():
                debug('testing line', l)
                if not l.startswith("#SBATCH"):
                    debug('skipping')
                    continue
                if "--exclusive" in l:
                    debug('found exclusive')
                    used_exclusive = True
                if "-t" in l:
                    debug('found wallclock')
                    used_wallclock = True
                    # To-do: If user doesn't request for all the cores on the node on full.q, do not let them submit the job
                # if "full.q" in l:
                #     print(
                #         "You are submitting your job to full.q without requesting for full node. Please use this flag IF and ONLY IF you are using all the cores on the node"
                #     )
    except Exception as e:
        with open("/var/log/sbatch-tracebacks.log", "a") as f:
            f.write(str(e))
    stdout = result.stdout.decode()
    print(stdout, end="")
    print(result.stderr.decode(), end="", file=sys.stderr)

    jid = stdout.split(" ")[-1].strip()
    debug(jid, used_wallclock, used_exclusive)
    return jid, used_wallclock, used_exclusive


def main(argv, *, call_sbatch=call_sbatch):

    jid, used_wallclock, used_exclusive = helper(argv, call_sbatch=call_sbatch)
    if used_exclusive:
        try:
            with open("/var/log/sbatch.log", "a") as f:
                import json
                f.write(json.dumps({"job_id": jid, 
                                    "exclusive" :True}))
        except:
            pass
        print(
            "WARNING: You are using --exclusive flag in your submission file. This blocks other users from running jobs on the same node as your job. Please use this flag IF and ONLY IF you are absolutely sure you need an entire node"
        )
    if used_wallclock == False:
        print(
            "You have not specified a wall-clock limit for your job to run. Please specify wall-clock time for scheduler to schedule your jobs more efficiently. You can specify a wall-clock time by adding this line in your submission script '--time=days-hours:minutes:seconds'", 
        file=sys.stderr)


def entrypoint():
    return main(sys.argv)


if __name__ == "__main__":
    main(sys.argv)
