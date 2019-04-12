from sbatch_wrapper import main

    
def fake_call_sbatch(script):
    from collections import namedtuple
    R = namedtuple("R", ['stdout', 'stderr'])
    return R(b"submitted job 12345", b"")


def test_call():
    import tempfile
    with tempfile.NamedTemporaryFile() as f:
        main(['sbatch_wrapper', f.name], call_sbatch=fake_call_sbatch)
