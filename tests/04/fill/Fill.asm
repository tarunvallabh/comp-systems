// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

    @SCREEN 
    D = A
    @pixelindex   // set pixel pointer to screen address
    M = D
(LOOP)
    @KBD // check if key is pressed
    D = M
    @KEYPRESSED  
    D;JGT   // if pressed, go to keypressed
    @KEYNOTPRESSED
    D;JLE  // if not pressed, go to keynotpressed
(KEYPRESSED)
    @KBD
    D = A   // store the kdb address in data
    @pixelindex
    D = D - M  // check if the pixel index is less than the kdb address
    @LOOP
    D;JEQ // if pixel index is less than kdb address, go to loop
    @pixelindex 
    A = M // go to address of pixel to change
    M = -1 // change pixel to black
    @pixelindex
    M = M + 1 // move to next pixel
    @LOOP // go back to loop
    0;JMP
(KEYNOTPRESSED)
    @SCREEN
    D = A // store the kdb address in data
    @pixelindex
    D = M - D // check if the pixel index is greater than or equal to screen
    @LOOP
    D;JLT // if pixel index is greater than or equal to screen, go to loop
    @pixelindex
    A = M // go to address of pixel to change
    M = 0 // change pixel to white
    @pixelindex
    M = M - 1 // move to previous pixel
    @LOOP // go back to loop
    0;JMP


