from FirstPassUtility import *
from FirstPass import *

base_loc,base_target,final_address = FirstPass("Example_4.txt")

# for i in FirstPass_output:
#     print(i)
objectcode = []
def pad(star,size,char):
    if(size > 0):
        return((size - len(star))*char + star)
    else:
        size = abs(size)
        return(star + (size - len(star))*char)
def format1():
    print("format 1")
def format2(target):
    if(',' in target):
        r1,r2 = target.split(',')
        r1 = registers.get(r1)
        r2 = registers.get(r2)
        return([r1,r2])
    return([registers.get(target),'0'])
    # print("format 2")
def format3(loc_counter,target):
    # "".join(objectcode[-1][1])
    flags,target_address = getFlags(loc_counter,3,target)
    flags = "".join(flags)
    return([flags, target_address])
    #print(hex(opcode)+hex(n,i) b p x e disp     )
def format4(loc_counter,target):
    flags,target_address = getFlags(loc_counter,4,target)
    flags = "".join(flags)
    return([flags, target_address])
    # return(getFlags(loc_counter,4,target))
def format5(loc_counter,target):
    flags,target_address = getFlags(loc_counter,3,target)
    flags = "".join(flags)
    return([flags, target_address])
    # return(getFlags(loc_counter,3,target))
def format6(loc_counter,target):
    flags,target_address = getFlags(loc_counter,4,target)
    flags = "".join(flags)
    return([flags, target_address])
    # return(getFlags(loc_counter,4,target))

def directive():
    return(['0','0','0','0','0'],0)
def getFlags(loc_counter,format,target):     #Immediate “#” i=1, n=0 Value = TA
                                #Indirect “@” i=0, n=1 Value = ((TA))
    n,i,x,b,p,e = '1','1','0','0','0','0'   #simple in sicxe i=1 , n=1 Value = (TA)
    flagzby=0
    if(target == placeholder):
        return([n,i,x,b,p,e],0)
    if('#' in target):
        n,i = '0','1'
        target = target[1:]
        flagzby=1
        # print("It entered" + loc_counter)
        try:
            target_address = int(target)
            return([n,i,x,b,p,e],(target_address))
        except:
            target_address = symbol_table.get(target)
            return([n,i,x,b,p,e],(target_address))

    elif('@' in target):
        n,i = '1','0'
        
        #removing the # from target
        target = target[1:]
        flagzby=1
        # if(target is INTEGER )
        
        try:
            target_address = int(target)
            return([n,i,x,b,p,e],(target_address))
        except:
            target_address = symbol_table.get(target)
            # print("try me none",target)
            # print(target_address)
            return([n,i,x,b,p,e],(target_address))
    elif('=' in target):
        target_address = int(literal_table.get(target[3:-1])[0],16)
        # print("literal check",target[3:-1],target_address)
    else:
        target_address = symbol_table.get(target)
    if(',X' in target):
        x = '1'
        target = target[0:-2]
        target_address = symbol_table.get(target)
        return([n,i,x,b,p,e],(target_address))
    # target_address = symbol_table.get(target)
    if(format in [4,6] ):
        if(flagzby==1):
            target_address=int(target)
        b,p,e = '0','0','1'
        return([n,i,x,b,p,e],(target_address))
    # print(symbol_table.get(target))
    # print(loc_counter)
    disp = target_address - (int(loc_counter,16) + format)
    # print("base and displacement",base_loc,disp)
    if(disp >= -2048 and disp < 0):
        #b = 0 , p = 1
        b,p = '0','1'
        disp &= int('FFF',16)
        # return disp
    elif(disp <= 2047 and disp > 0):
        #b = 0 , p = 1
        b,p = '0','1'
        # return disp
    elif(target_address <= 4096 + base_loc and target_address >= base_loc ):
        #b = 1 , p = 0
        b,p = '1','0'
        disp = target_address - base_loc
    # except:
    else:
        print("Base Address hasn't been specified and the jump is too large for PC-relative addressing, Please use format 4 at {}".format(loc_counter))
        exit()
    # disp = hex(disp)[2:]
    
    return([n,i,x,b,p,e],(disp))


