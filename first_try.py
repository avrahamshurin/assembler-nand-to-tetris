def dec_to_bin(x):
    return str(bin(int(x))[2:])


def padding(x):
    a = ""
    while len(a + x)<16:
        a = a + "0"
    return a + x

c_table ={"0":"0101010", "1":"0111111", "-1":"0111010", "D":"0001100", "A":"0110000",
          "!D":"0001101", "!A":"0110001", "-D":"0001111", "-A":"0110011", "D+1":"0011111",
          "A+1":"0110111", "D-1":"0001110", "A-1":"0110010", "D+A":"0000010", "D-A":"0010011",
          "A-D":"0000111", "D&A":"0000000", "D|A":"0010101", "M":"1110000", "!M":"1110001",
          "-M":"1110011", "M+1":"1110111","M-1":"1110010", "D+M":"1000010", "D-M":"1010011",
          "M-D":"1000111", "D&M":"1000000","D|M":"1010101"}

d_table = {"":"000","M":"001","D":"010","MD":"011","A":"100", "AM":"101", "AD":"110", "AMD":"111"}
j_table = {"":"000","JGT":"001","JEQ":"010","JGE":"011","JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111"}

symbol_table = {"SP": "0", "LCL":"1", "ARG":"2", "THIS":"3", "THAT":"4", "R0":"0",
                "R1": "1","R2":"2","R3":"3","R4":"4","R5":"5","R6":"6","R7":"7","R8":"8","R9":"9",
                "R10": "10","R11":"11","R12":"12","R13":"13","R14":"14","R15":"15", "SCREEN":"16384","KBD":"24576"}


with open("source.txt", "r") as open_file:      # first read- adding symbols
    address = 0
    line = open_file.readline()

    while line:
        stripped_line = line.replace(" ", "").split("//")[0].strip("\n")
        if "(" in stripped_line:
            sym = stripped_line.strip("(").strip(")")
            if sym not in symbol_table:
                symbol_table[sym] = str(address)
        elif stripped_line != "":
            address += 1

        line = open_file.readline()



with open("source.txt","r") as open_file:

    new_file = open("target.txt", "w+")
    line = open_file.readline()
    var_address = 16
    while line:
        stripped_line = line.replace(" ","").split("//")[0].strip("\n")  # remove whitespace and comments
        if "@" in stripped_line:                           # check for A instruction
            arg = stripped_line.split("@")[1]
            if arg[0]>="0" and arg[0]<="9":    #arg is a number, not a variable
                final_arg = arg
            else:
                if arg in symbol_table:
                    final_arg = symbol_table[arg]
                else:
                    final_arg = str(var_address)
                    symbol_table[arg] = str(var_address)
                    var_address +=1

            a_instruction = padding("0" + dec_to_bin(final_arg))  # convert to binary and add padding
            new_file.write(a_instruction)
            new_file.write("\n")
        elif stripped_line != "" and "(" not in stripped_line:                                             # check for C instruction

            if "=" in stripped_line:
                dst = stripped_line.split("=")[0]
                cmp = stripped_line.split("=")[1].split(";")[0]
            else:
                dst = ""
                cmp = stripped_line.split(";")[0]

            if ";" in stripped_line:
                jmp = stripped_line.split(";")[1]
            else:
                jmp = ""

            c_instruction = "111" + c_table[cmp] + d_table[dst] + j_table[jmp]
            new_file.write(c_instruction)
            new_file.write("\n")




        line = open_file.readline()

    new_file.close()


