from sbatch_wrapper import main, helper

    
def fake_call_sbatch(script):
    from collections import namedtuple
    R = namedtuple("R", ['stdout', 'stderr'])
    return R(b"submitted job 12345", b"")


def test_call():
    import tempfile
    with tempfile.NamedTemporaryFile() as f:
        main(['sbatch_wrapper', f.name], call_sbatch=fake_call_sbatch)

def test_exclusive_1():
    data = b"""
#SBATCH --exclusive
"""
    import tempfile
    with tempfile.NamedTemporaryFile() as f:
        f.write(data)
        f.flush()
        jid,wall,exclusive = helper(['sbatch_wrapper', f.name], call_sbatch=fake_call_sbatch)
    
    assert jid == '12345'
    assert wall == False
    assert exclusive == True

"""
#SBATCH -n 1
mpi_run --exclusive
"""



