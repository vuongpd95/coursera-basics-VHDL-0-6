####################################################################################################
## Module: Parser
## Author: Pham Duy Vuong
## Version: 1.0
## Description: break assembly command into underling component
####################################################################################################

INPUT_FILE = "prog.asm"    # name of the input file
OUTPUT_FILE = "prog.hack"  # name of the output file

# declare variable
class myclass:
    currentCommand = None   # is a string, contains current command
    currentLineNumber = 0   # is a number which is line number of current line in file (index of the pass)
    # initial symbol table
    symTable = {'SP':0,
                'LCL':1,
                'ARG':2,
                'THIS':3,
                'THAT':4,
                'R0':0, 'R3':3, 'R6':6, 'R9':9, 'R12':12,
                'R1':1, 'R4':4, 'R7':7, 'R10':10, 'R13':13,
                'R2':2, 'R5':5, 'R8':8, 'R11':11, 'R14':14, 'R15':15,
                'SCREEN':16384,
                'KBD':24576
                }
    fstIndex = 0            # index of the first pass A,C_COMMAND count
    RamAddress = 16         # next avaiable RAM address to store variable
v = myclass()               # static Variable
# get file info
inFile = open(INPUT_FILE,'r')       
lines = inFile.read().splitlines()  # list of lines in the file
numberOfLine = len(lines)           # number of line in th list
inFile.close()

## Function Return to first line of the file

def reset():
    v.currentLineNumber = 0         # reset to go through the file again

## Routine name: hasMoreCommands
## Arguments: None
## Returns: Boolean
## Function: Are there more command in the input?

def hasMoreCommands():
    for i in range(v.currentLineNumber, numberOfLine):
        checkingLine = lines[i].replace(" ", "")        # clear whitespace
        if len(checkingLine) >= 2:
            if checkingLine[0:2] != '//': return True   # check if it's a comment line
    return False

## Routine name: advance
## Arguments: None
## Returns: None
## Function: Read the next command from the input and makes it the current command should be
##           called only if hasMoreCommands() is true. Intially there is no current command

def advance():
    while True:
        checkingLine = lines[v.currentLineNumber].replace(" ", "")                  # clear the whitespace
        if len(checkingLine) >= 2:
            if checkingLine[0:2] != '//':                                           # go inside if it's not a comment line
                for i in range(0, len(checkingLine)-1):                             # search for the entry of comment parts
                    if checkingLine[i:i+2] == '//':
                        checkingLine = checkingLine.replace(checkingLine[i:], "")   # clear the command parts
                        break
                v.currentCommand = checkingLine                                     # store the complete command line to v.currentCommand
                v.currentLineNumber = v.currentLineNumber + 1                       # go to the next line of the file
                break            
        v.currentLineNumber = v.currentLineNumber + 1

## Routine name: commandType
## Arguments: None
## Returns: A/C/L_COMMAND
## Function: Return the type of the current command

def commandType():
    if v.currentCommand[0] == '@': return 'A_COMMAND'
    else:
        if v.currentCommand[0] == '(': return 'L_COMMAND'
        else: return 'C_COMMAND'

## Routine name: symbol
## Arguments: None
## Returns: string
## Function: return the symbol or decimal Xxx of the A_COMMAND(@Xxx) or C_COMMAND((Xxx))
##           should be called only when command type is A or C

def symbol():
    array = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    flag = "s"                                                      # "s" stands for symbol, "n" stands for number
    count = 0
    if commandType() == 'A_COMMAND':
        for i in range(1, len(v.currentCommand)):
            for j in range (0, len(array)):
                if v.currentCommand[i] == array[j]:
                    count = count + 1
                    break
            if count == len(v.currentCommand)-1: flag = "n"         # if every character of the command presents a number,
                                                                    # flag = "n"
        if flag == "n":                                             
            num = bin(int(v.currentCommand[1:]))[2:]                # make received decimal become 16bits
            for i in range (0, 16-len(num)):                        #
                num = "0" + num                                     # return flag to use for other operation
            return flag + num
        else:
            return flag + v.currentCommand[1:]                      # return flag = "s" and the symbol
    if commandType() == 'L_COMMAND': return v.currentCommand[1:-1]

####################################################################################################
## Module: Code 
## Author: Pham Duy Vuong
## Version: v1.0
## Description: Contains fuction return code string
####################################################################################################

## Routine name: dest
## Arguments: None
## Returns: string
## Function: Return the dest mnemonic in the current C_COMMAND
##           Should be called only when commandType() is C_COMMAND

