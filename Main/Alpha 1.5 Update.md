# Xenakis <font size="3" >_by Carlos Mauro_ </font>

## _A graphic music notation handler_

_July, 2022_

## Alpha 1.5 update:

### This update achieved:

- Simplification of code:
  - This version only contains the png to score generator to simplify code and to focus on its functions exhaustively.
  - The other functionalities will be developed once the main one is ready.
- Auto Scaling:
  - Now the algorithm will scale all data to 2200 to {max_midi_note}.
  - This scaling is sort of customizable.
- LARGE files now supported
  - If output is LARGE, it will be splited into batches of a maximun of 9999 events per batch
  - This allows MAX 8 to read and load the data without crashing.

### In the future:

- Comprehensive tests
- Image preview on separate pop-up window
  - For single layer:
    - Default status = 0
    - Trigger pop-up window function
    - If status = 0 --> Generate pop-up window
      - Set status to 1.
    - Else (status =! 0):
      - Update pop-up image.
  - For combined layer:
    - Same as single layer, but with different instance name.
