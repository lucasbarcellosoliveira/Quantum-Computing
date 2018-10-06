import projectq.setups.ibm
from projectq.ops import All, H, NOT, CNOT, Measure
from projectq import MainEngine
from projectq.backends import IBMBackend

def f(eng,x):
    y=eng.allocate_qubit()
    NOT | y
    return y

eng=MainEngine()#IBMBackend(True))
x=eng.allocate_qureg(2)
NOT | x[1]
All(H) | x
CNOT | (f(eng,x[0]),x[1]) #CNOT | (x[0],x[1]) emula funcao nao uniforme (ou ZERO-CNOT/CNOT+NOT)
All(H) | x
Measure | x
eng.flush()
if int(x[0]):
    print "Funcao NAO uniforme!"
else:
    print "Funcao uniforme!"

#Referencia para tabela-verdade: http://qudev.ethz.ch/content/courses/QSIT06/pdfs/Gulde03.pdf