def dest(): 
    clength = len(v.currentCommand)
    count = 0
    result = None
    while count<clength:
        if v.currentCommand[count] == "=":
            break
        count = count + 1                                   # count is the position of "=" in the currentCommand    
    if count == 1:                                          # count also equals the number of charater stands before "="
        if v.currentCommand[0] == "M": result = "001"       # use count = 1, 2, 3 to prevent mistaken between "M" and "MD"
        elif v.currentCommand[0] == "D": result = "010"     # "A" and "AM" and "AMD" ...
        elif v.currentCommand[0] == "A": result = "100"
    elif count == 2:
        if v.currentCommand[0:2] == "MD": result = "011"
        elif v.currentCommand[0:2] == "AM": result = "101"
        elif v.currentCommand[0:2] == "AD": result = "110"
    elif count == 3:
        if v.currentCommand[0:3] == "AMD": result = "111"
    else: result = "000"
    return result

## Routine name: comp
## Arguments: None
## Returns: string
## Function: Return the comp mnemonic in the current C_COMMAND
##           Should be called only when commandType() is C_COMMAND

def comp():
    destFlag = True                         # = true means dest = empty                                                         
    jumpFlag = True                         # = true means jump = empty
    index = 0
    clength = len(v.currentCommand)
    while index<clength:
        if v.currentCommand[index] == "=":  # check if the command contains "=" or ";"
            destFlag = False                # if it contains "=" then dest is not empty, jump is empty
            break                           # if it contains ";" then dest is empty, jump is not empty
        if v.currentCommand[index] == ";":
            jumpFlag = False
            break
        index = index + 1

    if jumpFlag and ~destFlag:              
        compl = clength - index - 1         # if dest is not empty, comp-part depends on characters standing behind "="
        if compl == 1:
            if v.currentCommand[index+1:] == "0": return "0101010"
            if v.currentCommand[index+1:] == "1": return "0111111"
            if v.currentCommand[index+1:] == "D": return "0001100"
            if v.currentCommand[index+1:] == "A": return "0110000"
            if v.currentCommand[index+1:] == "M": return "1110000"
        if compl == 2:
            if v.currentCommand[index+1:] == "-1": return "0111010"
            if v.currentCommand[index+1:] == "!D": return "0001101"
            if v.currentCommand[index+1:] == "!A": return "0110001"
            if v.currentCommand[index+1:] == "-D": return "0001111"
            if v.currentCommand[index+1:] == "-A": return "0110011"
            if v.currentCommand[index+1:] == "!M": return "1110001"
            if v.currentCommand[index+1:] == "-M": return "1110011"
        if compl == 3:
            if v.currentCommand[index+1:] == "D+1" or v.currentCommand[index+1:] == "1+D": return "0011111"
            if v.currentCommand[index+1:] == "1+A" or v.currentCommand[index+1:] == "A+1": return "0110111"
            if v.currentCommand[index+1:] == "D-1": return "0001110"
            if v.currentCommand[index+1:] == "A-1": return "0110010"
            if v.currentCommand[index+1:] == "D+A" or v.currentCommand[index+1:] == "A+D": return "0000010"
            if v.currentCommand[index+1:] == "D-A": return "0010011"
            if v.currentCommand[index+1:] == "A-D": return "0000111"
            if v.currentCommand[index+1:] == "D&A" or v.currentCommand[index+1:] == "A&D": return "0000000"
            if v.currentCommand[index+1:] == "D|A" or v.currentCommand[index+1:] == "A|D": return "0010101"
            if v.currentCommand[index+1:] == "M+1" or v.currentCommand[index+1:] == "1+M": return "1110111"
            if v.currentCommand[index+1:] == "M-1": return "1110010"
            if v.currentCommand[index+1:] == "M+D" or v.currentCommand[index+1:] == "D+M": return "1000010"
            if v.currentCommand[index+1:] == "D-M": return "1010011"
            if v.currentCommand[index+1:] == "M-D": return "1000111"
            if v.currentCommand[index+1:] == "M&D" or v.currentCommand[index+1:] == "D&M": return "1000000"
            if v.currentCommand[index+1:] == "M|D" or v.currentCommand[index+1:] == "D|M": return "1010101"
    if ~jumpFlag and destFlag:
        compl = index                   # if jump is not empty, comp-part depends on characters standing before ";"
        if compl == 1:
            if v.currentCommand[:index] == "0": return "0101010"
            if v.currentCommand[:index] == "1": return "1111111"
            if v.currentCommand[:index] == "D": return "0001100"
            if v.currentCommand[:index] == "A": return "0110000"
            if v.currentCommand[:index] == "M": return "1110000"
        if compl == 2:
            if v.currentCommand[:index] == "-1": return "0111010"
            if v.currentCommand[:index] == "!D": return "0001101"
            if v.currentCommand[:index] == "!A": return "0110001"
            if v.currentCommand[:index] == "-D": return "0001111"
            if v.currentCommand[:index] == "-A": return "0110011"
            if v.currentCommand[:index] == "!M": return "1110001"
            if v.currentCommand[:index] == "-M": return "1110011"
        if compl == 3:
            if v.currentCommand[:index] == "D+1" or v.currentCommand[:index] == "1+D": return "0011111"
            if v.currentCommand[:index] == "1+A" or v.currentCommand[:index] == "A+1": return "0110111"
            if v.currentCommand[:index] == "D-1": return "0001110"
            if v.currentCommand[:index] == "A-1": return "0110010"
            if v.currentCommand[:index] == "D+A" or v.currentCommand[:index] == "A+D": return "0000010"
            if v.currentCommand[:index] == "D-A": return "0010011"
            if v.currentCommand[:index] == "A-D": return "0000111"
            if v.currentCommand[:index] == "D&A" or v.currentCommand[:index] == "A&D": return "0000000"
            if v.currentCommand[:index] == "D|A" or v.currentCommand[:index] == "A|D": return "0010101"
            if v.currentCommand[:index] == "M+1" or v.currentCommand[:index] == "1+M": return "1110111"
            if v.currentCommand[:index] == "M-1": return "1110010"
            if v.currentCommand[:index] == "M+D" or v.currentCommand[:index] == "D+M": return "1000010"
            if v.currentCommand[:index] == "D-M": return "1010011"
            if v.currentCommand[:index] == "M-D": return "1000111"
            if v.currentCommand[:index] == "M&D" or v.currentCommand[:index] == "D&M": return "1000000"
            if v.currentCommand[:index] == "M|D" or v.currentCommand[:index] == "D|M": return "1010101"

