# Blob Game in the Jack programming language

The Blob Game is an interactive experience where players guide a friendly blob through a field of poison and food blobs. You control a smiley blob, and your objective is to consume all food blobs while avoiding the deadly poison blobs. This game was designed in Jack, a simple object-based laguage.

## How to Play

- The game begins with instructions displayed on the screen.
- Players use the arrow keys to control the blob's movement:
    - Up Arrow: Move up
    - Down Arrow: Move down
    - Left Arrow: Move left
    - Right Arrow: Move right
- The objective is to eat all food blobs without touching any poison blobs or the game border.

## Game Over Conditions

- **Poisoned:** Touching a poison blob results in a loss, halting the program and displaying a message.
- **Fence Collision:** Colliding with the game's border fence also results in a loss, halting the program and displaying a message.
- **Victory:** Successfully eating all food blobs leads to a win, halting the program and displaying a message. 

## Game Structure
The game is built around several key classes:
- **Game:** The primary class that initializes and manages the game's components and flow.
- **Blob:** Represents the player's character.
- **PoisonBlob and FoodBlob:** Represent the game's hazards and objectives, respectively.

## Compilation and Execution

The game's code was compiled using the Jack compiler provided by the nand2tetris course. It was then run on the VM emulator, also provided by nand2tetris, to ensure correct functionality and performance.

## Limitations
The game works as expected, with no known flaws in functionality. The player blob may flicker occasionaly due to the graphics updating of the blob during movement.








