#!/usr/bin/env python3

# Written by Thomas Roth <contact@stacksmashing.net>
# Send me a message on Twitter if you run into trouble! @ghidraninja
# Licensed under GPLv3

PREFIX_JMP  = 0b000
PREFIX_WAIT = 0b001
PREFIX_IN   = 0b010
PREFIX_OUT  = 0b011
PREFIX_PUSH = 0b100
PREFIX_PULL = 0b100
PREFIX_PUSH_PULL = 0b100
PREFIX_MOV  = 0b101
PREFIX_IRQ  = 0b110
PREFIX_SET  = 0b111

# Bit 7 inidcates whether it's push or pull
PUSH_BIT_7  = 0b0
PULL_BIT_7  = 0b1

# Conditions for JMP
CONDITION_ALWAYS        = 0b000
CONDITION_X_ZERO        = 0b001
CONDITION_X_NON_ZERO_PD = 0b10
CONDITION_Y_ZERO        = 0b011
CONDITION_Y_NOT_ZERO_PD = 0b100
CONDITINO_X_NOT_EQUAL_Y = 0b101
CONDITION_BRANCH_ON_PIN = 0b110
CONDITION_OSR_NOT_EMPTY = 0b111 # Output shift register not empty

JMP_CONDITIONS = {
    CONDITION_ALWAYS: None,
    CONDITION_X_ZERO: "!X",
    CONDITION_X_NON_ZERO_PD: "X--",
    CONDITION_Y_ZERO: "!Y",
    CONDITION_Y_NOT_ZERO_PD: "Y--",
    CONDITINO_X_NOT_EQUAL_Y: "X!=Y",
    CONDITION_BRANCH_ON_PIN: "PIN",
    CONDITION_OSR_NOT_EMPTY: "!OSRE"
}

# Wait sources 3.4.3.2
WAIT_SOURCE_GPIO     = 0b00
WAIT_SOURCE_PIN      = 0b01
WAIT_SOURCE_IRQ      = 0b10
WAIT_SOURCE_RESERVED = 0b11

WAIT_SOURCES = {
    WAIT_SOURCE_GPIO: "GPIO",
    WAIT_SOURCE_PIN: "PIN",
    WAIT_SOURCE_IRQ: "IRQ",
    WAIT_SOURCE_RESERVED: "RESERVED",
}


# IN sources 3.4.4.2
IN_SOURCE_PINS       = 0b000
IN_SOURCE_X          = 0b001
IN_SOURCE_Y          = 0b010
IN_SOURCE_NULL       = 0b011
IN_SOURCE_RESERVED_1 = 0b100
IN_SOURCE_RESERVED_2 = 0b101
IN_SOURCE_ISR        = 0b110
IN_SOURCE_OSR        = 0b111

IN_SOURCES = {
    IN_SOURCE_PINS: "PINS",
    IN_SOURCE_X: "X",
    IN_SOURCE_Y: "Y",
    IN_SOURCE_NULL: "NULL",
    IN_SOURCE_RESERVED_1: "RESERVED",
    IN_SOURCE_RESERVED_2: "RESERVED",
    IN_SOURCE_ISR: "ISR",
    IN_SOURCE_OSR: "OSR"
}

# OUT destinations 3.4.5.2
OUT_DEST_PINS    = 0b000
OUT_DEST_X       = 0b001
OUT_DEST_Y       = 0b010
OUT_DEST_NULL    = 0b011
OUT_DEST_PINDIRS = 0b100
OUT_DEST_PC      = 0b101
OUT_DEST_ISR     = 0b110
OUT_DEST_EXEC    = 0b111
OUT_DESTINATIONS = {
    OUT_DEST_PINS: "PINS",
    OUT_DEST_X: "X",
    OUT_DEST_Y: "Y",
    OUT_DEST_NULL: "NULL",
    OUT_DEST_PINDIRS: "PINDIRS",
    OUT_DEST_PC: "PC",
    OUT_DEST_ISR: "ISR",
    OUT_DEST_EXEC: "EXEC"
}

# MOV destinations 3.4.8.2
MOV_DEST_PINS     = 0b000
MOV_DEST_X        = 0b001
MOV_DEST_Y        = 0b010
MOV_DEST_RESERVED = 0b011
MOV_DEST_EXEC     = 0b100
MOV_DEST_PC       = 0b101
MOV_DEST_ISR      = 0b110
MOV_DEST_OSR      = 0b111
MOV_DESTINATIONS = {
    MOV_DEST_PINS: "PINS",
    MOV_DEST_X: "X",
    MOV_DEST_Y: "Y",
    MOV_DEST_RESERVED: "RESERVED",
    MOV_DEST_EXEC: "EXEC",
    MOV_DEST_PC: "PC",
    MOV_DEST_ISR: "ISR",
    MOV_DEST_OSR: "OSR"
}

