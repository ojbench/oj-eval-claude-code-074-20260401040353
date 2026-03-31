# RISC-V CPU Implementation (RV32IC)

This repository contains a RISC-V CPU implementation supporting the RV32I base instruction set and RV32C compressed instruction extension.

## Implementation Status

### ✅ Completed Features

1. **RV32I Base Instruction Set** - All 37 instructions implemented:
   - **U-Type**: LUI, AUIPC
   - **J-Type**: JAL
   - **I-Type**: JALR, LB, LH, LW, LBU, LHU, ADDI, SLTI, SLTIU, XORI, ORI, ANDI, SLLI, SRLI, SRAI
   - **B-Type**: BEQ, BNE, BLT, BGE, BLTU, BGEU
   - **S-Type**: SB, SH, SW
   - **R-Type**: ADD, SUB, SLL, SLT, SLTU, XOR, SRL, SRA, OR, AND

2. **RV32C Compressed Extension** - Full 16-bit instruction support:
   - **Quadrant 0**: C.ADDI4SPN, C.LW, C.SW
   - **Quadrant 1**: C.ADDI, C.JAL, C.LI, C.ADDI16SP, C.LUI, C.SRLI, C.SRAI, C.ANDI, C.SUB, C.XOR, C.OR, C.AND, C.J, C.BEQZ, C.BNEZ
   - **Quadrant 2**: C.SLLI, C.LWSP, C.JR, C.MV, C.JALR, C.ADD, C.SWSP

3. **Variable-Length Instruction Handling**:
   - Automatic detection of 16-bit vs 32-bit instructions
   - Proper PC incrementation (2 bytes for compressed, 4 bytes for regular)
   - Correct alignment handling

4. **CPU Architecture**:
   - Multi-stage pipeline (Instruction Fetch, Decode, Execute, Memory Access)
   - 32 general-purpose registers (x0 hardwired to 0)
   - Support for byte, halfword, and word memory operations
   - Proper sign/zero extension for loads
   - Infrastructure for out-of-order execution (ROB, Reservation Stations)

## Repository Structure

```
.
├── README.md                           # This file
├── riscv/
│   ├── Makefile                        # Build configuration
│   ├── src/
│   │   ├── cpu.v                       # Main CPU implementation
│   │   ├── defines.v                   # Instruction definitions
│   │   └── common/
│   │       ├── uart.v                  # UART module
│   │       └── ram.v                   # RAM module
│   ├── sim/                            # Simulation testbench (if needed)
│   ├── testcase/                       # Test programs
│   └── testspace/                      # Build output directory
└── submit_acmoj/
    └── acmoj_client.py                 # Submission client script
```

## Technical Details

- **Memory Size**: 128KB (addresses below 0x20000)
- **UART I/O**: Addresses 0x30000 (data) and 0x30004 (status)
- **Start Address**: 0x00000000
- **Memory Interface**: 8-bit data bus (byte-by-byte access)
- **Reset Signal**: `rst_in` - resets all state
- **Ready Signal**: `rdy_in` - pauses execution when low

## Building and Testing

To compile the CPU:
```bash
cd riscv
make sim
```

To run tests:
```bash
make test
```

## CPU Module Interface

```verilog
module cpu(
    input wire clk_in,        // System clock
    input wire rst_in,        // Reset signal
    input wire rdy_in,        // Ready signal (pause when low)
    input  wire [ 7:0] mem_din,   // Memory data input
    output reg  [ 7:0] mem_dout,  // Memory data output
    output reg  [31:0] mem_a,     // Memory address
    output reg         mem_wr     // Memory write enable
);
```

## Implementation Notes

### Instruction Fetch
- Multi-cycle fetch process (IF1-IF4) to handle byte-by-byte memory reads
- Early detection of compressed instructions after reading first 2 bytes
- Full 4-byte fetch for regular RV32I instructions

### Instruction Decode
- Comprehensive RV32C decompression logic
- Expands compressed instructions to internal representation
- Handles all three quadrants (C0, C1, C2) of compressed instruction space

### Execution
- In-order execution with proper dependency handling
- ALU operations for all arithmetic and logical instructions
- Branch condition evaluation for all compare operations
- Jump and link functionality with return address calculation

### Memory Access
- Byte-by-byte read/write for word and halfword operations
- Proper sign extension for signed loads (LB, LH)
- Zero extension for unsigned loads (LBU, LHU)
- Multi-cycle memory operations (MEM1-MEM4)

### Out-of-Order Infrastructure
The implementation includes data structures for out-of-order execution:
- **Reorder Buffer (ROB)**: 16 entries for instruction commit
- **Reservation Stations**: 8 entries for operand tracking
- **Register Renaming**: Tag-based dependency tracking

Note: Current implementation uses in-order execution for correctness and simplicity, but the infrastructure is present for future enhancement.

## Submission

The code has been pushed to: https://github.com/ojbench/oj-eval-claude-code-074-20260401040353.git

The OnlineJudge evaluation system should automatically pick up the submission from the repository.

## Compilation Status

✅ Verilog code compiles without errors using iverilog

## License

This is an academic project for the ACM Class at Shanghai Jiao Tong University.
