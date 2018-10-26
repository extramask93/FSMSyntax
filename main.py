from enum import Enum
import string
def lineContains(buffer,char):
    for c in buffer:
        if(c == '\n' or c==';' or c=='\"'):
            return False
        if(c == char):
            return True

class States(Enum):
    S_LSTART = 1
    S_TEXT = 2
    S_COMMENT = 3
    S_CONST = 4
    S_BLACK = 5
    S_STRING = 6
    S_POINTER = 7
    S_CCHANGE = 8
    S_LABEL = 9
class Color:
    def __init__(self,color):
        self.color = color
    def open(self):
        return "<font color=\"%s\">" % self.color
    def close(self):
        return "</font>"
def FSMAssembly(buffer, state):
    result = ""
    fws ="blue"
    while(len(buffer)):
        if(state == States.S_LSTART):
            c = Color("black")
            fws = "blue"
            result += "</br>"
            result += c.open()
            while len(buffer):
                temp = buffer[0]
                if(temp not in " \t"):
                    break
                result += buffer[0]
                buffer = buffer[1:]
            result += c.close()
            state = States.S_TEXT
        if(state == States.S_TEXT):
            c = Color(fws)
            result += c.open()
            char = buffer[0]
            if(char == ';'):
                state = States.S_COMMENT
                result += c.close()
                continue
            if(char in string.digits):
                result += c.close()
                state = States.S_CONST
                continue
            if(char in "[,]+-"):
                state = States.S_BLACK
                result += c.close()
                continue
            if(char == "\""):
                result += c.close()
                state = States.S_STRING
                continue
            if(char in string.ascii_uppercase):
                result += c.close()
                state = States.S_POINTER
                continue
            if(char  == "\n"):
                state = States.S_LSTART
            if(char in " \t"):
                state = States.S_CCHANGE
            if(lineContains(buffer,':')):
                state = States.S_LABEL
                result += c.close()
                continue
            result += buffer[0]
            buffer = buffer[1:]
            #Fallthrough
        if(state == States.S_COMMENT):
            c = Color("green")
            result += c.open()
            while(len(buffer)):
                temp = buffer[0]
                result += buffer[0]
                buffer = buffer[1:]
                if(temp == '\n'):
                    break
            result += c.close()
            state = States.S_LSTART
        if(state == States.S_CONST):
            c = Color("gray")
            result += c.open()
            while(len(buffer)):
                temp = buffer[0]
                if(temp not in string.hexdigits+"xX"):
                    break
                result += buffer[0]
                buffer = buffer[1:]
            result += c.close()
            state = States.S_TEXT
        if(state == States.S_BLACK):
            c = Color("black")
            result += c.open()
            result += buffer[0]
            buffer = buffer[1:]
            result += c.close()
            state = States.S_TEXT
        if(state == States.S_STRING):
            c = Color("red")
            result += c.open()
            second =0
            while(len(buffer)):
                temp = buffer[0]
                result += buffer[0]
                buffer = buffer[1:]
                if(temp == '\"' and second):
                    break
                if(temp == '\"'):
                    second = 1
            result += c.close()
            state = States.S_TEXT
        if(state == States.S_POINTER):
            c = Color("gray")
            result += c.open()
            while(len(buffer)):
                temp = buffer[0]
                result += buffer[0]
                buffer = buffer[1:]
                if(temp not in string.ascii_uppercase):
                    break
            result += c.close()
            state = States.S_TEXT
        if(state == States.S_CCHANGE):
            while(len(buffer)):
                if(buffer[0] not in " \t"):
                    break
                result += buffer[0]
                buffer = buffer[1:]
            fws = "bronze"
            state = States.S_TEXT
        if(state == States.S_LABEL):
            c2 = Color("orange")
            result += c2.open()
            while(len(buffer)):
                temp = buffer[0]
                result += buffer[0]
                buffer = buffer[1:]
                if(temp == ':'):
                    break
            state = States.S_TEXT
            result += c2.close()
    return result
code = """
global main
extern printf

section .data

beer    db      "%d bottles of beer on the wall, %d bottles of beer."
        db      0x0a
        db      "Take one down and pass it around, %d bottles of beer."
        db      0x0a
        db      0

main:
        mov ecx, 99

_loop:
        dec  ecx
        push ecx
        push ecx
        inc  ecx
        push ecx
        push ecx
        push beer
        call printf
        add  esp,16
        pop  ecx
        or   ecx, ecx
        jne  _loop
        xor  eax,eax
        ret
"""
res = FSMAssembly(code,States.S_LSTART)
f = open("dump.html","w")
f.write(res)