## Routine name: jump
## Arguments: None
## Returns: string
## Function: Return the jump mnemonic in the current C_COMMAND
##           should be called only commandType() == C_COMMAND

def jump():
    index = 0
    clength = len(v.currentCommand)
    while index<clength:
        if v.currentCommand[index] == ";":
            break
        index = index + 1    
    if index != 0:
        if v.currentCommand[index+1:] == "JGT": return "001"
        if v.currentCommand[index+1:] == "JEQ": return "010"
        if v.currentCommand[index+1:] == "JGE": return "011"
        if v.currentCommand[index+1:] == "JLT": return "100"
        if v.currentCommand[index+1:] == "JNE": return "101"
        if v.currentCommand[index+1:] == "JLE": return "110"
        if v.currentCommand[index+1:] == "JMP": return "111"
        return "000"
    else: return "000"

####################################################################################################
## Module: SymbolTable 
## Author: Pham Duy Vuong
## Version: v1.0
## Description: Contains fuction return symbol tables
####################################################################################################

# update table

def addEntry(symbol, address):
    v.symTable.update({symbol: address})

# check whether table contains symbol

def contains(symbol):
    if symbol in v.symTable:
        return True
    else:
        return False

# return address of the symbol

def GetAddress(symbol):
    return v.symTable[symbol]

# convert base(10) to 16bits
def convertDecimalTo16b(sym):
    symStr = str(sym)
    result = bin(int(symStr))[2:]
    for i in range (0, 16-len(result)):
        result = "0" + result
    return result

# main function #####################################################################################
# ready to write to prog.hack
outFile=open(OUTPUT_FILE, 'w')
# First pass to generate 
while hasMoreCommands():
    advance()
    if commandType() == 'A_COMMAND' or commandType() == 'C_COMMAND': v.fstIndex = v.fstIndex + 1
    if commandType() == 'L_COMMAND':
        if ~contains(symbol()):
            addEntry(symbol(), v.fstIndex)
# reset currentLineNumber to prepare for the next pass
reset()        
# Sencond pass
while hasMoreCommands():
    advance()
    if commandType() != 'C_COMMAND':
        if commandType() == 'A_COMMAND':
            if symbol()[0] == 's':
                sym = symbol()[1:]
                if sym in v.symTable:
                    sym = v.symTable[sym]
                    sym = convertDecimalTo16b(sym)
                    outFile.write(sym + "\n")
                else:
                    addEntry(symbol()[1:], v.RamAddress)
                    sym = convertDecimalTo16b(v.RamAddress)
                    v.RamAddress = v.RamAddress + 1
                    outFile.write(sym + "\n")
            if symbol()[0] == 'n':
                outFile.write(symbol()[1:] + "\n")
    else:
        outFile.write("111" + comp() + dest() + jump() + "\n")
# Close prog.hack
outFile.close()
