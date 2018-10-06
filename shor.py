from random import random
from math import ceil,log,pi
from fractions import Fraction,gcd
from projectq import MainEngine
from projectq.libs.math import MultiplyByConstantModN
from projectq.meta import Control
from projectq.ops import X,Measure,H,R

def shor(eng,entrada,inicial):
    n=int(ceil(log(entrada,2)))
    x=eng.allocate_qureg(n)
    X|x[0]
    medidas=[0]*(2*n)
    ctrl=eng.allocate_qubit()
    for i in range(2*n):
        a_novo=pow(2**(2*n-1-i),entrada) #exponenciacao modular em Python
        H|ctrl
        with Control(eng,ctrl):
            MultiplyByConstantModN(a_novo,entrada)|x #exponenciacao modular quantica
        for j in range(i):
            if medidas[j]:
                R(-pi/(2**(i-j)))|ctrl #transformada de Fourier quantica
        H|ctrl
        Measure|ctrl
        eng.flush()
        if medidas[i]:
            X|ctrl
    Measure|x
    y=sum([(medidas[2*n-1-j]*1./(2**(j+1))) for j in range(2*n)])
    s=Fraction(y).limit_denominator(entrada-1).denominator
    return s

eng=MainEngine()
entrada=int(input('Numero a fatorar: '))
inicial=int(random()*entrada)
if gcd(inicial,entrada)!=1:
    print("Fator encontrado por acaso: ",gcd(inicial,entrada))
    print("Outro fator: ",int(entrada/gcd(inicial,entrada)))
else:
    s=shor(eng,entrada,inicial) #obtem periodo provavel
    if s%2!=0:
        s*=2
    exponenciacao=pow(inicial,int(s/2),entrada) #exponenciacao modular em Python
    f1=gcd(exponenciacao+1,entrada)
    f2=gcd(exponenciacao-1,entrada)
    if f1*f2!=entrada and f1*f2>1 and int(1.*entrada/(f1*f2))*f1*f2==entrada:
        f1=f1*f2
        f2=int(entrada/(f1*f2))
    print("Fatores encontrados: ",f1,f2)
    if f1*f2!=entrada or f1<=1 or f2<=1:
        print("Sem convergencia")