# MOV operations 3.4.8.2
MOV_OP_NONE        = 0b00
MOV_OP_INVERT      = 0b01
MOV_OP_BIT_REVERSE = 0b10
MOV_OP_RESERVED    = 0b11
MOV_OPERATIONS = {
    MOV_OP_NONE: "",
    MOV_OP_INVERT: "!",
    MOV_OP_BIT_REVERSE: "::",
    MOV_OP_RESERVED: "RESERVED"
}

# MOV source 3.4.8.2
MOV_SOURCE_PINS     = 0b000
MOV_SOURCE_X        = 0b001
MOV_SOURCE_Y        = 0b010
MOV_SOURCE_NULL     = 0b011
MOV_SOURCE_RESERVED = 0b100
MOV_SOURCE_STATUS   = 0b101
MOV_SOURCE_ISR      = 0b110
MOV_SOURCE_OSR      = 0b111
MOV_SOURCES = {
    MOV_SOURCE_PINS: "PINS",
    MOV_SOURCE_X: "X",
    MOV_SOURCE_Y: "Y",
    MOV_SOURCE_NULL: "NULL",
    MOV_SOURCE_RESERVED: "RESERVED",
    MOV_SOURCE_STATUS: "STATUS",
    MOV_SOURCE_ISR: "ISR",
    MOV_SOURCE_OSR: "OSR"
}

# SET destination 3.4.10.2
SET_DEST_PINS = 0b000
SET_DEST_X = 0b001
SET_DEST_Y = 0b010
SET_DEST_RESERVED_1 = 0b011
SET_DEST_PINDIRS = 0b100
SET_DEST_RESERVED_2 = 0b101
SET_DEST_RESERVED_3 = 0b110
SET_DEST_RESERVED_4 = 0b111
SET_DESTINATIONS = {
    SET_DEST_PINS: "PINS",
    SET_DEST_X: "X",
    SET_DEST_Y: "Y",
    SET_DEST_RESERVED_1: "RESERVED",
    SET_DEST_PINDIRS: "PINDIRS",
    SET_DEST_RESERVED_2: "RESERVED",
    SET_DEST_RESERVED_3: "RESERVED",
    SET_DEST_RESERVED_4: "RESERVED"
}


class Instruction:
    def __init__(self, assembly, reference=None):
        self.assembly = assembly
        self.reference = reference
        self.sideset = ""

def parse_jmp(instruction: int):
    condition = (instruction >> 5) & 0b111
    condition_string = JMP_CONDITIONS[condition]
    address = instruction & 0b11111
    if condition_string:
        return Instruction("jmp " + condition_string + " label_" + hex(address), address)
    else:
        return Instruction("jmp " + hex(address))

def parse_wait(instruction: int):
    index = instruction & 0b11111
    polarity = instruction >> 7 & 0b1
    source = instruction >> 5 & 0b11
    source_string = WAIT_SOURCES[source]
    # TODO: No support for (rel) mark yet
    return Instruction("wait " + str(polarity) + " " + source_string + " " + str(index))

def parse_in(instruction: int):
    source = (instruction >> 5) & 0b111
    source_str = IN_SOURCES[source]
    bitcount = instruction & 0b11111
    if bitcount == 0:
        bitcount = 32
    return Instruction("in " + source_str + ", " + str(bitcount))

def parse_out(instruction: int):
    destination = (instruction >> 5) & 0b111
    destination_str = OUT_DESTINATIONS[destination]
    bitcount = instruction & 0b11111
    if bitcount == 0:
        bitcount = 32
    return Instruction("out " + destination_str + ", " + str(bitcount))

def parse_pull(instruction: int):
    ret = "pull "
    if (instruction >> 6) & 0b1:
        ret += "ifempty "
    if (instruction >> 5) & 0b1:
        ret += "block"
    else:
        ret += "noblock"
    return Instruction(ret)

def parse_push(instruction: int):
    ret = "push "
    if (instruction >> 6) & 0b1:
        ret += "iffull "
    if (instruction >> 5) & 0b1:
        ret += "block"
    else:
        ret += "noblock"
    return Instruction(ret)

def parse_pushpull(instruction: int):
    if (instruction >> 7) & 0b1:
        # Pull
        return parse_pull(instruction)
    else:
        return parse_push(instruction)

def parse_mov(instruction: int):
    source = instruction & 0b111
    op = (instruction >>3) & 0b11
    destination = (instruction >> 5) & 0b111

    destination_str = MOV_DESTINATIONS[destination]
    op_str = MOV_OPERATIONS[op]
    source_str = MOV_SOURCES[source]

    return Instruction("mov " + destination_str + ", " + op_str + source_str)

