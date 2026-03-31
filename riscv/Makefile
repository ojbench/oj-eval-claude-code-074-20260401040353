# RISC-V CPU Makefile

.PHONY: all clean test sim

VERILOG_SRC = src/cpu.v src/common/uart.v src/common/ram.v

all: sim

sim:
	iverilog -o testspace/cpu_sim $(VERILOG_SRC) sim/testbench.v

test: sim
	cd testspace && ./cpu_sim

clean:
	rm -rf testspace/*
