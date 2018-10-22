from enum import Enum
from string import *

class States(Enum):
    S_START = 0
    S_MNEMO =1
    S_WS1 = 2
    S_OP1 =3
    S_COMMA = 4
    S_OP2 = 5

class ColorStrategy:
    def StartColoring(self,color):
        pass
    def StopColoring(self, color):
        pass
class HtmlColorStrategy(ColorStrategy):
    def StartColoring(self,color):
        pass
    def StopColoring(self, color):
        pass

def FSMAssembly(buffer, colorStrategy):
    state = States.S_START
    mnemo = []
    operand1 = []
    operand2 = []
    while(len(buffer)):
        char = buffer[0]
        buffer = buffer[1:]
        if(state == States.S_START):
            if(char in whitespace):
                continue
            state = States.S_MNEMO
            #Fallthrough
        if(state == States.S_MNEMO):
            if(char not in whitespace):
                mnemo.append(char)
                continue
            state = States.S_WS1
            #Fallthrough
        if(state == States.S_WS1):
            if(char in whitespace):
                continue
            state = States.S_OP1
            #Fallthrough
        if(state == States.S_OP1):
            if(char != ","):
                operand1.append(char)
                continue
            state = States.S_COMMA
            #Fallthrough
        if(state == States.S_COMMA):
            if(char in ','+whitespace):
                continue
            state = States.S_OP2
            #Fallthrough
        if(state == States.S_OP2):
            if(char not in whitespace):
                operand2.append(char)
                continue
            state = States.S_START
    print(''.join(mnemo))
    print(''.join(operand1))
    print(''.join(operand2))
FSMAssembly("")