def parse_irq(instruction: int):
    index = instruction & 0b11111
    irq_index = index & 0b111
    wait = (instruction >> 5) & 0b1
    clr = (instruction >> 6) & 0b1

    ret = "irq "
    if clr:
        ret += "clear "
    else:
        if wait:
            ret += "wait "
        else:
            ret += "nowait "
    
    ret += str(irq_index)

    return Instruction(";IRQ support is not yet great!\n\t" + ret)




def parse_set(instruction: int):
    data = instruction & 0b11111
    destination = (instruction >> 5) & 0b111
    destination_str = SET_DESTINATIONS[destination]
    return Instruction("set " + destination_str + ", " + str(data))

parsers = {
    PREFIX_JMP: parse_jmp,
    PREFIX_IN: parse_in,
    PREFIX_OUT: parse_out,
    PREFIX_WAIT: parse_wait,
    PREFIX_PUSH_PULL: parse_pushpull,
    PREFIX_MOV: parse_mov,
    PREFIX_IRQ: parse_irq,
    PREFIX_SET: parse_set
}

def parse_sideset(instruction: int, sideset: int, sideset_en: bool):
    # sideset_en is a mapping for EXECCTRL_SIDE_EN: If this is one,
    # the very first bit is reserved for that

    delay_side_set = (instruction >> 8) & 0b11111

    # default values
    sideset_bits = 0
    delay_bits = 5

    if sideset > 0:
        sideset_bits = sideset
        if sideset_en:
            sideset_bits += 1
        
        delay_bits -= sideset_bits
    
    # Mask to filter out delay
    delay_mask = (2**delay_bits) - 1
    sideset_mask = (2**sideset_bits) - 1
    
    # Parse delay
    delay = delay_side_set & delay_mask

    # Parse sideset
    sideset_en_value = 0
    if sideset_en:
        sideset_en_value = (delay_side_set  >> 4) & 0b1
        # Clear first bit for side set parsing
        delay_side_set &= 0b01111
    else:
        if (delay_side_set >> delay_bits) > 0:
            sideset_en_value = 1
    
    sideset = delay_side_set >> delay_bits

    result = ""
    if sideset_en_value:
        result += "side " + str(sideset)
    
    if delay > 0:
        if len(result) > 0:
            result += " "
        result += "[" + str(delay) + "]"
    
    return result


def parse(instruction: int, sideset: int, sideset_en: bool):
    prefix = (instruction >> 13) & 0b111
    try:
        parser = parsers[prefix]
        parse_result = parser(instruction)
        parse_result.sideset = parse_sideset(instruction, sideset, sideset_en)
        return parse_result
    except:
        pass
    return Instruction(f"{bin(prefix)} not implemented")


if __name__ == "__main__":
    import argparse
    import struct, sys
    parser = argparse.ArgumentParser(description="Disassemble a PIO hex file.")
    parser.add_argument("--name", dest="name", type=str, default="piodisasm_result", help="Name for program")
    parser.add_argument("--sideset", dest="sideset", type=int, default=0, help="Sideset value to use.")
    parser.add_argument("--sideset-optional", dest="sideset_optional", type=bool, default=False, help="Sideset optional.")
    parser.add_argument("--sideset-pindirs", dest="sideset_pindirs", type=bool, default=False, help="Sideset applies to PINDIRS.")
    parser.add_argument("--sideset-enable", dest="sideset_en", type=bool, default=False, help="Whether the sideset enable pin (EXECCTRL_SIDE_EN) is set.")
    parser.add_argument("pio_file", type=argparse.FileType("r"))
    args = parser.parse_args()
    data = bytes.fromhex(args.pio_file.read())
    if len(data) % 2 != 0:
        print("Program length % 2 is not 0.")
        sys.exit(1)

    parsed_instructions = []
    while True:
        instruction_data = data[:2]
        if len(instruction_data) != 2:
            break
        data = data[2:]
        instruction = struct.unpack(">H", instruction_data)[0]
        parsed_instructions.append(parse(instruction, args.sideset, args.sideset_en))
    
    references = []
    for i in parsed_instructions:
        if i.reference == None:
            continue
        if i.reference in references:
            continue
        references.append(i.reference)
    
    print("; Generated by piodisasm\n\n")
    print(".program " + args.name)
    if args.sideset > 0:
        print(".side_set " + str(args.sideset), end="")
        if args.sideset_optional:
            print(" opt", end="")
        if args.sideset_pindirs:
            print(" pindirs", end="")
        print()

    print("\n\n; program starts here\n\n")
    for i in range(0, len(parsed_instructions)):
        # i contains current address
        if i in references:
            print("label_" + hex(i) + ":")
        print("\t" + parsed_instructions[i].assembly, end="")
        if len(parsed_instructions[i].sideset) > 0:
            print("\t" + parsed_instructions[i].sideset, end="")
        print()