// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
	@sum
	M=0
	@count
	M=1
(LOOP)
	@count
	D=M
	@1
	D=D-M
	@EVAL
	D;JGT
	@0
	D=M
	@sum
	M=M+D
	@count
	M=M+1
	@LOOP
	0;JMP
(EVAL)
	@sum
	D=M
	@2
	M=D
(END)
