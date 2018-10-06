import projectq.setups.ibm
from projectq.ops import H, NOT, Measure
from projectq import MainEngine
from projectq.backends import IBMBackend

def f(eng,x): #sempre retorna 1
    y=eng.allocate_qubit()
    NOT | y
    return y

eng=MainEngine()#IBMBackend(True))
s=eng.allocate_qubit()
t=eng.allocate_qubit()
H | s
t=f(eng,s)
H | s
Measure | s
#Measure | t #Nao necessario
eng.flush()
print "Periodo s = ",int(s)
