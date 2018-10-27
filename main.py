from enum import Enum
from abc import ABCMeta, abstractmethod
import string

fws = "blue"
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
class ColorStrategy:
    def __init__(self,color):
        self.color = color
    @abstractmethod
    def open(self,color):
        raise NotImplementedError
    @abstractmethod
    def close(self,color):
        raise NotImplementedError
class HtmlColorStrategy(ColorStrategy):
    def __init__(self,color):
        super().__init__(color)
    def open(self):
        return "<font color=\"%s\">" % self.color
    def close(self):
        return "</font>"
class AnsiColorStrategy(ColorStrategy):
    def __init__(self,color):
        super()
    def open(self):
        return ""
    def close(self):
        return ""

def FSMAssembly(buffer, state):
    result = []
    state = States.S_LSTART
    states = {States.S_LSTART : StartState, States.S_TEXT : TextState,States.S_COMMENT : CommentState,States.S_CONST : ConstState,States.S_BLACK : BlackState,
              States.S_STRING: StringState,States.S_POINTER : PointerState,States.S_CCHANGE : CCHangeState,States.S_LABEL : LabelState
              }
    while(len(buffer)):
        state = states[state](buffer,result)
    return result
def StartState(buffer,result):
    c = HtmlColorStrategy("black")
    global fws
    fws = "blue"
    result += list("</br>")
    result += list(c.open())
    while len(buffer):
        temp = buffer[0]
        if (temp not in " \t"):
            break
        result.append(buffer[0])
        buffer.pop(0)
    result += list(c.close())
    state = States.S_TEXT
    return state
def TextState(buffer,result):
    c = HtmlColorStrategy(fws)
    result += list(c.open())
    char = buffer[0]
    state = States.S_TEXT
    if (char == ';'):
        state = States.S_COMMENT
        result += list(c.close())
        return state
    if (char in string.digits):
        result += list(c.close())
        state = States.S_CONST
        return state
    if (char in "[,]+-"):
        state = States.S_BLACK
        result += list(c.close())
        return state
    if (char == "\"" or char == '\''):
        result += list(c.close())
        state = States.S_STRING
        return state
    if (char in string.ascii_uppercase):
        result += list(c.close())
        state = States.S_POINTER
        return state
    if (char == "\n"):
        state = States.S_LSTART
    if (char in " \t"):
        state = States.S_CCHANGE
    if (lineContains(buffer, ':')):
        state = States.S_LABEL
        result += list(c.close())
        return state
    result.append(buffer[0])
    buffer.pop(0)
    return state

def CommentState(buffer,result):
    c = HtmlColorStrategy("green")
    result += list(c.open())
    while (len(buffer)):
        temp = buffer[0]
        result.append(buffer[0])
        buffer.pop(0)
        if (temp == '\n'):
            break
    result += list(c.close())
    return States.S_LSTART
def ConstState(buffer,result):
    c = HtmlColorStrategy("gray")
    result += list(c.open())
    while (len(buffer)):
        temp = buffer[0]
        if (temp not in string.hexdigits + "xX"):
            break
        result.append(buffer[0])
        buffer.pop(0)
    result += list(c.close())
    return States.S_TEXT
def BlackState(buffer,result):
    c = HtmlColorStrategy("black")
    result += list(c.open())
    result.append(buffer[0])
    buffer.pop(0)
    result += list(c.close())
    return States.S_TEXT
def StringState(buffer,result):
    c = HtmlColorStrategy("red")
    result += list(c.open())
    second = 0
    while (len(buffer)):
        temp = buffer[0]
        result.append(buffer[0])
        buffer.pop(0)
        if (temp in '\"\'' and second):
            break
        if (temp in '\"\''):
            second = 1
    result += list(c.close())
    return States.S_TEXT
def PointerState(buffer,result):
    c = HtmlColorStrategy("gray")
    result += list(c.open())
    while (len(buffer)):
        temp = buffer[0]
        result.append(buffer[0])
        buffer.pop(0)
        if (temp not in string.ascii_uppercase):
            break
    result += list(c.close())
    return States.S_TEXT

def CCHangeState(buffer,result):
    while (len(buffer)):
        if (buffer[0] not in " \t"):
            break
        result.append(buffer[0])
        buffer.pop(0)
    global fws
    fws = "bronze"
    return States.S_TEXT
def LabelState(buffer, result):
    c2 = HtmlColorStrategy("orange")
    result += list(c2.open())
    while (len(buffer)):
        temp = buffer[0]
        result.append(buffer[0])
        buffer.pop(0)
        if (temp == ':'):
            break
    state = States.S_TEXT
    result += list(c2.close())
    return state


code = """
global _start

section .data
        ; Align to the nearest 2 byte boundary, must be a power of two
        align 2
        ; String, which is just a collection of bytes, 0xA is newline
        str:     db 'Hello, world!',0xA
        strLen:  equ $-str

section .bss

section .text
        _start:

;
;       op      dst,  src
;
                                ;
                                ; Call write(2) syscall:
                                ;       ssize_t write(int fd, const void *buf, size_t count)
                                ;
        mov     edx, strLen     ; Arg three: the length of the string
        mov     ecx, str        ; Arg two: the address of the string
        mov     ebx, 1          ; Arg one: file descriptor, in this case stdout
        mov     eax, 4          ; Syscall number, in this case the write(2) syscall: 
        int     0x80            ; Interrupt 0x80        

                                ;
                                ; Call exit(3) syscall
                                ;       void exit(int status)
                                ;
        mov     ebx, 0          ; Arg one: the status
        mov     eax, 1          ; Syscall number:
        int     0x80
"""
res = FSMAssembly(list(code),States.S_LSTART)
f = open("dump.html","w")
f.write("".join(res))
