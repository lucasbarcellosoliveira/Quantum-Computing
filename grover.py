import projectq.setups.ibm
from projectq.ops import All, H, Z, NOT, Measure
from projectq import MainEngine
from projectq.backends import IBMBackend
from projectq.meta import Loop, Control, Compute, Uncompute
from math import sqrt

def oraculo(eng,x,ctrl):
    with Compute(eng):
        All(NOT) | x[1::2]
    with Control(eng, x):
        NOT | ctrl
    Uncompute(eng)
    return

n=4 #numero de bits da estrutura a ser buscada
eng=MainEngine()#IBMBackend(True))
x=eng.allocate_qureg(n)
All(H) | x
ctrl=eng.allocate_qubit()
NOT | ctrl
H | ctrl
with Loop(eng,int(sqrt(2**n))): #ou for?
    oraculo(eng,x,ctrl)
    with Compute(eng):
        All(H) | x
        All(NOT) | x
    with Control(eng, x[0:-1]):
        Z | x[-1]
    Uncompute(eng)
Measure | x
eng.flush()
print "Posicao encontrada:"
for i in range(n):
    print int(x[i]),
