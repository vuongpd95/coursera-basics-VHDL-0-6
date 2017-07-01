// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
(TOP)
	@SCREEN
	D=A
	@0
	M=D
	@24576
	D=M
	@BKS
	D;JNE
(WTS)
	@0
	D=M
	M=M+1
	A=D
	M=0
	@24575
	D=D-A
	@TOP
	D;JGE
	@WTS
	0;JMP
(BKS)
	@0
	D=M
	M=M+1
	A=D
	M=-1
	@24575
	D=D-A
	@TOP
	D;JGE
	@BKS
	0;JMP