def SecondPass():
    
    for line in FirstPass_output:
        
        loc_counter, label, instruction, target = line
        
        # print(loc_counter, label, instruction, target)

        if(instruction in reserved):
            # if(instruction == "LTORG" or instruction == "END"):
            #     for i in literal_table:
            #         objectcode.append()
            if(instruction == "WORD"):
                objectcode.append([loc_counter,pad(identifyData(target),6,'0')])
                # ocode.append(pad(identifyData(target),6,'0'))
            elif(instruction == "BYTE"):
                objectcode.append([loc_counter,pad(identifyData(target),2,'0')])
                # ocode.append(pad(identifyData(target),2,'0'))
            elif(instruction == "RESW" or instruction == "RESB"):
                objectcode.append([loc_counter,skipper])
            else:
                objectcode.append([loc_counter,placeholder])
            continue

        elif(instruction[0] =='+'):

            
            # instruction = instruction[1:]
            # opcode = instruction_table.get(instruction)[1]
            form,opcode = instruction_table.get(instruction[1:])
            form+=1
            opcode = opcode >> 2
            objectcode.append([opcode,*format4(loc_counter,target)])
            

        elif(instruction[0] =='&'):

            
            # instruction = instruction[1:]
            # opcode = instruction_table.get(instruction)[1]
            form,opcode = instruction_table.get(instruction[1:])
            form+=1
            opcode = opcode >> 2
            objectcode.append([opcode,*format5(loc_counter,target)])

        elif(instruction[0] =='$'):
            # instruction = instruction[1:]
            # opcode = instruction_table.get(instruction)[1]
            form,opcode = instruction_table.get(instruction[1:])
            form+=1
            opcode = opcode >> 2
            objectcode.append([opcode,*format6(loc_counter,target)])
        elif(instruction == placeholder):
            objectcode.append([loc_counter,target])
            continue
        else:
            form,opcode = instruction_table.get(instruction)
            if(form == 1):
                # format1()
                objectcode.append([loc_counter,opcode])
                continue
            elif(form == 2):
                # dat = int(opcode,16)
                # dat = hex(dat),format2(target)
                # print(loc_counter,instruction,target)
                objectcode.append([loc_counter,hex(opcode)[2:]+"".join(format2(target))])
                continue
            elif(form == 3):
                opcode = opcode >> 2
                objectcode.append([opcode,*format3(loc_counter,target)])
            # print(instruction,form,hex(opcode))
        # print(objectcode[-1][1])
        
        # a= (int(objectcode[-1][1][0],2)<<1)
        # b= (int(objectcode[-1][1][1],2)<<0)  
        # bin(int(objectcode[-1][1][1],2)<<0) 
        # c=hex(a+b)
        # d=hex(objectcode[-1][0])
        # #print(c)
        # #print(d)
        # e=hex(int(c,16)+int(d,16))
        # print(e)
        # if( int(e,16) < 15 ):
        #     hex(int(e,16) << 1)
        #     print(e)

        # a= (int(objectcode[-1][1][2],2)<<3)
        # b= (int(objectcode[-1][1][3],2)<<2)
        # c= (int(objectcode[-1][1][4],2)<<1)
        # d= (int(objectcode[-1][1][5],2)<<0)

        # e=hex(a+b+c+d)
        # print(e)



        #last element in array, which contains the opcode
        #shifts the opcode right twice to get rid of 2 zeroes
        # [opcode, [flag array],target_address]
        # (objectcode[-1])[1] = "".join(objectcode[-1][1])
        # objectcode[-1][0] = objectcode[-1][0] >> 2
        #(0b)111111
        # print(objectcode[-1][1])

        # print(target,objectcode[-1])

        # if(objectcode[-1][0] == placeholder):
        #     continue
        #     print("objectcode[0]")
            # print(loc_counter, label, instruction, target, objectcode[-1],ocode)
        
        objectcode[-1][2] = hex(objectcode[-1][2])[2:]
        size = 3 if form == 3 else 5
        if(len(objectcode[-1][2]) < size):
            objectcode[-1][2] = (size - len(objectcode[-1][2]))*'0' + objectcode[-1][2]
        ocode = bin(objectcode[-1][0])[2:] + objectcode[-1][1] #+ objectcode[-1][2]
        ocode = hex(int(ocode,2))[2:] + objectcode[-1][2]
        ocode = pad(ocode,6,'0')
        print(objectcode[-1])
        objectcode[-1][0] = hex(objectcode[-1][0])
        objectcode[-1] = [loc_counter,ocode]
        print(loc_counter, label, instruction, target, objectcode[-1])
        
        # print(ocode)
        # print(objectcode[-1][1])
        # x b p e
        # 1 0 0 0
        # 0 1 0 0
        #
        
        
        # print(instruction,form,hex(opcode))
    

SecondPass()


def GenerateHRecord():
    program_name, starting_address = first_line
    program_name = pad(program_name,-6,padding)#(program_name + (6 - len(program_name))*padding)

    starting_address = int(starting_address,16)
    program_size = hex(final_address - starting_address)[2:]
    program_size = pad(program_size,6,'0')#((6 - len(program_size))*'0' + program_size)

    starting_address = hex(starting_address)[2:]
    starting_address = pad(starting_address,6,'0')#((6 - len(starting_address))*'0'+ starting_address)
    star = "H." + program_name + seperator + starting_address + seperator + program_size
    return(star)
for e in objectcode:
    print(e)
def GenerateTRecords():
    records = []
    max_size = 10
    size=0
    opcode_record = 'T'
    starting_address = objectcode[0][0]
    print(starting_address)
    for loc_counter,opcode in objectcode:
        if(size == 0):
            starting_address= loc_counter
        if(opcode == placeholder):
            print("skipped")
            continue
        if(opcode == skipper):
            print("skipper'd")
            print(starting_address,size/2,opcode_record)
            size = 0
            opcode_record = 'T'
            continue

        if(size + len(opcode) > 60):
            print(starting_address,size/2,opcode_record)
            # if(loc_counter == '$'):
            #     continue
            starting_address = loc_counter
            size = len(opcode)
            opcode_record = 'T.' + opcode
            continue
        # print("premod",size,'+',len(opcode),opcode,opcode_record)
        size += len(opcode)
        opcode_record += '.'+opcode
        # print("postmod",size,opcode_record)
    print(starting_address,size/2,opcode_record)
            # if(loc_counter == '$'):
            #     continue
    # starting_address = loc_counter
    # size = len(opcode)
    # opcode_record = 'T.' + opcode
# for i in objectcode:
#     print(i)
print(GenerateHRecord())
GenerateTRecords()
# def GenerateHTE():