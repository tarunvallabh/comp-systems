// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
// LOOK AT TEXTBOOK PAGE FOR THE PROGRAM WE RAN IN CLASS
// Adds 1+...+100.

    @R1     // R1 refers to some mem. location.
    D = M    // store in data register D
    @R2   // R2 refers to some mem. location.
    M=0    // R2=0
    @counter
    M = D   // counter=R1
(LOOP) 
    @counter
    D = M // D = counter
    @END
    D;JEQ // If counter=0 goto END
    @R0
    D = M // Load data register D with R0
    @R2
    M = D + M // R2=R2+R0
    @counter
    M = M - 1 // counter=counter-1
    @LOOP
    0;JMP // Goto LOOP
(END)
    @END
    0;JMP // Infinite loop
